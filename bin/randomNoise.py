#!/usr/bin/python
# -*- encoding: utf-8 -*-

import numpy.random as rand
import MyConf

SIZE = 600
lambdaList = {10, 100, 1000, 10000}

for l in lambdaList:
  for i in range(100):
    noise = rand.poisson(lam=l, size=SIZE)
    fileName = "lambda_%05d-%04d.txt" % (l, i)
    path = MyConf.RANDOM_NOISE + fileName
    outputFile = open(path, 'w')
    for n in noise:
      line = "%d\n" % n
      outputFile.write(line)
    outputFile.close()

