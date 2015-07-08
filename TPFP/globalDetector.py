#!/usr/bin/python
# -*- encoding: utf-8 -*-

import Event
import collections

nodeList = [100, 1000]
lambdaList = [10, 100, 1000, 10000]
DETECTOR_NUM = 10

for node in nodeList:
  for l in lambdaList:
    thresholdList = {}
    path = "./bestThreshold/node%d_lambda%d" % (node, l)
    for line in open(path, 'r'):
      para = line.split(',')
      as_number = int(para[0])
      th = float(para[1])
      thresholdList[as_number] = th

    priority = []
    ASList = {}
    # select node by degree
    path = "./localAUC/node%d_lambda%d" % (node, l)
    for line in open(path, 'r'):
      para = line.split(',')
      as_number = int(para[0])
      customer = int(para[3])
      priority.append((as_number, customer))
    priority.sort(key=lambda x:(x[1]), reverse = True)
    ASList = []
    for i in range(DETECTOR_NUM):
      ASList.append(priority[i][0])

    TPCountList = collections.defaultdict(int)
    FPCountList = collections.defaultdict(int)

    for i in range(100):
      seq = "node%d-lambda%d-%d" % (node, l, i)
      print seq
      eventList = {}
      globalAttackAlertCount = []
      globalNoiseAlertCount = []
      for as_number in ASList:
        event = Event.Event()
        attackFile = "../attack_data/node%d/%05d-%04d.txt" % (node, as_number, i)
        event.loadAttack(attackFile)
        noiseFile = "../random_noise/lambda_%05d-%04d" % (l, i)
        event.loadNoiseWithLearning(noiseFile, 300)
        event.calcTotal()
        event.calcTotalScore(useLearningData = True)
        event.calcNoiseScore(useLearningData = True)
        event.threshold = thresholdList[as_number]

        event.detectAttackWithTime()
        event.detectNoiseWithTime()

        temp = [0] * len(event.totalAlert)
        if len(globalAttackAlertCount) == 0: 
          globalAttackAlertCount = [0] * len(event.totalAlert)
          globalNoiseAlertCount = [0] * len(event.noiseAlert)
        for j in range(len(event.totalAlert)):
          if event.totalAlert[j] == 1:
            for k in range(j, j+5):
              if k >= len(event.totalAlert):
                continue
              else:
                temp[k] = 1
        for j in range(len(event.totalAlert)):
          globalAttackAlertCount[j] += temp[j]

        temp = [0] * len(event.noiseAlert)
        for j in range(len(event.noiseAlert)):
          if event.noiseAlert[j] == 1:
            for k in range(j, j+5):
              if k >= len(event.noiseAlert):
                continue
              else:
                temp[k] = 1
        for j in range(len(event.noiseAlert)):
          globalNoiseAlertCount[j] += temp[j]

      maxAttackAlert = max(globalAttackAlertCount)
      maxNoiseAlert = max(globalNoiseAlertCount)
      for th in range(1, DETECTOR_NUM+1):
        if maxAttackAlert >= th:
          TPCountList[th] += 1
        if maxNoiseAlert >= th:
          FPCountList[th] += 1

    outputFileName = "./globalDetectorResult/node%d_lambda%d" % (node, l)
    outputFile = open(outputFileName, 'w')
    print TPCountList
    print FPCountList
    for th in range(1, DETECTOR_NUM+1):
      tp = float(TPCountList[th]) / 100.0
      fp = float(FPCountList[th]) / 100.0
      line = "%d, %f, %f\n" % (th, tp, fp)
      outputFile.write(line)
    outputFile.close()
