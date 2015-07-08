#!/usr/bin/python
# -*- encoding: utf-8 -*-

import Event
import collections
import random

thresholdList = {}
for line in open('./bestThreshold.txt', 'r'):
  para = line.split(',')
  as_number = int(para[0])
  th = float(para[1])
  thresholdList[as_number] = th

degreeRank = []
ASList = []
# select node by degree
for line in open('degree_100.txt', 'r'):
  para = line.split(',')
  as_number = int(para[0])
  degree = int(para[1])
  degreeRank.append((as_number, degree))
degreeRank.sort(key=lambda x:(x[1]), reverse = True)
for i in range(len(degreeRank)):
  ASList.append(degreeRank[i][0])

TPCountList = []
FPCountList = []
for i in range(10):
  TPCountList.append(collections.defaultdict(int))
  FPCountList.append(collections.defaultdict(int))

noiseNumbers = range(0, 10000+1)
random.shuffle(noiseNumbers)

for i in range(100):
  eventList = {}
  globalAttackAlertCount = []
  globalNoiseAlertCount = []
  rank = 1
  for as_number in ASList:
    event = Event.Event()
    attackFile = "../../attack_data/node100/%05d-%04d.txt" % (as_number, i)
    event.loadAttack(attackFile)
    noiseFile = "../../random_noise/lambda_%05d" % (noiseNumbers[i])
    burstFile = "../../burst_noise/%05d" % (random.randint(0, 299))
    event.loadNoiseWithBurstAndLearning(noiseFile, burstFile, 300)
    event.calcTotal()
    event.calcTotalScore(useLearningData = True)
    event.calcNoiseScore(useLearningData = True)

    event.threshold = thresholdList[as_number]
    event.detectAttackWithTime()
    temp = [0]*len(event.totalAlert)
    for j in range(0, 10):
      globalAttackAlertCount.append([])
      globalNoiseAlertCount.append([])
      if (len(globalAttackAlertCount[j]) == 0):
        globalAttackAlertCount[j] =[0] * len(event.totalAlert)
        globalNoiseAlertCount[j] = [0] * len(event.noiseAlert)
    for j in range(len(event.totalAlert)):
      if event.totalAlert[j] == 1:
        for k in range(j, j+5):
          if k >= len(event.totalAlert):
            continue
          else:
            temp[k] = 1
    for d in range(10, 100+1, 10):
      if rank<=d:
        for j in range(len(event.totalAlert)):
          globalAttackAlertCount[(d/10) -1][j] += temp[j]

    event.detectNoiseWithTime()
    temp = [0] * len(event.totalAlert)
    for j in range(len(event.noiseAlert)):
      if event.noiseAlert[j] == 1:
        for k in range(j, j+5):
          if k >= len(event.noiseAlert):
            continue
          else:
            temp[k] = 1
    for d in range(10, 100+1, 10):
      if rank<=d:
        for j in range(len(event.noiseAlert)):
          globalNoiseAlertCount[(d/10)-1][j] += temp[j]
    rank+=1

  for j in range(0, 10):
    maxAttackAlert = max(globalAttackAlertCount[j])
    maxNoiseAlert = max(globalNoiseAlertCount[j])
    for th in range(1, (j+1)*10):
      if maxAttackAlert >= th:
        TPCountList[j][th] += 1
      if maxNoiseAlert >= th:
        FPCountList[j][th] += 1

  
  print "%04d" % (i)
  """
  print "Attack"
  print globalAttackAlertCount
  print "Noise"
  print globalNoiseAlertCount
  print ""
  """
for node in range(10, 100+1, 10):
  outputFileName = "./globalResultWithDegree%s" % node
  outputFile = open(outputFileName, 'w')
  for th in range(1, node+1):
    tp = float(TPCountList[(node/10)-1][th]) / 100.0
    fp = float(FPCountList[(node/10)-1][th]) / 100.0
    line = "%d, %f, %f\n" % (th, tp, fp)
    outputFile.write(line)
