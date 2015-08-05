#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import math
import MyConf

lambdaList = [10, 100, 1000, 10000]

argv = sys.argv
argc = len(argv)

if argc < 3:
  print "Usage : python bestThreshold.py env_dir number_of_node"
  sys.exit(0)

ENV_DIR = MyConf.ENV + argv[1]
NUMBER_OF_NODE = int(argv[2])

for l in lambdaList:
  threshold = {}
  for as_number in range(1, NUMBER_OF_NODE+1):
    path = ENV_DIR + "/threshold/lambda%05d-as%05d.txt" % (l, as_number)
    min_distance = 2.0
    best_th = -1
    best_tp = -1
    best_fp = -1
    for line in open(path, 'r'):
      para = line.split(',')
      th = float(para[0])
      tp = float(para[1])
      fp = float(para[2])
      d = math.sqrt( ((1.0-tp)**2 + (0.0-fp)**2) )
      if d < min_distance:
        min_distance = d
        best_th = th
        best_tp = tp
        best_fp = fp

    threshold[as_number] = best_th
    outputFileName = ENV_DIR + "/bestThreshold/lambda%05d.txt" % (l)
    outputFile = open(outputFileName, 'w')
  for as_number in sorted(threshold.keys()):
    th = threshold[as_number]
    line = "%05d, %f\n" % (as_number, th)
    outputFile.write(line)
  outputFile.close()
