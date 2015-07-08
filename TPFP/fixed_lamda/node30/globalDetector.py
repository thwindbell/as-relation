#!/usr/bin/python
# -*- encoding: utf-8 -*-

import Event
import collections

thresholdList = {}
for line in open('./thresholdList.txt', 'r'):
  para = line.split(',')
  as_number = int(para[0])
  th = float(para[1])
  thresholdList[as_number] = th

TPCountList = collections.defaultdict(int)
FPCountList = collections.defaultdict(int)

for i in range(100):
  eventList = {}
  globalAttackAlertCount = []
  globalNoiseAlertCount = []
  for as_number in range(1, 30+1):
    event = Event.Event()
    attackFile = "./attack/%02d-%04d.txt" % (as_number, i)
    event.loadAttack(attackFile)
    noiseFile = "./noise/%02d-%04d.txt" % (as_number, i)
    burstFile = "./burst/%02d-%04d.txt" % (as_number, i)
    #event.loadNoise(noiseFile)
    event.loadNoiseWithBurst(noiseFile, burstFile)
    event.calcTotal()
    event.calcTotalScore()
    event.calcNoiseScore()

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
  for j in range(1, 30+1):
    if maxAttackAlert >= j:
      TPCountList[j] += 1
    if maxNoiseAlert >= j:
      FPCountList[j] += 1
  
  print "%04d" % (i)
  """
  print "Attack"
  print globalAttackAlertCount
  print "Noise"
  print globalNoiseAlertCount
  print ""
  """

print TPCountList
print FPCountList
