#!/usr/bin/python
import sys
import logging

from models import *

import storage.data as d
import storage.prediction_exporter as pe

import utils.stats as s
import utils.preprocessor_methods as pr



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = d.get_data()
pe.set_base_from_dataset(d.get_full_test_set())


# docs_train, y_train, docs_train_subjectivity=None, y_train_subjectivity=None, docs_train_polarity=None, y_train_polarity=None):

clf = Boosting(docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity)

if len(sys.argv) > 1:
  y_predicted = clf.predict(docs_test)
  sys.stdout.write(pe.predictions_as_str(y_predicted))
else:
  s.test_clf(clf, docs_test, y_test)
