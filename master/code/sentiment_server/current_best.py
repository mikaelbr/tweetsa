#!/usr/bin/python
import sys
import numpy as np
import logging

from models import *

import utils as u
import stats as s
import tokenizer as t

from storage import data as d
import preprocessor_methods as pr

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = d.get_data()

vect_options = {
  'ngram_range': (1,1),
  'smooth_idf': True,
  'max_df': 0.5,
  'sublinear_tf': True,
  'preprocessor': pr.no_usernames,
  'use_idf': False,
  'stop_words': None
}

default_options = {
  'C': 0.5
}

# Best CLF: <methods.svm.SVM object at 0x9e49fcc>
# Best params: {
#   'vect__ngram_range': (1, 1), 
#   'vect__smooth_idf': True, 
#   'vect__max_df': 0.5, 
#   'vect__sublinear_tf': True, 
#   'vect__preprocessor': <function no_usernames at 0x9e16614>, 
#   'vect__stop_words': None, 
#   'vect__use_idf': False, 
#   'clf__C': 0.5
# }
 


clf = SVM(docs_train, y_train, default_options=default_options, vect_options=vect_options)
# if len(sys.argv) > 1:
#   y_predicted = clf.predict(docs_test)
#   sys.stdout.write("\n".join(y_predicted) + "\n")
# else:
s.test_clf(clf, docs_test, y_test)


# Expected result: 0.646916565901