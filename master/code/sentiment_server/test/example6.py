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


import filters as f
import preprocess as p
import preprocessor as pr

conv = {
  '"negative"': 0,
  '"objective"': 1,
  '"positive"': 2
}

headers = ['"negative"', '"objective"', '"positive"']

best_algorithm = None
stats_matrix = []
total_best = 0

def translate_to_numbers(li):
  return [conv[v] for v in li]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

train_set_filename = (sys.argv[1] if len(sys.argv) > 1 else False) or 'data/output2'

if not path.exists(train_set_filename): # or not path.exists(test_set_filename):
  raise Exception("File not found")
 
train = np.loadtxt(train_set_filename, delimiter='\t', dtype='S', comments=None)

# Split the dataset in training and test set:
docs_train, docs_test, y_train, y_test = train_test_split(
    train[:,3], train[:,2], test_size=0.4, random_state=0)


def run_gridsearch(clf, extra = {}, useCrossValidation = True):

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
              'tfidf__use_idf': (True, False),
              'tfidf__smooth_idf': (True, False),
              'tfidf__sublinear_tf': (True, False)
            }

  options = dict(options.items() + extra.items())
  cv = StratifiedKFold(y_train, n_folds=10) if useCrossValidation else None

  grid = GridSearchCV(
            pipeline, 
            options,
            cv=cv,
            refit=True,
            n_jobs=-1,
            verbose=1
          )


  print "## Training "
  grid.fit(docs_train, y_train)
  print "## Done training"
  y_predicted = grid.best_estimator_.predict(docs_test)

  # Translate classifications to numbers to allow classification_report
  y_test_int = translate_to_numbers(y_test)
  y_predicted_int = translate_to_numbers(y_predicted)

  # calc f-messure etc.
  report = classification_report(y_test_int, y_predicted_int, target_names=headers)

  # calc confisuon matrix
  confusion = confusion_matrix(y_test, y_predicted)

  return grid.best_params_, grid.best_score_, report, confusion


def print_stats(best_params, best_score, report=False, confusion=False):
  print "## Best params: %s " % best_params
  print "## Best Score: %s " % best_score

  if report != None:
    print report

  if confusion != None:
    print confusion


def run_global_gridsearch(classifications):
  global total_best, best_algorithm

  for c in classifications:
    m = c['clf']
    print "###############################################"
    print "# Initiation %s " % m.__class__.__name__
    print "###############################################\n"
    best_params, best_score, report, confusion = run_gridsearch(m, c['extra'])
    print "# Stats for %s" % m.__class__.__name__
    print_stats(best_params, best_score, report, confusion)

    stats_matrix.append({
      "clf": m,
      "best_score": best_score  
    })


    if best_score >= total_best:
      best_algorithm = m
      total_best = best_score

    print "###############################################"
    print "# Done testing %s " % m.__class__.__name__
    print "###############################################\n"


run_global_gridsearch(
  [
    # {
    #   "clf": MultinomialNB(),
    #   "extra": {
    #     'clf__alpha': ( 0.01, 0.1, 0.5, 1.0 )
    #   }
    # },
    {
      "clf": LogisticRegression(),
      "extra": {
        # 'clf__C': ( 0.1, 0.5, 1.0, 1.5, 2.0),
        # 'clf__dual': (True, False),
        'clf__penalty': ('l1', 'l2')
      }
    },
    {
      "clf": LinearSVC(),
      "extra": {
        # 'clf__C': ( 0.1, 0.5, 1.0, 1.5, 2.0 )
      }
    }
  ])

print "###############################################"
print "# Finished Stats:"
print stats_matrix
print "###############################################"


print "###############################################"
print "# Best algorithm %s, with best score of %s #" % (best_algorithm.__class__.__name__, total_best)
print "###############################################"

