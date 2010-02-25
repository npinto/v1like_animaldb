import os
from os import path
from glob import glob
import csv
import scipy as sp
from scipy import io
from scipy import random
from scipy.stats import norm

mypath = path.dirname(path.abspath(__file__))
itype_name_l = ['Head', 'Close-body', 'Medium-body', 'Far-body']
model_l = ['v1like_a', 'v1like_a_plus']



for model in model_l:
    for itype_name in itype_name_l:

        pattern = "output/AnimalDB_%s_split_??.csv.svm_ova_results.%s.mat" % (itype_name, model)
        fname_l = glob(pattern)
        
        hit_rate_l = []
        dprime_l = []

        for fname in fname_l:
            mat = io.loadmat(fname)

            preds = sp.sign(mat['test_distances'])
            gt = mat['svm_labels']

            target_idx = gt>0
            distractor_idx = gt<=0
            
            pred_targets = preds[target_idx]
            pred_distractors = preds[distractor_idx]

            hit_rate = 1.*(pred_targets > 0).sum() / pred_targets.size
            hit_rate_l += [hit_rate]

            falsealarm_rate = 1.*(pred_distractors > 0).sum() / pred_distractors.size
            dprime = norm.ppf(hit_rate) - norm.ppf(falsealarm_rate)
            dprime_l += [dprime]

            print fname, dprime

        hit_rate_a = 100.* sp.array(hit_rate_l)
        dprime_a = 1.* sp.array(dprime_l)
        print "=" * 80
        print "Model: %s, Type: %s" % (model, itype_name)
        print " hit (%%): mean=%.2f, std=%.2f" % (hit_rate_a.mean(), hit_rate_a.std())
        print " d-prime: mean=%.2f, std=%.2f" % (dprime_a.mean(), dprime_a.std())
            
