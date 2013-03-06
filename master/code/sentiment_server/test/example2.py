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
  '"neutral"': 1,
  '"objective"': 2,
  '"objective-OR-neutral"': 3,
  '"positive"': 4
}

headers = [ '"negative"', '"neutral"', '"objective"', '"objective-OR-neutral"', '"positive"' ]

def translate_to_numbers(li):
  return [conv[v] for v in li]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

train_set_filename = (sys.argv[1] if len(sys.argv) > 1 else False) or 'data/train/output_tweets.tsv'
test_set_filename = (sys.argv[2] if len(sys.argv) > 2 else False) or 'data/test/test_output_tweets.tsv'

if not path.exists(train_set_filename) or not path.exists(test_set_filename):
  raise Exception("File not found")
 
train = np.loadtxt(train_set_filename, delimiter='\t', dtype='S', comments=None)
test = np.loadtxt(test_set_filename, delimiter='\t', dtype='S', comments=None)


filtered_from_empty = []
for x in train:
  if x[4].lower() != "not available":
    filtered_from_empty.append(x)

train = np.array(filtered_from_empty)

# Split the dataset in training and test set:
# docs_train, docs_test, y_train, y_test = train_test_split(
#     train[:,4], train[:,3], test_size=0.5, random_state=0)

docs_train = train[:,4]
y_train = train[:,3]

docs_test = test[:,4]
y_test = test[:,3]

vect = CountVectorizer(charset_error='ignore')
pipeline = Pipeline([
    ('vect', vect),
    ('tfidf', TfidfTransformer()),
    ('clf', LinearSVC()),
])

cv = StratifiedKFold(y_train, n_folds=5)

grid = GridSearchCV(
          pipeline, 
          {
            # 'vect__ngram_range': ((1, 1), (2, 2), (3,3)),
            # 'vect__ngram_range': ((1, 1), (2, 2)),
            # 'vect__stop_words': ('english', None),
            # 'vect__preprocessor': (None, pr.no_usernames, pr.remove_noise, pr.placeholders, pr.all),
            # 'vect__preprocessor': (None, pr.no_usernames, pr.all),
            'tfidf__use_idf': (True, False),
            # 'tfidf__smooth_idf': (True, False),
            # 'tfidf__sublinear_tf': (True, False),
            # 'clf__alpha': tuple( np.arange(0, 1.0, 0.1) ),
            # 'clf__C': ( 100, ),
          },
          # cv=cv,
          refit=True,
          n_jobs=-1,
          verbose=1
        )

print "Training "
grid.fit(docs_train, y_train)
# grid.fit(train[:,4], train[:,3])
print "Done training"

print "\nBest Params:"
print grid.best_params_

y_predicted = grid.best_estimator_.predict(docs_test)
# y_predicted = grid.best_estimator_.predict(test[:,4])
# 
# Translate classifications to numbers to allow classification_report
y_test_int = translate_to_numbers(y_test)
y_predicted_int = translate_to_numbers(y_predicted)

# print classification_report(y_test, y_predicted, labels=None, target_names=None)
print "\nClassification Report:"
print classification_report(y_test_int, y_predicted_int, target_names=headers)

# Plot the confusion matrix
print "\nConfusion matrix: "
print confusion_matrix(y_test_int, y_predicted_int)

print "\nBest score: %s" % grid.best_score_

# # Predict the result on some short new sentences:
# y_predicted = grid.best_estimator_.predict(test[:,4])
# print y_predicted[:30]
# print y_test[:30]
print "\nCalculated acc, np.mean(y_predicted == y_test): %s" % np.mean(y_predicted == y_test)
print "Accuracy Score, grid.score(docs_test, y_test): %.2f" % grid.score(docs_test, y_test)
