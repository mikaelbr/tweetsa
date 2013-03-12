"""
    Sentiment analysis using basic bigrams.
"""
from sklearn.naive_bayes import MultinomialNB

import logging

from base import BaseMethod

class NB(BaseMethod):
    
   def __init__(self, docs_train, y_train, useCrossValidation = False, default_options={}, vect_options={}):
    self.clf = MultinomialNB(**default_options)
    extra = {
      'clf__alpha': (0.1, 0.3, 0.5, 0.7, 0.8, 1.0,),
    }
    super(NB, self).__init__(docs_train, y_train, extra=extra, useCrossValidation=useCrossValidation, vect_options=vect_options)