import os
from os import path
from glob import glob
import csv
import scipy as sp
from scipy import random

mypath = path.dirname(path.abspath(__file__))
random.seed(1)
itype_l = ['H', 'B', 'M', 'F']
itype_name_l = ['Head', 'Close-body', 'Medium-body', 'Far-body']
ntrials = 20
nsamples = 75

target_l = glob(path.join(mypath, "Targets/*.jpg"))
distractor_l = glob(path.join(mypath, "Distractors/*.jpg"))


target_d = dict(zip(itype_l,
                    [[elt for elt in target_l
                      if path.split(elt)[-1].startswith(itype)
                      ]
                     for itype in itype_l
                     ]
                    )
                )

distractor_d = dict(zip(itype_l,
                        [[elt for elt in distractor_l
                          if path.split(elt)[-1].startswith(itype)
                          ]
                         for itype in itype_l
                         ]
                        )
                    )


output_dir = path.join(mypath, "splits_csv")
if not path.exists(output_dir):
    os.makedirs(output_dir)

for n in xrange(ntrials):
    
    for name, (tk, tv), (dk, dv) in zip(itype_name_l,
                                        target_d.iteritems(),
                                        distractor_d.iteritems()):

        assert tk == dk

        random.shuffle(tv)
        random.shuffle(dv)

        train_pos_l = [(elt, '+1', 'train') for elt in tv[:len(tv)/2]]
        assert len(train_pos_l) == nsamples
        train_neg_l = [(elt, '-1', 'train') for elt in dv[:len(tv)/2]]
        assert len(train_neg_l) == nsamples

        test_pos_l = [(elt, '+1', 'test') for elt in tv[len(tv)/2:]]
        assert len(test_pos_l) == nsamples
        test_neg_l = [(elt, '-1', 'test') for elt in dv[len(tv)/2:]]
        assert len(test_neg_l) == nsamples


        traintest_l = train_pos_l + train_neg_l \
                      + test_pos_l + test_neg_l

        assert len(traintest_l) == len(target_d)*nsamples

        out_fname = path.join(mypath, "splits_csv",
                              "AnimalDB_%s_split_%02d.csv" % (name, n+1))
        print "Writing", out_fname
        fout = open(out_fname, "w+")
        csvw = csv.writer(fout)
        csvw.writerows(traintest_l)
        fout.close()
        
        
