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

vect_options = {
  'ngram_range': (1,1),
  'smooth_idf': True,
  'max_df': 0.5,
  'sublinear_tf': True,
  'preprocessor': pr.remove_noise,
  'use_idf': False,
  'stop_words': None
}

default_options = {
  'C': 1.0
}

clf = SVM(docs_train, y_train, default_options=default_options, vect_options=vect_options)
if len(sys.argv) > 1:
  y_predicted = clf.predict(docs_test)
  sys.stdout.write(pe.predictions_as_str(y_predicted))
else:
  s.test_clf(clf, docs_test, y_test)
