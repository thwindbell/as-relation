#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os

nodeList = [10, 100, 1000]
lambdaList = [10, 100, 1000, 10000]

for node in nodeList:
  degreeFile = './degree/degree_%d.txt' % (node)
  customerFile = './degree/customerLinks_%d.txt' % (node)
  transitFile = './degree/transit_%d.txt' % (node)
  degreeList = {}
  customerList = {}
  transitList = {}
  for line in open(degreeFile, 'r'):
    para = line.split(',')
    as_number = int(para[0])
    degree = int(para[1])
    degreeList[as_number] = degree
  for line in open(customerFile, 'r'):
    para = line.split(',')
    as_number = int(para[0])
    customer = int(para[1])
    customerList[as_number] = customer
  for line in open(transitFile, 'r'):
    para = line.split(',')
    as_number = int(para[0])
    transit = int(para[1])
    transitList[as_number] = transit
  for l in lambdaList:
    inputDir = "./node%d/lambda%05d/" % (node, l)

    files = os.listdir(inputDir)
    auclist = {}
    for fileName in files:
      path = "%s/%s" % (inputDir, fileName)
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
      para = fileName.split('.')
      as_number = int(para[0])
      auclist[as_number] = auc

    outputFileName = "./localAUC/node%d_lambda%d" % (node, l)
    outputFile = open(outputFileName, 'w')
    for as_number in sorted(auclist.keys()):
      auc = auclist[as_number]
      degree = degreeList[as_number]
      customer = customerList[as_number]
      transit = transitList[as_number]
      line = "%05d, %f, %d, %d, %d\n" % (as_number, auc, degree, customer, transit)
      outputFile.write(line)
