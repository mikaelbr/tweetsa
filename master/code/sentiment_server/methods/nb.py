"""
    Sentiment analysis using basic bigrams.
"""
from sklearn.naive_bayes import MultinomialNB

import logging

from base import BaseMethod

class NB(BaseMethod):
    
   def __init__(self, docs_train, y_train, useCrossValidation = False):
    self.clf = MultinomialNB()
    extra = {
      'clf__alpha': ( 0.01, 0.1, 0.5, 1.0 )
    }
    super(NB, self).__init__(docs_train, y_train, extra=extra, useCrossValidation=useCrossValidation)