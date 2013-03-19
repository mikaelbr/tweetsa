import sys
import numpy as np

from os import path
import cache
from models import *

import utils.utils as u

"""
    Get data sets. Both train set and test set.
    Default factor for train set is 3/4. 

    E.g. on a set of 2000 entries, 1500 is used for training and 500 for testing. 
"""
train = None
test = None

def set_file_names(train_set = None, test_set = None):
  global train, test
  train_set_filename = (train_set if train_set != None else False) or 'data/tweeti-b.dist.output.tsv'
  test_set_filename = (test_set if test_set != None else False) or 'data/test/twitter-dev-gold-B.tsv'
  cache.set_training_file(train_set_filename)

  if not path.exists(train_set_filename) or not path.exists(test_set_filename): # or not path.exists(test_set_filename):
    raise Exception("File not found")

  train = np.loadtxt(train_set_filename, delimiter='\t', dtype='S', comments=None)
  # train2 = np.loadtxt('data/output_2013-03-07.tsv', delimiter='\t', dtype='S', comments=None)
  # train = np.concatenate((train, train2), axis=0)

  test = np.loadtxt(test_set_filename, delimiter='\t', dtype='S', comments=None)

def get_full_test_set():
  global test
  return test

def get_data():
  global train, test

  test = u.normalize_test_set_classification_scheme(test)
  train = u.normalize_test_set_classification_scheme(train)

  # Normalize data?
  # train = u.reduce_dataset(train, 3000)

  # To compansate for poor TSV data structure
  i_d = 4 if len(test[0]) > 4 else 3
  t_d = 4 if len(train[0]) > 4 else 3

  docs_test, y_test = test[:,i_d], test[:,i_d-1]
  docs_train, y_train = train[:,t_d], train[:,t_d-1]


  docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = u.generate_two_part_dataset(train)
  return docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity