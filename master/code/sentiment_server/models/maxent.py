"""
    Sentiment analysis using basic bigrams.
"""
from sklearn.linear_model import LogisticRegression 

import logging

from base import BaseMethod

class MaxEnt(BaseMethod):
    
   def __init__(self, docs_train, y_train, useCrossValidation = False, default_options={}, vect_options={}):
    self.clf = LogisticRegression(**default_options)
    extra = {
      'clf__C': (0.1, 0.3, 0.5, 0.7, 0.8, 1.0,),
      'clf__penalty': ('l1', 'l2')
    }
    super(MaxEnt, self).__init__(docs_train, y_train, extra, useCrossValidation, vect_options=vect_options)