import numpy as np
from sklearn.metrics import classification_report, confusion_matrix


def generate_subjective_set(dataset):
  label_i = 3 if len(dataset[0]) > 4 else 2 
  
  new_set = []
  for i in np.array(dataset, copy=True):
    if i[label_i] == '"objective"' or i[label_i] == '"objective-OR-neutral"':
      i[label_i] = '"neutral"'
    if i[label_i] != '"neutral"':
      i[label_i] = '"subjective"'
    new_set.append(i)
  return new_set


def generate_polarity_set(dataset):
  label_i = 3 if len(dataset[0]) > 4 else 2 

  new_set = []
  for i in np.array(dataset, copy=True):
    if i[label_i] != '"objective"' and i[label_i] != '"neutral"' and i[label_i] != '"objective-OR-neutral"':
      new_set.append(i)
  return new_set


def normalize_test_set_classification_scheme(dataset):
  label_i = 3 if len(dataset[0]) > 4 else 2 

  for i in dataset:
    if i[label_i] == '"objective"' or i[label_i] == '"objective-OR-neutral"':
      i[label_i] = '"neutral"' 
  return dataset

def generate_two_part_dataset(train):
  label_i = 3 if len(train[0]) > 4 else 2
  text_i = 4 if len(train[0]) > 4 else 3

  subjectivity = np.array(generate_subjective_set(train))
  polarity = np.array(generate_polarity_set(train))

  docs_train_subjectivity = subjectivity[:,text_i]
  y_train_subjectivity = subjectivity[:,label_i]

  docs_train_polarity = polarity[:,text_i]
  y_train_polarity = polarity[:,label_i]

  return docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity


conv = {
  '"negative"': 0,
  '"neutral"': 1,
  '"positive"': 2
}

headers = ['"negative"', '"neutral"', '"positive"']

def translate_to_numbers(li):
  return [conv[v] for v in li]

def translate_from_number(num):
  mapping = dict (zip(conv.values(), conv.keys()))
  return mapping[int(round(num))]

def clf_report(y_test, y_predicted):
  # Translate classifications to numbers to allow classification_report
  y_test_int = translate_to_numbers(y_test)
  y_predicted_int = translate_to_numbers(y_predicted)

  return classification_report(y_test_int, y_predicted_int, target_names=headers)


def clf_confusion_matrix(y_test, y_predicted):
  # calc confisuon matrix
  return confusion_matrix(y_test, y_predicted)


def score(y_test, y_predicted):
  return np.mean(y_predicted == y_test)


def print_stats(best_params, best_score, report=False, confusion=False):
  print "## Best params: %s " % best_params
  print "## Best Score: %s " % best_score

  if report != None:
    print "## Classification Report: "
    print report

  if confusion != None:
    print "## Confusion Matrix: "
    print confusion

