from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import textwrap
import utils as u
from sklearn.utils.extmath import density
from models import *

headers = ['negative', 'neutral', 'positive']


def clf_report(y_test, y_predicted):
  # Translate classifications to numbers to allow classification_report
  y_test_int = u.translate_to_numbers(y_test)
  y_predicted_int = u.translate_to_numbers(y_predicted)

  return classification_report(y_test_int, y_predicted_int, target_names=headers)


def clf_confusion_matrix(y_test, y_predicted):
  # calc confisuon matrix
  return confusion_matrix(y_test, y_predicted)


def print_stats(best_params, best_score, report=False, confusion=False):
  print "## Best params: %s " % best_params
  print "## Best Score: %s " % best_score

  if report != None:
    print "## Classification Report: "
    print report

  if confusion != None:
    print "## Confusion Matrix: "
    print confusion

def show_most_informative_features(model, num=15):


  if isinstance(model, Boosting) and hasattr(model, 'models'):
    # Is Boosting, contains alot of models:
    for m in model.models:
      show_most_informative_features(m, num)
    return

  if isinstance(model, Combined) and hasattr(model, 'subjectivity_clf'):
    show_most_informative_features_binary(model.subjectivity_clf, num, True)
    show_most_informative_features_binary(model.polarity_clf, num, True)
    return

  steps = model.steps
  clf = steps['clf']


  if hasattr(clf, 'coef_'):
    print "Top Features for Model: %s" % model

    coef = clf.coef_
    print "dimensionality: {}".format(coef.shape[1])
    print "density: {}".format(density(coef))

    print "top %s keywords per class:" % num
    feature_names = np.asarray(steps['vect'].get_feature_names())

    for i, category in enumerate(['negative', 'neutral', 'positive']):
        topkw = np.argsort(coef[i])[-num:]
        keywords = '\n\t'.join(textwrap.wrap(
            ", ".join(feature_names[topkw])
        ))
        print "{}: {}".format(category, keywords)
    print

def show_most_informative_features_binary(model, n=20, binary=False):

  if isinstance(model, Boosting) and hasattr(model, 'models'):
    # Is Boosting, contains alot of models:
    for m in model.models:
      if binary:
        show_most_informative_features_binary(m, n)
      else:
        show_most_informative_features(m, n)
    return

  if isinstance(model, Combined) and hasattr(model, 'subjectivity_clf'):
    show_most_informative_features_binary(model.subjectivity_clf, n, True)
    show_most_informative_features_binary(model.polarity_clf, n, True)
    return

  steps = model.steps 
  vectorizer = steps['vect']
  clf = steps['clf']

  if hasattr(clf, 'coef_'):
    coef = clf.coef_

    print "Informative Features for Model: %s" % model

    print "dimensionality: {}".format(coef.shape[0])
    print "density: {}".format(density(coef))
    co = coef if len(coef) > 1 else coef[0]
    print "top %s keywords per class:" % n
    c_f = sorted(zip(co, vectorizer.get_feature_names()))
    top = zip(c_f[:n], c_f[:-(n+1):-1])
    for (c1,f1),(c2,f2) in top:
        print "\t%.4f\t%-15s\t\t%.4f\t%-15s" % (c1,f1,c2,f2)

def print_best_params(best_clf):
  if hasattr(best_clf, 'grid'):
    print "Best params: %s" % best_clf.best_params

  if isinstance(best_clf, Combined):
    if not isinstance(best_clf.subjectivity_clf, Boosting):
      print "Best params Subj: %s" % best_clf.subjectivity_clf.best_params

    if not isinstance(best_clf.polarity_clf, Boosting):
      print "Best params Pol: %s" % best_clf.polarity_clf.best_params



best_clf = None
best_score = 0.0

def test_clf(clf, docs_test, y_test):
  global best_score, best_clf

  print "######################################################################"
  print "#   Showing for %s" % clf

  print_best_params(clf)
  show_most_informative_features(clf)

  y_predict = clf.predict(docs_test)

  current_score = u.score(y_test, y_predict)
  print 30 * "="
  print "# Total Score: %s " % current_score
  print 30 * "="

  print clf_report(y_test, y_predict)
  print clf_confusion_matrix(y_test, y_predict)

  if current_score >= best_score:
      best_clf = clf
      best_score = current_score

  print "######################################################################"
