from time import time
from typing import List, Tuple, Dict
from abc import ABC
from abc import abstractmethod

import numpy as np

from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import StratifiedKFold, LeaveOneGroupOut
from sklearn.feature_selection import RFECV

from pica.ml.vectorizer import CustomVectorizer
from pica.structure.records import TrainingRecord, GenotypeRecord
from pica.ml.cccv import CompleContaCV
from pica.util.helpers import get_x_y_tn, get_groups
from pica.ml.feature_select import recursive_feature_elimination, compress_vocabulary, DEFAULT_STEP_SIZE,\
    DEFAULT_SCORING_FUNCTION


class TrexClassifier(ABC):
    """
    Abstract base class of Trex classifier.
    """
    def __init__(self, random_state: int = None, verb: bool = False):
        self.trait_name = None
        self.cccv_result = None
        self.pipeline = None
        self.cv_pipeline = None
        self.logger = None
        self.random_state = np.random.RandomState(random_state)
        self.verb = verb
        self.vectorizer = CustomVectorizer(binary=True, dtype=np.bool)

    def train(self, records: List[TrainingRecord], reduce_features: bool = False,
              n_features: int = 10000, **kwargs):
        """
        Fit CountVectorizer and train LinearSVC on a list of TrainingRecord.

        :param records: a List[TrainingRecord] for fitting of CountVectorizer and training of LinearSVC.
        :param reduce_features: toggles feature reduction using recursive feature elimination
        :param n_features: minimum number of features to retain when reducing features
        :param kwargs: additional named arguments are passed to the fit() method of Pipeline.
        :returns: Whether the Pipeline has been fitted on the records.
        """

        self.logger.info("Begin training classifier.")
        X, y, tn = get_x_y_tn(records)
        if self.trait_name is not None:
            self.logger.warning("Pipeline is already fitted. Refusing to fit again.")
            return False

        if reduce_features:
            self.logger.info("using recursive feature elimination as feature selection strategy")
            # use non-calibrated classifier
            recursive_feature_elimination(records, self.cv_pipeline, n_features=n_features)
            compress_vocabulary(records, self.pipeline)

        self.trait_name = tn

        self.pipeline.fit(X=X, y=y, **kwargs)
        self.logger.info("Classifier training completed.")
        return self

    @abstractmethod
    def get_feature_weights(self) -> Dict:
        pass

    def crossvalidate(self, records: List[TrainingRecord], cv: int = 5,
                      scoring: str = DEFAULT_SCORING_FUNCTION, n_jobs=-1,
                      n_replicates: int = 10, groups: bool = False,
                      # TODO: add more complex scoring/reporting, e.g. AUC
                      reduce_features: bool = False, n_features: int = 10000,
                      demote=False, **kwargs) -> Tuple[float, float, np.ndarray]:
        """
        Perform cv-fold crossvalidation or leave-one(-group)-out validation if groups == True

        :param records: List[TrainingRecords] to perform crossvalidation on.
        :param scoring: Scoring function of crossvalidation. Default: Balanced Accuracy.
        :param cv: Number of folds in crossvalidation. Default: 5
        :param n_jobs: Number of parallel jobs. Default: -1 (All processors used)
        :param n_replicates: Number of replicates of the crossvalidation
        :param groups: If True, use group information stored in records for splitting. Otherwise,
            stratify split according to labels in records. This also resets n_replicates to 1.
        :param reduce_features: toggles feature reduction using recursive feature elimination
        :param n_features: minimum number of features to retain when reducing features
        :param demote: toggles logger that is used. if true, msg is written to debug else info
        :param kwargs: Unused
        :return: A list of mean score, score SD, and the percentage of misclassifications per sample
        """

        log_function = self.logger.debug if demote else self.logger.info
        t1 = time()
        X, y, tn = get_x_y_tn(records)

        # unfortunately RFECV does not work with pipelines (need to use the vectorizer separately)
        self.cv_pipeline.fit(X, y)
        vec = self.cv_pipeline.named_steps["vec"]
        clf = self.cv_pipeline.named_steps["clf"]

        if not vec.vocabulary:
            vec.fit(X)
        X_trans = vec.transform(X)

        misclassifications = np.zeros(len(y))
        scores = []

        if groups:
            log_function("Begin Leave-One-Group-Out validation on training data.")
            splitting_strategy = LeaveOneGroupOut()
            group_ids = get_groups(records)
            n_replicates = 1
        else:
            log_function("Begin cross-validation on training data.")
            splitting_strategy = StratifiedKFold(n_splits=cv, shuffle=True,
                                                 random_state=self.random_state)
            group_ids = None

        for i in range(n_replicates):
            inner_cv = StratifiedKFold(n_splits=cv, shuffle=True,
                                       random_state=self.random_state)
            outer_cv = splitting_strategy
            for tr, ts in outer_cv.split(X_trans, y, groups=group_ids):
                if reduce_features:
                    est = RFECV(estimator=clf, cv=inner_cv, n_jobs=n_jobs,
                                step=DEFAULT_STEP_SIZE, min_features_to_select=n_features,
                                scoring=DEFAULT_SCORING_FUNCTION)
                else:
                    est = clf
                est.fit(X_trans[tr], y[tr])
                y_pred = est.predict(X_trans[ts])
                mismatch = np.logical_xor(y[ts], y_pred)
                mismatch_indices = ts[np.where(mismatch)]
                misclassifications[mismatch_indices] += 1
                score = balanced_accuracy_score(y[ts], y_pred)
                scores.append(score)
            log_function(f"Finished replicate {i + 1} of {n_replicates}")

        misclassifications /= n_replicates
        score_mean, score_sd = float(np.mean(scores)), float(np.std(scores))
        t2 = time()
        log_function(f"Cross-validation completed.")
        log_function(f"Total duration of cross-validation: {np.round(t2 - t1, 2)} seconds.")
        return score_mean, score_sd, misclassifications

    def predict(self, X: List[GenotypeRecord]) -> Tuple[List[str], np.ndarray]:
        """
        Predict trait sign and probability of each class for each supplied GenotypeRecord.

        :param X: A List of GenotypeRecord for each of which to predict the trait sign
        :return: a Tuple of predictions and probabilities of each class for each GenotypeRecord in X.
        """
        features: List[str] = [" ".join(x.features) for x in X]
        preds = self.pipeline.predict(X=features)
        probas = self.pipeline.predict_proba(
            X=features)  # class probabilities via Platt scaling
        return preds, probas

    def crossvalidate_cc(self, records: List[TrainingRecord], cv: int = 5,
                         comple_steps: int = 20, conta_steps: int = 20,
                         n_jobs: int = -1, n_replicates: int = 10,
                         reduce_features: bool = False, n_features: int = 10000):
        """
        Instantiates a CompleContaCV object, and calls its run_cccv method with records. Returns its result.

        :param records: List[TrainingRecord] on which completeness_contamination_CV is to be performed
        :param cv: number of folds in StratifiedKFold split
        :param comple_steps: number of equidistant completeness levels
        :param conta_steps: number of equidistant contamination levels
        :param n_jobs: number of parallel jobs (-1 for n_cpus)
        :param n_replicates: Number of times the crossvalidation is repeated
        :param reduce_features: toggles feature reduction using recursive feature elimination
        :param n_features: selects the minimum number of features to retain (if feature reduction is used)
        :return: A dictionary with mean balanced accuracies for each combination: dict[comple][conta]=mba
        """

        cccv = CompleContaCV(pipeline=self.cv_pipeline, cv=cv,
                             comple_steps=comple_steps, conta_steps=conta_steps,
                             n_jobs=n_jobs, n_replicates=n_replicates,
                             random_state=self.random_state, verb=self.verb,
                             reduce_features=reduce_features, n_features=n_features)
        score_dict = cccv.run(records=records)
        self.cccv_result = score_dict
        return score_dict
