#!/usr/bin/python
import sys
import logging

from models import *


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import storage.data as d
import storage.prediction_exporter as pe

import utils.stats as s
import utils.preprocessor_methods as pr

from numpy import *
from pylab import *


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

d.set_file_names()
docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = d.get_data()
pe.set_base_from_dataset(d.get_full_test_set())

vect_options = {
  'ngram_range': (1,1),
  'sublinear_tf': True,
  'preprocessor': pr.remove_noise,
  'use_idf': False,
  'stop_words': None
}

default_options = {
  'C': 1.0
}

clf = SVM(docs_train, y_train, default_options=default_options, vect_options=vect_options)

y_predicted = clf.predict(docs_test)
conf_arr = s.confusion_matrix(y_test, y_predicted)

norm_conf = []
for i in conf_arr:
        a = 0
        tmp_arr = []
        a = sum(i,0)
        for j in i:
                tmp_arr.append(float(j)/float(a))
        norm_conf.append(tmp_arr)

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111)
res = ax.imshow(array(norm_conf), cmap=cm.jet, interpolation='nearest')
for i, cas in enumerate(conf_arr):
    for j, c in enumerate(cas):
        if c>0:
            plt.text(j-.2, i+.2, c, fontsize=14)
cb = fig.colorbar(res)
savefig("plots/confusion_matrix.png", format="png")
