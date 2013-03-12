#!/usr/bin/python
import sys
import numpy as np
import logging

from models import *

import utils as u
import stats as s

from storage import data as d

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = d.get_data()

# clf = Boosting(docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity)
# s.test_clf(clf, docs_test, y_test)

# indevidual_models = clf.models
# for i in indevidual_models:
#   s.test_clf(i, docs_test, y_test)

c1 = Boosting(docs_train_subjectivity, y_train_subjectivity)
c2 = Boosting(docs_train_polarity, y_train_polarity)
clf = Combined(c1, c2)

s.test_clf(clf, docs_test, y_test)

print "Best CLF: %s" % s.best_clf
s.print_best_params(s.best_clf)
print "Score of best CLF: %s" % s.best_score