#!/usr/bin/env python
# a bar plot with errorbars
import sys
import numpy as np
import logging


import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from models import *

import utils.utils as u
import utils.stats as stat

import storage.data as d

from numpy import *
from pylab import *


from sklearn.metrics import precision_recall_fscore_support

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

d.set_file_names()
docs_test, y_test, docs_train, y_train, docs_train_subjectivity, y_train_subjectivity, docs_train_polarity, y_train_polarity = d.get_data()

labels = []
res = [
    [],
    [],
    []
]

def test(clf):
    global labels, pres, recall, f1score

    y_pred = clf.predict(docs_test)
    p, r, f1, s = precision_recall_fscore_support(y_test, y_pred)

    labels.append(str(clf))

    res[0].append(np.mean(p))
    res[1].append(np.mean(r))
    res[2].append(np.mean(f1))

    conf_arr = stat.confusion_matrix(y_test, y_pred)

    norm_conf = []
    for i in conf_arr:
            a = 0
            tmp_arr = []
            a = sum(i,0)
            for j in i:
                    tmp_arr.append(float(j)/float(a))
            norm_conf.append(tmp_arr)

    return conf_arr, norm_conf


def autolabel(rects):
    # attach some text labels
    for i, rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., height, '%5.3f' % height,
                ha='center', va='top', rotation=90)


c1 = MaxEnt(docs_train_subjectivity, y_train_subjectivity)
c2 = SVM(docs_train_polarity, y_train_polarity)

clf = Combined(c1, c2)

conf_arr, norm_conf = test(clf)

N = len(labels)
ind = np.arange(N)  # the x locations for the groups
width = 1       # the width of the bars


fig = plt.figure(1)
ax = plt.subplot(111)

colors = ['#FA6E6E', '#6E9FFA', '#A4FA6E']
plt.xticks(ind + width * 2, labels)
plt.title('Different scores by algorithms')
plt.grid(True)

for i, l in enumerate(labels):
    for x, y in enumerate(res):
        rect = ax.bar(ind+(width * x) + 4, res[x], width, color=colors[x])
        autolabel(rect)

# fig.autofmt_xdate()

# Shink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.legend( ['Precision', 'Recall', 'F1 Score'], loc='center left', bbox_to_anchor=(1, 0.5) )

savefig("plots/stats_best.png", format="png")



plt.clf()
fig = plt.figure(2)
ax = fig.add_subplot(111)
res = ax.imshow(array(norm_conf), cmap=cm.jet, interpolation='nearest')
for i, cas in enumerate(conf_arr):
    for j, c in enumerate(cas):
        if c>0:
            plt.text(j-.2, i+.2, c, fontsize=14)
cb = fig.colorbar(res)
savefig("plots/confusion_matrix_best.png", format="png")


