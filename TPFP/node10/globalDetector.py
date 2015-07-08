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
"""
for line in open('customerLinks_1000.txt', 'r'):
  para = line.split(',')
  as_number = int(para[0])
  degree = int(para[1])
  degreeRank.append((as_number, degree))
degreeRank.sort(key=lambda x:(x[1]), reverse = True)
for i in range(10):
  print degreeRank[i]
  ASList.append(degreeRank[i][0])
"""

# select node by auc
for line in open('auclist.txt', 'r'):
  para = line.split(',')
  as_number = int(para[0])
  auc = float(para[1])
  if auc >= 0.9:
    ASList.append(as_number)
    print "%05d, %f" % (as_number, auc)

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
    attackFile = "../../attack_data/node10/%05d-%04d.txt" % (as_number, i)
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
outputFile = open("./globalDetectorThreshold.txt", 'w')
for th in range(1, len(ASList)+1):
  tp = float(TPCountList[th]) / 100.0
  fp = float(FPCountList[th]) / 100.0
  line = "%d, %f, %f\n" % (th, tp, fp)
  print line
  outputFile.write(line)
