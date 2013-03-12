#!/usr/bin/python
import sys
import numpy as np
import logging

from os import path
from sklearn import decomposition, linear_model
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.linear_model import LogisticRegression 
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from itertools import permutations

import filters as f
import preprocess as p
import preprocessor_methods as pr

conv = {
  'negative': 0,
  'neutral': 1,
  'positive': 2
}

headers = ['negative', 'neutral', 'positive']

best_algorithm = None
total_best = 0

def translate_to_numbers(li):
  return [conv[v] for v in li]

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

train_set_filename = (sys.argv[1] if len(sys.argv) > 1 else False) or 'data/tweeti-b.dist.output.tsv'
test_set_filename = (sys.argv[0] if len(sys.argv) > 1 else False) or 'data/test/twitter-dev-gold-B.tsv'

if not path.exists(train_set_filename) or not path.exists(test_set_filename): # or not path.exists(test_set_filename):
  raise Exception("File not found")
 

def generate_subjective_set(dataset):
  label_i = 3 if len(dataset[0]) > 4 else 2 
  
  new_set = []
  for i in np.array(dataset, copy=True):
    if i[label_i] == 'objective' or i[label_i] == 'objective-OR-neutral':
      i[label_i] = 'neutral'
    if i[label_i] != 'neutral':
      i[label_i] = 'subjective'
    new_set.append(i)
  return new_set


def generate_polarity_set(dataset):
  label_i = 3 if len(dataset[0]) > 4 else 2 

  new_set = []
  for i in np.array(dataset, copy=True):
    if i[label_i] != 'objective' and i[label_i] != 'neutral' and i[label_i] != 'objective-OR-neutral':
      new_set.append(i)
  return new_set


def normalize_test_set_classification_scheme(dataset):
  label_i = 3 if len(dataset[0]) > 4 else 2 

  for i in dataset:
    i[label_i] = i[label_i].replace('"', '')
    if i[label_i] == 'objective' or i[label_i] == 'objective-OR-neutral':
      i[label_i] = 'neutral' 
  return dataset


train = np.loadtxt(train_set_filename, delimiter='\t', dtype='S', comments=None)
test = np.loadtxt(test_set_filename, delimiter='\t', dtype='S', comments=None)
train = normalize_test_set_classification_scheme(train)

subjectivity = np.array(generate_subjective_set(train))
polarity = np.array(generate_polarity_set(train))

docs_train_subjectivity = subjectivity[:,3]
y_train_subjectivity = subjectivity[:,2]

docs_train_polarity = polarity[:,3]
y_train_polarity = polarity[:,2]

test = normalize_test_set_classification_scheme(test)
docs_test = test[:,3]
y_test = test[:,2]

cache1 = {};
cache2 = {};

def run_gridsearch(clf, docs_train, y_train, extra = {}, useCrossValidation = True):

  vect = CountVectorizer(charset_error='ignore')
  pipeline = Pipeline([
      ('vect', vect),
      ('tfidf', TfidfTransformer()),
      ('clf', clf),
  ])

  options = {
              # 'vect__ngram_range': ((1, 1), (2, 2), (3,3)),
              # 'vect__stop_words': ('english', None),
              # 'vect__preprocessor': (None, pr.no_prep, pr.no_usernames, pr.remove_noise, pr.placeholders, pr.all, pr.remove_all, pr.method1, pr.method2),
              # 'tfidf__use_idf': (True, False),
              # 'tfidf__smooth_idf': (True, False),
              'tfidf__sublinear_tf': (True, False)
            }

  options = dict(options.items() + extra.items())
  cv = StratifiedKFold(y_train, n_folds=10) if useCrossValidation else None

  grid = GridSearchCV(
            pipeline, 
            options,
            # cv=cv,
            # refit=True,
            n_jobs=-1,
            verbose=1
          )


  print "## Training "
  grid.fit(docs_train, y_train)

  return grid


def print_stats(best_params, best_score, report=False, confusion=False):
  print "## Best params: %s " % best_params
  print "## Best Score: %s " % best_score

  if report != None:
    print report

  if confusion != None:
    print confusion


def predict(g1, g2, test_set):
  y_predicted = []
  for i in test_set:

    p1 = g1.best_estimator_.predict([i])[0];
    if p1 == 'neutral':
      y_predicted.append('neutral')
      continue

    y_predicted.append(g2.best_estimator_.predict([i])[0])

  return y_predicted

def run_global_gridsearch(classifications):
  global total_best, best_algorithm

  for c in classifications:
    m1, m2 = c[0]['clf'], c[1]['clf']
    m1name = m1.__class__.__name__
    m2name = m2.__class__.__name__
    e1, e2 = c[0]['extra'], c[1]['extra']

    print "Now testing: (%s -> %s)" % (m1.__class__.__name__, m2.__class__.__name__)

    g1 = cache1[m1name] if m1name in cache1 else run_gridsearch(m1, docs_train_subjectivity, y_train_subjectivity, extra=e1)
    g2 = cache2[m2name] if m2name in cache2 else run_gridsearch(m2, docs_train_polarity, y_train_polarity, extra=e2)

    cache1[m1name] = g1
    cache2[m2name] = g2

    y_predicted = predict(g1, g2, docs_test)

    print "Best params for Subjectivity Classification With %s : --- " % m1.__class__.__name__
    print g1.best_params_

    print "Best params for Polarity Classification With %s : --- " % m2.__class__.__name__
    print g2.best_params_

    
    print "Best score for Subjectivity Classification With %s : --- " % m1.__class__.__name__
    print g1.best_score_

    print "Best score for Polarity Classification With %s : --- " % m2.__class__.__name__
    print g2.best_score_


    # Translate classifications to numbers to allow classification_report
    y_test_int = translate_to_numbers(y_test)
    y_predicted_int = translate_to_numbers(y_predicted)

    # calc f-messure etc.
    report = classification_report(y_test_int, y_predicted_int, target_names=headers)

    # calc confisuon matrix
    confusion = confusion_matrix(y_test, y_predicted)

    print "--- Total Report: ----"
    print report

    print "--- Total Confusion Matrix: ----"
    print confusion

    best_score = np.mean(y_predicted == y_test)

    print "--- Total Score: ----"
    print best_score

    if best_score >= total_best:
      best_algorithm = "(%s -> %s)" % (m1.__class__.__name__, m2.__class__.__name__)
      total_best = best_score

    print "###############################################"
    print "# Done testing %s -> %s " % (m1.__class__.__name__, m2.__class__.__name__)
    print "###############################################\n"


algos = [
    {
      "clf": MultinomialNB(),
      "extra": {
        'clf__alpha': ( 0.01, 0.1, 0.5, 1.0 )
      }
    },
    {
      "clf": LogisticRegression(),
      "extra": {
        'clf__C': ( 0.1, 0.5, 1.0, 1.5, 2.0),
        'clf__penalty': ('l1', 'l2')
      }
    },
    {
      "clf": LinearSVC(),
      "extra": {
        'clf__C': ( 0.1, 0.5, 1.0, 1.5, 2.0 )
      }
    }
  ]

def print_permutations(perms):
  for i in perms:
    for m in i:
      print m['clf'].__class__.__name__

  print "-----"

perms = permutations(algos, 2)


run_global_gridsearch(perms)

print "######## TOTAL BEST ##############"
print total_best

print "###### BEST ALGORITHM PERMUTATION #######"
print best_algorithm
