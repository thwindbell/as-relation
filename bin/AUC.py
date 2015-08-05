#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
import MyConf

lambdaList = [10, 100, 1000, 10000]

argv = sys.argv
argc = len(argv)

if argc < 3:
  print "Usage : python AUC.py env_dir number_of_node"
  sys.exit(0)

ENV_DIR = MyConf.ENV + argv[1]
NUMBER_OF_NODE = int(argv[2])

for l in lambdaList:
  auclist = {}
  for as_number in range(1, NUMBER_OF_NODE+1):
    path = ENV_DIR + "/threshold/lambda%05d-as%05d.txt" % (l, as_number)
    data = []
    x = []
    y = []
    points = {}
    aucx = []
    aucy = []
    for line in open(path, 'r'):
      para = line.split(',')
      tp = float(para[1])
      fp = float(para[2])
      data.append((fp,tp))
      x.append(fp)
      y.append(tp)

    for i in range(len(x))[::-1]:
      points[x[i]] = y[i]

    for key in sorted(points.keys()):
      aucx.append(key)
      aucy.append(points[key])

    prev = aucx[0]
    auc = 0.0
    for i in range(1, len(aucx)):
      d = aucx[i] - prev
      prev = aucx[i]
      auc += (aucy[i] * d)
    auclist[as_number] = auc

  outputFileName = ENV_DIR + "/AUC/lambda%05d.txt" % (l)
  outputFile = open(outputFileName, 'w')
  for as_number in sorted(auclist.keys()):
    auc = auclist[as_number]
    line = "%05d, %f\n" % (as_number, auc)
    outputFile.write(line)
