#!/usr/bin/python
# -*- encoding: utf-8 -*-

import networkx
import numpy as np
import numpy.random as np
import matplotlib.pyplot as plt
import collections
import sys
import os
import glob
import math

threshold = {}

for fileName in glob.glob('./threshold/*'):
  min_distance = 2.0
  best_th = -1
  best_tp = -1
  best_fp = -1
  for line in open(fileName, 'r'):
    para = line.split(',')
    th = float(para[0])
    tp = float(para[1])
    fp = float(para[2])
    d = math.sqrt( ((1-tp)**2 + (0-fp)**2) )
    if d < min_distance:
      min_distance = d
      best_th = th
      best_tp = tp
      best_fp = fp

  threshold[fileName] = best_th
  para = fileName.split('/')
  para = para[2].split('.')
  as_number = int(para[0])
  #print "%d: th=%f, tp=%f, fp=%f, d=%f" % (as_number, best_th, best_tp, best_fp, min_distance)
  print "%d,%f" % (as_number, best_th)
