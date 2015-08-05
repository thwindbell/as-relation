#!/usr/bin/python
# -*- encoding: utf-8 -*-

import collections
import Event
import sys
import MyConf

argv = sys.argv
argc = len(argv)

if argc < 3:
  print "Usage : python TPFP.py env_dir number_of_as"
  sys.exit(0)

LOOP_COUNT = 100
ENV_DIR = MyConf.ENV + argv[1]
NUMBER_OF_AS = int(argv[2])

lambdaList = {10, 100, 1000, 10000}

thresholdList = []
for i in range(200):
  f = 0.1 * float(i)
  thresholdList.append(f)
thresholdList.append(100)
TPList = {}
FPList = {}
optimalThreshold = {}


for as_number in range(1, NUMBER_OF_AS+1):
  for l in lambdaList:
    FPList[as_number] = collections.defaultdict(float)
    TPList[as_number] = collections.defaultdict(float)
    for i in range(LOOP_COUNT):
      event = Event.Event()
      attackFile = ENV_DIR + "/attack_file/%05d-%04d.txt" % (as_number, i)
      event.loadAttack(attackFile)
      noiseFile = MyConf.RANDOM_NOISE + "/lambda_%05d-%04d.txt" % (l, i)
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
      TPList[as_number][th] /= float(LOOP_COUNT)
      FPList[as_number][th] /= float(LOOP_COUNT)
      TPForPlot.append(TPList[as_number][th])
      FPForPlot.append(FPList[as_number][th])

    fileName = ENV_DIR + "/threshold/lambda%05d-as%05d.txt" % (l, as_number)
    outputFile = open(fileName, 'w')
    for i in range(len(thresholdList)):
      th = thresholdList[i]
      tp = TPForPlot[i]
      fp = FPForPlot[i]
      line = "%f, %f, %f\n" % (th, tp, fp)
      outputFile.write(line)
