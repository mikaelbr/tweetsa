"""
    Sentiment analysis using basic bigrams.
"""
import logging

from base import BaseMethod

class Combined(BaseMethod):
    
  def __init__(self, m1, m2):
    self.subjectivity_clf = m1
    self.polarity_clf = m2

    self.best_score = (self.subjectivity_clf.best_score + self.polarity_clf.best_score) / 2

  def train(self, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity):
    print docs_train_subjectivity[:3]
    print y_train_subjectivity[:3]
    self.subjectivity_clf.train(docs_train_subjectivity, y_train_subjectivity)
    self.polarity_clf.train(docs_train_polarity, y_train_polarity)

    self.best_score = (self.subjectivity_clf.best_score + self.polarity_clf.best_score) / 2

  def predict_list(self, li):
    y_predicted = []
    for i in li:
      y_predicted.append(self.predict(i))
    return y_predicted

  def predict(self, arg_input):
    if not isinstance(arg_input, basestring):
      return self.predict_list(arg_input)

    p1 = self.subjectivity_clf.predict(arg_input)
    if p1 == '"neutral"':
      return '"neutral"'

    return self.polarity_clf.predict(arg_input)
