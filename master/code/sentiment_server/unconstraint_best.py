#!/usr/bin/python

"""
Now testing: (LogisticRegression -> LinearSVC)
Best params for Subjectivity Classification With LogisticRegression : ---
{'tfidf__smooth_idf': False, 'tfidf__sublinear_tf': False, 'vect__preprocessor': None, 'tfidf__use_idf': True, 'clf__penalty': 'l1', 'clf__C': 1.0}
Best params for Polarity Classification With LinearSVC : ---
{'tfidf__use_idf': True, 'tfidf__smooth_idf': True, 'vect__preprocessor': <function no_usernames at 0x971117c>, 'clf__C': 1.0, 'tfidf__sublinear_tf': True}

0.645102781137
"""

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


# {
#   'tfidf__smooth_idf': False, 
#   'tfidf__sublinear_tf': False, 
#   'vect__preprocessor': None, 
#   'tfidf__use_idf': True, 
#   'clf__penalty': 'l1', 
#   'clf__C': 1.0
# }
# 

# {
#   'tfidf__use_idf': True, 
#   'tfidf__smooth_idf': True, 
#   'vect__preprocessor': <function no_usernames at 0x971117c>, 
#   'clf__C': 1.0, 
#   'tfidf__sublinear_tf': True
#   }


c1_vect_options = {
  'ngram_range': (1,1),
  'sublinear_tf': False,
  'preprocessor': None, # pr.remove_noise,
  'use_idf': True,
  'smooth_idf': False,
  'stop_words': None
}

c2_vect_options = {
  'ngram_range': (1,1),
  'sublinear_tf': True,
  'smooth_idf': True,
  'preprocessor': pr.no_usernames,
  'use_idf': True,
  'stop_words': None
}

c1_default_options = {
  'penalty': 'l1',
  'C': 1.0
}

c2_default_options = {
  'C': 1.0
}


c1 = MaxEnt(docs_train_subjectivity, y_train_subjectivity, default_options=c1_default_options, vect_options=c1_vect_options)
c2 = SVM(docs_train_polarity, y_train_polarity, default_options=c2_default_options, vect_options=c2_vect_options)
clf = Combined(c1, c2)

if len(sys.argv) > 1:
  y_predicted = clf.predict(docs_test)
  sys.stdout.write(pe.predictions_as_str(y_predicted))
else:
  s.test_clf(clf, docs_test, y_test)
