#!/usr/bin/python
# -*- encoding: utf-8 -*-

import math

nodeList = [10, 100, 1000]
lambdaList = [10, 100, 1000, 10000]

for node in nodeList:
  for l in lambdaList:
    threshold = {}
    for as_number in range(1, node+1):
      path = "./node%d/lambda%05d/%05d.txt" % (node, l, as_number)
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
    outputFileName = "./bestThreshold/node%d_lambda%d" % (node, l)
    outputFile = open(outputFileName, 'w')
    for as_number in sorted(threshold.keys()):
      th = threshold[as_number]
      line = "%05d, %f\n" % (as_number, th)
      outputFile.write(line)
    outputFile.close()
