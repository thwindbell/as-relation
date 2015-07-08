#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plot
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

for as_number in range(1, 30+1):
  TPList[as_number] = collections.defaultdict(float)
  FPList[as_number] = collections.defaultdict(float)
  for i in range(100):
    event = Event.Event()
    attackFile = "./attack/%02d-%04d.txt" % (as_number, i)
    event.loadAttack(attackFile)
    noiseFile = "./noise/%02d-%04d.txt" % (as_number, i)
    event.loadNoise(noiseFile)
    event.calcTotal()
    event.calcTotalScore()
    event.calcNoiseScore()

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
    TPList[as_number][th] /= 100.0
    FPList[as_number][th] /= 100.0
    TPForPlot.append(TPList[as_number][th])
    FPForPlot.append(FPList[as_number][th])

  fileName = "./threshold/%02d.txt" % (as_number)
  outputFile = open(fileName, 'w')
  for i in range(len(thresholdList)):
    th = thresholdList[i]
    tp = TPForPlot[i]
    fp = FPForPlot[i]
    line = "%f, %f, %f\n" % (th, tp, fp)
    outputFile.write(line)
  """
  fig = plot.figure()
  ax = fig.add_subplot(111)
  sx = ax.scatter(FPForPlot, TPForPlot, s=25, marker="o", color="r")
  ax.set_xlim(0.0, 1.0)
  ax.set_ylim(0.9, 1.0)
  ax.grid(True)
  plot.show()
  """

