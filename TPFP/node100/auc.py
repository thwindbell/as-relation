#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os

degreeList = {}
for line in open('./degree_100.txt', 'r'):
  para = line.split(',')
  as_number = int(para[0])
  degree = int(para[1])
  degreeList[as_number] = degree

files = os.listdir('./threshold/')
auclist = {}
for fileName in files:
  path = "./threshold/%s" % (fileName)
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

  for i in range(len(x)-1, -1, -1):
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
  para = fileName.split('.')
  as_number = int(para[0])
  auclist[as_number] = auc

outputFile = open('./auclist.txt', 'w')
for as_number in sorted(auclist.keys()):
  auc = auclist[as_number]
  degree = degreeList[as_number]
  line = "%02d, %f, %d\n" % (as_number, auc, degree)
  outputFile.write(line)
