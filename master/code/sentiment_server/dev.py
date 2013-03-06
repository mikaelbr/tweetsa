#!/usr/bin/python
import sys
import numpy as np
import logging

from os import path

from trainer import cache

from methods import *

import utils as u

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

train_set_filename = (sys.argv[1] if len(sys.argv) > 1 else False) or 'data/output2'
# train_set_filename = (sys.argv[1] if len(sys.argv) > 1 else False) or 'data/train/output_tweets.tsv'
test_set_filename = (sys.argv[0] if len(sys.argv) > 1 else False) or 'data/test/test_output_tweets.tsv'

if not path.exists(train_set_filename) or not path.exists(test_set_filename): # or not path.exists(test_set_filename):
  raise Exception("File not found")


cache.set_training_file(train_set_filename)

train = np.loadtxt(train_set_filename, delimiter='\t', dtype='S', comments=None)
test = np.loadtxt(test_set_filename, delimiter='\t', dtype='S', comments=None)

test = u.normalize_test_set_classification_scheme(test)
docs_test, y_test = test[:,4], test[:,3]


# docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = u.generate_two_part_dataset(train)
# c1 = SVM(docs_train_subjectivity, y_train_subjectivity)
# c2 = NB(docs_train_polarity, y_train_polarity)
# clf = Combined(c1, c2)

train = u.normalize_test_set_classification_scheme(train)
docs_train, y_train = train[:,3], train[:,2]
clf = MaxEnt(docs_train, y_train, useCrossValidation=True)


# Example for boosting:
# train = u.normalize_test_set_classification_scheme(train)
# docs_train, y_train = train[:,3], train[:,2]
# docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = u.generate_two_part_dataset(train)
# clf = Boosting(docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity)

# y_predict = clf.predict(docs_test)

# print "Total Score Boosting: %s " % u.score(y_test, y_predict)

# print u.clf_report(y_test, y_predict)
# print u.clf_confusion_matrix(y_test, y_predict)

# print "....-----------------------------------....."

# c1 = SVM(docs_train_subjectivity, y_train_subjectivity)
# c2 = NB(docs_train_polarity, y_train_polarity)
# clf = Combined(c1, c2)

y_predict = clf.predict(docs_test)

print "Total Score TwoPart: %s " % u.score(y_test, y_predict)

print u.clf_report(y_test, y_predict)
print u.clf_confusion_matrix(y_test, y_predict)
