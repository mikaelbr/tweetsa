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
import numpy as np

class Boosting(BaseMethod):
    
  def __init__(self, docs_train, y_train, docs_train_subjectivity=None, y_train_subjectivity=None, docs_train_polarity=None, y_train_polarity=None):
    nb = NB
    svm = SVM
    maxent = MaxEnt

    self.baseModels = [nb, svm, maxent]

    self.models = [ 
      nb(docs_train, y_train),
      svm(docs_train, y_train),
      maxent(docs_train, y_train) 
    ]

    if docs_train_subjectivity != None:
      self.combination_permutation(docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity)

    self.set_best_score()


  def combination_permutation(self, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity):
    perms = permutations(self.baseModels, 2)
    for cmb in perms:
      c1 = cmb[0](docs_train_subjectivity, y_train_subjectivity)
      c2 = cmb[1](docs_train_polarity, y_train_polarity)
      self.models.append(Combined(c1, c2))


  def set_best_score(self):
    self.best_score = np.mean(map(lambda x: x.best_score, self.models))


  def train(self):
    pass

  def pick_majoraty(self, y_pred):
    clfs = {}
    for i, m in zip(y_pred, self.models):
      # mavg = m.best_score / len(self.models)
      mavg = m.best_score
      clfs[i] = clfs[i] + mavg  if i in clfs else mavg

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
    for m in self.models:
      y_pred.append(m.predict(arg_input))

    pred = self.pick_majoraty(y_pred)
    return pred

