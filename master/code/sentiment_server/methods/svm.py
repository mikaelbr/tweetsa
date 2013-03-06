"""
    Sentiment analysis using basic bigrams.
"""
from sklearn.svm import LinearSVC

import logging

from base import BaseMethod

class SVM(BaseMethod):
    
   def __init__(self, docs_train, y_train, useCrossValidation = False):
    self.clf = LinearSVC()
    extra = {
      'clf__C': ( 0.1, 0.5, 1.0, 1.5, 2.0 )
    }
    super(SVM, self).__init__(docs_train, y_train, extra, useCrossValidation)