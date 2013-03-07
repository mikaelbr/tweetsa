"""
    Sentiment analysis using basic bigrams.
"""
import logging

from base import BaseMethod
from numpy import mean
from utils import translate_to_numbers, translate_from_number
from methods import *
from itertools import permutations
from random import choice

class Boosting(BaseMethod):
    
  def __init__(self, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity):
    nb = NB
    svm = SVM
    maxent = MaxEnt

    self.baseMethods = [nb, svm, maxent]

    self.methods = [ 
      nb(docs_train, y_train),
      svm(docs_train, y_train),
      maxent(docs_train, y_train) 
    ]

    self.combination_permutation(docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity)

  def combination_permutation(self, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity):
    perms = permutations(self.baseMethods, 2)
    for cmb in perms:
      c1 = cmb[0](docs_train_subjectivity, y_train_subjectivity)
      c2 = cmb[1](docs_train_polarity, y_train_polarity)
      self.methods.append(Combined(c1, c2))


  def train(self):
    pass

  def pick_majoraty(self, y_pred):
    clfs = {}
    for i, m in zip(y_pred, self.methods):
      # mavg = m.best_score / len(self.methods)
      mavg = m.best_score
      clfs[i] = clfs[i] + mavg  if i in clfs else mavg

    logging.debug("CLFS: %s" % clfs)
    highest_val = max(clfs.values())
    highest = filter(lambda t: t[1] == highest_val, clfs.items())
    return choice(highest)[0]

  def predict_list(self, li):
    y_predictions = []
    for i in li:
      prediction = self.predict(i)
      y_predictions.append(prediction)

    return y_predictions

  def predict(self, arg_input):
    
    if not isinstance(arg_input, basestring):
      return self.predict_list(arg_input)

    y_pred = []
    for m in self.methods:
      y_pred.append(m.predict(arg_input))

    pred = self.pick_majoraty(y_pred)
    logging.debug("Pred: %s" % pred)
    return pred

