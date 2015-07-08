#!/usr/bin/python
# -*- encoding: utf-8 -*-

import collections
import Event

thresholdList = []
for i in range(200):
  f = 0.1 * float(i)
  thresholdList.append(f)
thresholdList.append(100)
TPList = {}
FPList = {}
optimalThreshold = {}

NODE_NUM = 0
for line in open('./degree/degree_1000.txt', 'r'):
  NODE_NUM += 1

LOOP = 100

lambdaList = {10, 100, 1000, 10000}

for as_number in range(1, NODE_NUM+1):
  for l in lambdaList:
    FPList[as_number] = collections.defaultdict(float)
    TPList[as_number] = collections.defaultdict(float)
    for i in range(LOOP):
      event = Event.Event()
      attackFile = "../attack_data/node1000/%05d-%04d.txt" % (as_number, i)
      event.loadAttack(attackFile)
      noiseFile = "../random_noise/lambda_%05d-%04d" % (l, i)
      event.loadNoiseWithLearning(noiseFile, 300)
      event.calcTotal()
      event.calcTotalScore(useLearningData = True)
      event.calcNoiseScore(useLearningData = True)

      for th in thresholdList:
        event.threshold = th
        event.detectAttack()
        event.detectNoise()
        if event.detection == True:
          TPList[as_number][th] += 1.0
        if event.missDetection == True:
          FPList[as_number][th] += 1.0

    TPForPlot = []
    FPForPlot = []
    for th in thresholdList:
      TPList[as_number][th] /= float(LOOP)
      FPList[as_number][th] /= float(LOOP)
      TPForPlot.append(TPList[as_number][th])
      FPForPlot.append(FPList[as_number][th])

    fileName = "./node1000/lambda%05d/%05d.txt" % (l, as_number)
    outputFile = open(fileName, 'w')
    for i in range(len(thresholdList)):
      th = thresholdList[i]
      tp = TPForPlot[i]
      fp = FPForPlot[i]
      line = "%f, %f, %f\n" % (th, tp, fp)
      outputFile.write(line)
