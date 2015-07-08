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
for line in open('degree30.txt', 'r'):
  para = line.split(',')
  as_number = int(para[0])
  degree = int(para[1])
  degreeRank.append((as_number, degree))
degreeRank.sort(key=lambda x:(x[1]), reverse = True)
ASList = []
for i in range(10):
  print degreeRank[i]
  ASList.append(degreeRank[i][0])

TPCountList = collections.defaultdict(int)
FPCountList = collections.defaultdict(int)

noiseNumbers = range(0, 10000+1)
random.shuffle(noiseNumbers)

for i in range(100):
  eventList = {}
  globalAttackAlertCount = []
  globalNoiseAlertCount = []
  for as_number in ASList:
    event = Event.Event()
    attackFile = "../../attack_data/node30/%05d-%04d.txt" % (as_number, i)
    event.loadAttack(attackFile)
    noiseFile = "../../random_noise/lambda_%05d" % (noiseNumbers[i])
    burstFile = "../../burst_noise/%05d" % (random.randint(0, 299))
    event.loadNoiseWithBurstAndLearning(noiseFile, burstFile, 300)
    event.calcTotal()
    event.calcTotalScore(useLearningData = True)
    event.calcNoiseScore(useLearningData = True)

    event.threshold = thresholdList[as_number]
    event.detectAttackWithTime()
    temp = [0] * len(event.totalAlert)
    if (len(globalAttackAlertCount) == 0):
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


    event.detectNoiseWithTime()
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
  for th in range(1, len(ASList)+1):
    if maxAttackAlert >= th:
      TPCountList[th] += 1
    if maxNoiseAlert >= th:
      FPCountList[th] += 1
  
  print "%04d" % (i)
  """
  print "Attack"
  print globalAttackAlertCount
  print "Noise"
  print globalNoiseAlertCount
  print ""
  """

for th in range(1, len(ASList)+1):
  tp = float(TPCountList[th]) / 100.0
  fp = float(FPCountList[th]) / 100.0
  line = "%d, %f, %f" % (th, tp, fp)
  print line
