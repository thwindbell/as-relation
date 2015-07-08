#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt
import os

files = os.listdir('./threshold/')
for fileName in files:
  path = "./threshold/%s" % (fileName)
  data = []
  x = []
  y = []
  for line in open(path, 'r'):
    para = line.split(',')
    tp = float(para[1])
    fp = float(para[2])
    data.append((fp,tp))
    x.append(fp)
    y.append(tp)

  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)
  #sc = ax.scatter(x, y, s=25, marker='x', color='b')
  ax.set_title('Roc Curve')
  ax.set_xlabel('False Positive Rate')
  ax.set_ylabel('True Positive Rate')
  ax.set_xlim([0.0, 1.0])
  ax.set_ylim([0.0, 1.0])
  plt.plot(x, y, '-', lw=3, label='roc curve')
  #ax.legend(loc='best')

  para = fileName.split('.')
  as_number = int(para[0])
  outputFile = './roc/%02d.png' % (as_number)
  #outputFile = './roc/%02d.eps' % (as_number)
  plt.savefig(outputFile)
  #plt.show()
  fig = None
