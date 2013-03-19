#!/usr/bin/env python
# a bar plot with errorbars
import sys
import numpy as np
import logging

from models import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



import utils.utils as u
import utils.stats as s

import storage.data as d
from pylab import arange, savefig

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

d.set_file_names()
docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = d.get_data()

# labels = ['NB', 'SVM', 'MaxEnt', 'Combined (Foo -> Bar)', 'Combined (Foo -> Bar)', 'Combined (Foo -> Bar)', 'Combined (Foo -> Bar)', 'Combined (Foo -> Bar)', 'Combined (Foo -> Bar)', 'Boosting']
# values = [0.549392, 0.34543453, 0.23432999, 0.654213, 0.3213495, 0.65343, 0.53999211, 0.34543453, 0.23432999, 0.654213]

labels = []
values = []

def test(clf):
	global labels, values

	y_predict = clf.predict(docs_test)
	score = u.score(y_test, y_predict)

	labels.append(str(clf))
	values.append(score)

def autolabel(rects):
    # attach some text labels
    for i, rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., height * 1.01, '%5.3f' % values[i],
                ha='center', va='bottom')

clf = Boosting(docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity)
map(lambda x: test(x), clf.models + [clf])


val = values    # the bar lengths
pos = arange(len(values))+.5    # the bar centers on the y axis



fig  = plt.figure()
rect = plt.bar(pos, val, align='center')
autolabel(rect)
plt.xticks(pos, labels)
plt.xlabel('Algorithms')

plt.ylabel('Accuracy')
plt.title('Comparison of the different ?')
plt.grid(True)
fig.autofmt_xdate()

savefig("plots/comparison_different_testset_reduce_3000.png", format="png")
