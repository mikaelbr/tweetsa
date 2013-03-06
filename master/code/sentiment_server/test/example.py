#!/usr/bin/python
import sys
import numpy as np
import logging

from os import path
from sklearn import decomposition, linear_model
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import filters as f
import preprocess as p

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

def add_filters (text):
  text = f.no_url(text)
  # text = f.username_placeholder(text)
  text = f.no_usernames(text)
  # text = f.no_emoticons(text)
  text = f.no_hash(text)
  # text = f.no_rt_tag(text)
  text = f.reduce_letter_duplicates(text)
  # text = p.remove_stopwords(text, ['not'])
  text = p.negation_attachment(text)

  return text

train_set_filename = (sys.argv[1] if len(sys.argv) > 1 else False) or 'data/train/output_tweets.tsv'
test_set_filename = (sys.argv[2] if len(sys.argv) > 2 else False) or 'data/test/test_output_tweets.tsv'

if not path.exists(train_set_filename) or not path.exists(test_set_filename):
  raise Exception("File not found")
 
my_data = np.loadtxt(train_set_filename, delimiter='\t', dtype='S', comments=None)
my_test_data = np.loadtxt(test_set_filename, delimiter='\t', dtype='S', comments=None)


better_result = []
for x in my_data:
  if x[4].lower() != "not available":
    better_result.append(x)

better_result = np.array(better_result)
my_data = better_result


for x in my_data:
  x[4] = add_filters(x[4])

# print my_data[:10,4]
# sys.exit(0)

# print len(my_data), len(better_result)

def test(text):
  print text
  return text

# my_data = my_data[:len(my_data)-1]
vect = CountVectorizer(charset_error='ignore', preprocessor=test)
text_clf = Pipeline([
      ('vect', vect),
      ('tfidf', TfidfTransformer()),
      ('clf', MultinomialNB()),
  ])

print "Dataset length: %s " % len(my_data)
print("Training...")
my_clf = text_clf.fit(my_data[:,4], my_data[:,3])

print "# Features: %s" % len(vect.vocabulary_)

print("Done! \nClassifying test set...")
predicted = my_clf.predict(my_test_data[:,4])

print(np.mean(predicted == my_test_data[:,3]))

print "Accuracy: %.2f" % my_clf.score(my_data[:,4], my_data[:,3])
print "Accuracy: %.2f" % my_clf.score(predicted, my_test_data[:,3])


