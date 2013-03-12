import numpy as np


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

def score(y_test, y_predicted):
  return np.mean(y_predicted == y_test)

def reduce_dataset(dataset, num):
  num_n, num_o, num_p = 0,0,0
  new_dataset = []
  for i in dataset:
    if i[2] == 'negative' and num_n < num:
      num_n += 1
      new_dataset.append(i)
    if i[2] == 'positive' and num_p < num:
      num_p += 1
      new_dataset.append(i)
    if i[2] == 'neutral' and num_o < num:
      num_o += 1
      new_dataset.append(i)

  return np.array(new_dataset)


conv = {
  'negative': 0,
  'neutral': 1,
  'positive': 2
}

def translate_to_numbers(li):
  return [conv[v] for v in li]

def translate_from_number(num):
  mapping = dict (zip(conv.values(), conv.keys()))
  return mapping[int(round(num))]


