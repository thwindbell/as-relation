#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt
import os

inputFiles = os.listdir('./localAUC')

for inputFile in inputFiles:
  auc = []
  degree = []
  customer = []
  transit = []
  path = "./localAUC/%s" % (inputFile)
  for line in open(path, 'r'):
    para = line.split(',')
    auc.append(float(para[1]))
    degree.append(int(para[2]))
    customer.append(int(para[3]))
    transit.append(int(para[4]))
  """
  fig = plt.figure(figsize=(10,10))
  plt.rcParams['font.size'] = 24
  plt.tick_params(pad=10)
  ax = fig.add_subplot(1, 1, 1)
  ax.set_xlabel('Degree of AS')
  ax.set_ylabel('AUC')
  ax.set_ylim([0.0, 1.0])
  plt.plot(degree, auc, 'o', markersize=20, color="0.5")
  outputFileName = "./plot/%s_Degree.png" % (inputFile)
  plt.savefig(outputFileName, bbox_inches='tight')
  plt.close()
  """
  fig = plt.figure(figsize=(10,6))
  plt.rcParams['font.size'] = 30
  plt.tick_params(pad=15)
  ax = fig.add_subplot(1, 1, 1)
  ax.set_xlabel('# of connected customer ASes')
  ax.set_ylabel('AUC')
  ax.set_ylim([0.0, 1.0])
  plt.plot(customer, auc, 'o', markersize=25, color="0.5")
  outputFileName = "./plot/%s_Customer.eps" % (inputFile)
  plt.savefig(outputFileName, bbox_inches='tight')
  plt.close()
  """
  fig = plt.figure(figsize=(10,10))
  plt.rcParams['font.size'] = 24
  plt.tick_params(pad=10)
  ax = fig.add_subplot(1, 1, 1)
  ax.set_xlabel('Custopmer & Provider of AS')
  ax.set_ylabel('AUC')
  ax.set_ylim([0.0, 1.0])
  plt.plot(transit, auc, 'o', markersize=20, color="0.5")
  outputFileName = "./plot/%s_Transit.png" % (inputFile)
  plt.savefig(outputFileName, bbox_inches='tight')
  plt.close()
  """
