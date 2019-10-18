#
# Created by Lukas Lüftinger on 17/02/2019.
#
first_genotype_accession = {
    "Sulfate_reducer": "GCA_000007085.1",
}

first_phenotype_accession = {
    "Sulfate_reducer": "GCA_000007085.1",
}

cv_scores_trex = {
    'SVM': {'Sulfate_reducer': {3 : {'accuracy'         : (0.9477939477939478, 0.04189200493982592),
                                     'balanced_accuracy': (0.94017094017094, 0.04262807124628204),
                                     'f1'               : (
                                     0.9220779220779222, 0.05903974760599939)},
                                5 : {'accuracy'         : (0.9375494071146246, 0.06028931377996689),
                                     'balanced_accuracy': (0.9264285714285714, 0.06660030710912283),
                                     'f1'               : (
                                     0.9046153846153846, 0.08991777966893824)},
                                10: {'accuracy'         : (0.930909090909091, 0.08231108542721141),
                                     'balanced_accuracy': (0.9145833333333334, 0.11427990126585398),
                                     'f1'               : (
                                     0.8746031746031747, 0.17762606905565204)}}},
    }

cccv_scores_trex = {'SVM': {'Sulfate_reducer': {0.0 : {0.0 : {'score_mean': 0.5,
                                                              'score_sd'  : 0.0},
                                                       0.33: {'score_mean': 0.04583333333333333,
                                                              'score_sd'  : 0.044253060157839176},
                                                       0.67: {'score_mean': 0.02,
                                                              'score_sd'  : 0.016329931618554522},
                                                       1.0 : {'score_mean': 0.12595238095238095,
                                                              'score_sd'  : 0.11039097698840025}},
                                                0.33: {0.0 : {'score_mean': 0.9197619047619046,
                                                              'score_sd'  : 0.06771120480567323},
                                                       0.33: {'score_mean': 0.5235714285714286,
                                                              'score_sd'  : 0.08462925180320913},
                                                       0.67: {'score_mean': 0.07761904761904763,
                                                              'score_sd'  : 0.031027495852327707},
                                                       1.0 : {'score_mean': 0.1136904761904762,
                                                              'score_sd'  : 0.07228847475750501}},
                                                0.67: {0.0 : {'score_mean': 0.9264285714285714,
                                                              'score_sd'  : 0.06660030710912283},
                                                       0.33: {'score_mean': 0.8476785714285715,
                                                              'score_sd'  : 0.10143849157837544},
                                                       0.67: {'score_mean': 0.5102380952380952,
                                                              'score_sd'  : 0.045174453981393144},
                                                       1.0 : {'score_mean': 0.27803571428571433,
                                                              'score_sd'  : 0.1312048972283022}},
                                                1.0 : {0.0 : {'score_mean': 0.9264285714285714,
                                                              'score_sd'  : 0.06660030710912283},
                                                       0.33: {'score_mean': 0.9001785714285714,
                                                              'score_sd'  : 0.07517166672662015},
                                                       0.67: {'score_mean': 0.6789285714285714,
                                                              'score_sd'  : 0.12519463305239853},
                                                       1.0 : {'score_mean': 0.5233928571428571,
                                                              'score_sd'  : 0.038916737680017945}}}},
                    'XGB': {'Sulfate_reducer': {0.0 : {0.0 : {'score_mean': 0.5, 'score_sd': 0.0},
                                                       0.33: {'score_mean': 0.4545833333333333,
                                                              'score_sd'  : 0.033706247360261135},
                                                       0.67: {'score_mean': 0.20208333333333328,
                                                              'score_sd'  : 0.04174991683291783},
                                                       1.0 : {'score_mean': 0.08595238095238095,
                                                              'score_sd'  : 0.08744418368748703}},
                                                0.33: {0.0 : {'score_mean': 0.5803571428571429,
                                                              'score_sd'  : 0.07533936824903209},
                                                       0.33: {'score_mean': 0.42791666666666667,
                                                              'score_sd'  : 0.0757325337399104},
                                                       0.67: {'score_mean': 0.2436904761904762,
                                                              'score_sd'  : 0.06258508947054628},
                                                       1.0 : {'score_mean': 0.10440476190476188,
                                                              'score_sd'  : 0.03318760662596944}},
                                                0.67: {0.0 : {'score_mean': 0.8670238095238093,
                                                              'score_sd'  : 0.042223490254261316},
                                                       0.33: {'score_mean': 0.7105357142857143,
                                                              'score_sd'  : 0.06581610900138074},
                                                       0.67: {'score_mean': 0.565952380952381,
                                                              'score_sd'  : 0.0633604600874578},
                                                       1.0 : {'score_mean': 0.3727380952380953,
                                                              'score_sd'  : 0.10284667054272274}},
                                                1.0 : {0.0 : {'score_mean': 0.9532142857142857,
                                                              'score_sd'  : 0.03946136777261098},
                                                       0.33: {'score_mean': 0.8769642857142856,
                                                              'score_sd'  : 0.02282301519685199},
                                                       0.67: {'score_mean': 0.5702976190476191,
                                                              'score_sd'  : 0.0536436021760449},
                                                       1.0 : {'score_mean': 0.4998809523809524,
                                                              'score_sd'  : 0.03934051012584167}}}}
                    }

num_of_features_uncompressed = {"Sulfate_reducer": 50973}

num_of_features_compressed = {"Sulfate_reducer": 19029}

num_of_features_selected = {"Sulfate_reducer": 10000}
