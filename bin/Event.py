#!/usr/bin/python
# -*- encoding: utf-8 -*-

import changefinder

class Event:
  def __init__(self, threshold=1.0, r=0.02, order=1, smooth=5):
    self.noise = []
    self.attack = []
    self.burst = []
    self.total = []
    self.learning = []
    self.noiseScore = []
    self.totalScore = []
    self.noiseDiff = []
    self.totalDiff = []
    self.noiseAlert = []
    self.totalAlert = []

    self.length = 0
    self.attackTime = -1
    self.detectionTime = -1
    self.missDetectionTime = -1
    self.threshold = threshold
    self.r = r
    self.order = order
    self.smooth = 5
    self.detection = False
    self.missDetection = False
  
  def __loadTimeSeries(self, path, targetList):
    for line in open(path, 'r'):
      i = int(line)
      targetList.append(i)

  def loadNoise(self, path):
    self.__loadTimeSeries(path, self.noise)

  def loadNoiseWithBurst(self, path1, path2):
    self.__loadTimeSeries(path1, self.noise)
    self.__loadTimeSeries(path2, self.burst)
    for i in range(len(self.noise)):
      self.noise[i] += self.burst[i]

  def loadNoiseWithLearning(self, path, learningLen):
    self.__loadTimeSeries(path, self.noise)
    for i in range(learningLen):
      temp = self.noise.pop(0)
      self.learning.append(temp)

  def loadNoiseWithBurstAndLearning(self, path1, path2, learningLen):
    self.__loadTimeSeries(path1, self.noise)
    self.__loadTimeSeries(path2, self.burst)
    for i in range(len(self.noise)):
      self.noise[i] += self.burst[i]
    for i in range(learningLen):
      temp = self.noise.pop(0)
      self.learning.append(temp)

  def loadAttack(self, path):
    self.__loadTimeSeries(path, self.attack)
    for i in range(len(self.attack)):
      c = self.attack[i]
      if c > 0:
        self.attackTime = i
        break

  def calcTotal(self):
    for i in range(len(self.attack)):
      self.total.append(self.attack[i] + self.noise[i])
      self.totalAlert.append(0)
      self.noiseAlert.append(0)

  def __calcScore(self, inputList, score, diff, useLearningData=False):
    cf = changefinder.ChangeFinder(r=self.r, order=self.order, smooth=self.smooth)
    if useLearningData==False:
      for n in self.noise:
        cf.update(n)
    else:
      for l in self.learning:
        cf.update(l)
    for i in inputList:
      s = cf.update(i)
      score.append(s)
    prev = score[0]
    for s in score:
      d = s-prev
      diff.append(d)
      prev = s

  def calcNoiseScore(self, useLearningData=False):
    self.__calcScore(self.noise, self.noiseScore, self.noiseDiff, useLearningData)

  def calcTotalScore(self, useLearningData=False):
    self.__calcScore(self.total, self.totalScore, self.totalDiff, useLearningData)

  def detect(self, inputList, alert):
    for i in range(len(inputList)):
      d = inputList[i]
      if d >= self.threshold:
        alert[i] = 1
      else:
        alert[i] = 0

  def detectAttack(self):
    self.detect(self.totalDiff, self.totalAlert)
    fromAttackToEnd = self.totalAlert[self.attackTime:]
    if 1 in fromAttackToEnd:
      self.detection = True
    else:
      self.detection = False

  def detectAttackWithTime(self):
    self.detect(self.totalDiff, self.totalAlert)
    fromAttackToEnd = self.totalAlert[self.attackTime:]
    if 1 in fromAttackToEnd:
      self.detection = True
      self.detectionTime = self.totalAlert.index(1)
    else:
      self.detection = False
      self.detectonTime = -1

  def detectNoise(self):
    self.detect(self.noiseDiff, self.noiseAlert)
    if 1 in self.noiseAlert:
      self.missDetection = True
    else:
      self.missDetection = False

  def detectNoiseWithTime(self):
    self.detect(self.noiseDiff, self.noiseAlert)
    if 1 in self.noiseAlert:
      self.missDetection = True
      self.missDetectionTime = self.noiseAlert.index(1)
    else:
      self.missDetection = False
      self.missDetectionTime = -1
