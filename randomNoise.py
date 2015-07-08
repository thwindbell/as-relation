#!/usr/bin/python
# -*- encoding: utf-8 -*-

import numpy.random as rand

SIZE = 600
lambdaList = {10, 100, 1000, 10000}

for l in lambdaList:
  for i in range(100):
    noise = rand.poisson(lam=l, size=SIZE)
    fileName = "./random_noise/lambda_%05d-%04d" % (l, i)
    outputFile = open(fileName, 'w')
    for n in noise:
      line = "%d\n" % n
      outputFile.write(line)
    outputFile.close()

