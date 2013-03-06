#!/usr/bin/python
import sys
import numpy as np
import logging

from os import path
from sklearn import decomposition, linear_model
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

import filters as f
import preprocess as p
import preprocessor as pr

conv = {
  '"negative"': 0,
  '"objective"': 1,
  '"positive"': 2
}

headers = ['"negative"', '"objective"', '"positive"']

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

vect = CountVectorizer(charset_error='ignore')
pipeline = Pipeline([
    ('vect', vect),
    ('tfidf', TfidfTransformer()),
    # ('clf', MultinomialNB()),
    ('clf', LinearSVC()),
])

grid = GridSearchCV(
          pipeline, 
          {
            'vect__ngram_range': ((1, 1), (2, 2), (3,3)),
            'vect__stop_words': ('english', None),
            'vect__preprocessor': (None, pr.no_prep, pr.no_usernames, pr.remove_noise, pr.placeholders, pr.all, pr.remove_all, pr.method1, pr.method2),
            'tfidf__use_idf': (True, False),
            'tfidf__smooth_idf': (True, False),
            'tfidf__sublinear_tf': (True, False),
            # 'clf__alpha': ( 0, 0.1, 0.5, 1.0 ),
            'clf__C': ( 0.1, 0.5, 1.0, 1.5, 2.0 ),
          },
          cv=StratifiedKFold(y_train, n_folds=10),
          refit=True,
          n_jobs=-1,
          verbose=1
        )

print "Training "
grid.fit(docs_train, y_train)

print "Done training"

print "\nBest Params:"
print grid.best_params_



y_predicted = grid.best_estimator_.predict(docs_test)
 
# Translate classifications to numbers to allow classification_report
y_test_int = translate_to_numbers(y_test)
y_predicted_int = translate_to_numbers(y_predicted)

print "\nClassification Report:"
print classification_report(y_test_int, y_predicted_int, target_names=headers)

# Plot the confusion matrix
print "\nConfusion matrix: "
print confusion_matrix(y_test, y_predicted)

print "\nBest score: %s" % grid.best_score_

print "\nCalculated acc, np.mean(y_predicted == y_test): %s" % np.mean(y_predicted == y_test)
print "Accuracy Score, grid.score(docs_test, y_test): %.2f" % grid.score(docs_test, y_test)
