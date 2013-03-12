import sys
import numpy as np

from os import path
import cache
from models import *

import utils as u

"""
    Get data sets. Both train set and test set.
    Default factor for train set is 3/4. 

    E.g. on a set of 2000 entries, 1500 is used for training and 500 for testing. 
"""

def get_data():
  train_set_filename = (sys.argv[2] if len(sys.argv) > 2 else False) or 'data/tweeti-b.dist.output.tsv'
  test_set_filename = (sys.argv[1] if len(sys.argv) > 1 else False) or 'data/test/twitter-dev-gold-B.tsv'

  if not path.exists(train_set_filename) or not path.exists(test_set_filename): # or not path.exists(test_set_filename):
    raise Exception("File not found")

  cache.set_training_file(train_set_filename)

  train = np.loadtxt(train_set_filename, delimiter='\t', dtype='S', comments=None)
  test = np.loadtxt(test_set_filename, delimiter='\t', dtype='S', comments=None)

  test = u.normalize_test_set_classification_scheme(test)
  train = u.normalize_test_set_classification_scheme(train)

  # Normalize data?
  # train = u.reduce_dataset(train, 3000)
  # test = u.reduce_dataset(test, 300)

  # To compansate for poor TSV data structure
  i_d = 4 if len(test[0]) > 4 else 3
  t_d = 4 if len(train[0]) > 4 else 3

  docs_test, y_test = test[:,i_d], test[:,i_d-1]
  docs_train, y_train = train[:,t_d], train[:,t_d-1]


  docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = u.generate_two_part_dataset(train)
  return docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity