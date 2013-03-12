"""
    Base class for different methods of using sentiment analysis.
"""
import logging
import sys
import textwrap
import numpy as np
from sklearn.utils.extmath import density

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.grid_search import GridSearchCV

import preprocessor_methods as pr

from trainer import cache


class BaseMethod(object):

  def __init__(self, docs_train, y_train, extra = {}, useCrossValidation = False, vect_options = {}):

    if sys.flags.debug:
        self.options = {}
    else: 
        self.options = {
                'vect__ngram_range': [(1, 1), (2, 2), (3,3)],
                'vect__stop_words': ('english', None),
                'vect__preprocessor': (None, pr.no_prep, pr.no_usernames, pr.remove_noise, pr.placeholders, pr.all, pr.remove_all, pr.reduced_attached, pr.no_url_usernames_reduced_attached),
                'vect__use_idf': (True, False),
                'vect__max_df': (0.5,),
                'vect__smooth_idf': (True, False),
                'vect__sublinear_tf': (True, False)
              }

    self.train(docs_train, y_train, extra, useCrossValidation, vect_options)


  def train(self, docs_train, y_train, extra = {}, useCrossValidation = False, vect_options={}):

    options = dict(self.options.items() + extra.items())
    cv = StratifiedKFold(y_train, n_folds=10) if useCrossValidation else None

    pipeline = Pipeline([
        ('vect', TfidfVectorizer(charset_error='ignore', **vect_options)),
        ('clf', self.clf),
    ])

    useGrid = sys.flags.optimize

    if useGrid:
        self.grid = GridSearchCV(
                pipeline, 
                options,
                cv=cv,
                refit=True,
                n_jobs=-1,
                verbose=sys.flags.verbose
              )
    else:
        self.grid = pipeline

    cache_key = str(self.grid) + str(docs_train)

    cached = cache.get(cache_key)
    
    if cached and not(sys.flags.debug): 
        logging.debug("# Fetched cached version of %s " % self.clf.__class__.__name__)
        self.best_estimator = cached['est']
        self.best_score = cached['scr']
        self.best_params = cached['parm']

    else:
        logging.debug("# Training new instance of %s " % self.clf.__class__.__name__)

        self.grid.fit(docs_train, y_train)

        

        if useGrid:
            self.best_estimator = self.grid.best_estimator_
            self.best_params = self.grid.best_params_
            self.best_score = self.grid.best_score_
        else:
            self.best_estimator = self.grid
            self.best_params = self.grid.get_params(False)
            self.best_score = 1


        logging.debug("Saving to cache for %s " % self.clf.__class__.__name__)
        cache.save(cache_key, {
            "est": self.best_estimator,
            "scr": self.best_score,
            "parm": self.best_params
          })

    self.steps = self.best_estimator.named_steps

    

    logging.debug("# Best params for  %s :" % self.clf.__class__.__name__)
    logging.debug(self.best_params)

    logging.debug("# Best score for  %s :" % self.clf.__class__.__name__)
    logging.debug(self.best_score)

    return self.grid

  def predict(self, arg_input):
    orig = arg_input
    if isinstance(arg_input, basestring):
        orig = [orig]

    predictions = self.best_estimator.predict(orig)
    if isinstance(arg_input, basestring):
      return predictions[0]

    return predictions

