"""
    Base class for different methods of using sentiment analysis.
"""
import logging
import sys

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.grid_search import GridSearchCV

import preprocessor_methods as pr

from trainer import cache


class BaseMethod(object):

  def __init__(self, docs_train, y_train, extra = {}, useCrossValidation = False):

    if sys.flags.debug:
        self.options = {}
    else: 
        self.options = {
                'vect__ngram_range': ((1, 1), (2, 2), (3,3)),
                'vect__stop_words': ('english', None),
                'vect__preprocessor': (None, pr.no_prep, pr.no_usernames, pr.remove_noise, pr.placeholders, pr.all, pr.remove_all, pr.reduced_attached, pr.no_url_usernames_reduced_attached),
                'tfidf__use_idf': (True, False),
                'tfidf__smooth_idf': (True, False),
                'tfidf__sublinear_tf': (True, False)
              }

    self.train(docs_train, y_train, extra, useCrossValidation)


  def train(self, docs_train, y_train, extra = {}, useCrossValidation = False):
    options = dict(self.options.items() + extra.items())
    cv = StratifiedKFold(y_train, n_folds=10) if useCrossValidation else None

    self.vect = CountVectorizer(charset_error='ignore')
    self.tfidf = TfidfTransformer()
    pipeline = Pipeline([
        ('vect', self.vect),
        ('tfidf', self.tfidf),
        ('clf', self.clf),
    ])

    self.grid = GridSearchCV(
            pipeline, 
            options,
            cv=cv,
            refit=True,
            n_jobs=-1,
            verbose=1
          )

    cached = cache.get(self.grid)
    if cached: 
        logging.debug("# Fetched cached version of %s " % self.clf.__class__.__name__)
        self.grid = cached
        return self.grid

    logging.debug("# Training new instance of %s " % self.clf.__class__.__name__)
    self.grid.fit(docs_train, y_train)

    logging.debug("Saving to cache for %s " % self.clf.__class__.__name__)
    cache.save(self.grid, self.grid)

    logging.debug("# Best params for  %s :" % self.clf.__class__.__name__)
    logging.debug(self.grid.best_params_)

    logging.debug("# Best score for  %s :" % self.clf.__class__.__name__)
    logging.debug(self.grid.best_score_)

    return self.grid

  def predict(self, arg_input):
    orig = arg_input
    if isinstance(arg_input, basestring):
        orig = [orig]

    predictions = self.grid.best_estimator_.predict(orig)
    if isinstance(arg_input, basestring):
      return predictions[0]

    return predictions

