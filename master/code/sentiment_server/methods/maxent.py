"""
    Sentiment analysis using basic bigrams.
"""
from sklearn.linear_model import LogisticRegression 

import logging

from base import BaseMethod

class MaxEnt(BaseMethod):
    
   def __init__(self, docs_train, y_train, useCrossValidation = False):
    self.clf = LogisticRegression()
    extra = {
      'clf__C': ( 0.1 , 0.5, 1.0, 1.5, 2.0),
      'clf__penalty': ('l1', 'l2')
    }
    super(MaxEnt, self).__init__(docs_train, y_train, extra, useCrossValidation)