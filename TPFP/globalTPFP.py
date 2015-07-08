#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt
import os

inputFiles = os.listdir('./localAUC')

nodeList = [1000]
lambdaList = [10, 100, 1000, 10000]



for node in nodeList:
  TPList = {}
  FPList = {}
  for l in lambdaList:
    TPList[l] = []
    FPList[l] = []
    path = "./globalDetectorResult/node%d_lambda%d" % (node, l)
    for line in open(path, 'r'):
      para = line.split(',')
      TP = float(para[1])
      FP = float(para[2])
      TPList[l].append(TP)
      FPList[l].append(FP)

  fig = plt.figure(figsize=(20,10))
  plt.rcParams['font.size'] = 40
  plt.tick_params(pad=15)
  ax = fig.add_subplot(1, 1, 1)
  ax.set_xlabel('$N_{th}$')
  ax.set_ylabel('TP')
  ax.set_ylim([0.0, 1.0])
  x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  plt.plot(x, TPList[10], 'o-', markersize=25, color="0.8", label="$\lambda=10$")
  plt.plot(x, TPList[100], 'v-', markersize=25, color='0.6', label='$\lambda=100$')
  plt.plot(x, TPList[1000], 's-', markersize=25, color='0.4', label='$\lambda=1,000$')
  plt.plot(x, TPList[10000], 'D-', markersize=25, color='0.2', label='$\lambda=10,000$')
  ax.set_xlim([0.5, 10.5])
  plt.legend(loc='best')
  outputFileName = "./plot/globalTP_node%d.eps" % (node)
  plt.savefig(outputFileName, bbox_inches='tight')
  plt.show()
  plt.close()

  fig = plt.figure(figsize=(20,10))
  plt.rcParams['font.size'] = 40
  plt.tick_params(pad=15)
  ax = fig.add_subplot(1, 1, 1)
  ax.set_xlabel('$N_{th}$')
  ax.set_ylabel('FP')
  ax.set_ylim([0.0, 1.0])
  x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  plt.plot(x, FPList[10], 'o-', markersize=25, color="0.8", label="$\lambda=10$")
  plt.plot(x, FPList[100], 'v-', markersize=25, color='0.6', label='$\lambda=100$')
  plt.plot(x, FPList[1000], 's-', markersize=25, color='0.4', label='$\lambda=1,000$')
  plt.plot(x, FPList[10000], 'D-', markersize=25, color='0.2', label='$\lambda=10,000$')
  ax.set_xlim([0.5, 10.5])
  plt.legend(loc='best')
  outputFileName = "./plot/globalFP_node%d.eps" % (node)
  plt.savefig(outputFileName, bbox_inches='tight')
  plt.show()
  plt.close()
