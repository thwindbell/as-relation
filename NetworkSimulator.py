#!/usr/bin/python
# -*- coding: utf-8 -*-

import Network
import collections
import sys
import numpy as np
import numpy.random as random
import time

def logToCount(logList, countList, MAX_COUNT, STEP=1000):
  timestamps = []
  for line in logList:
    time = line[2]
    timestamps.append(time)
  
  for i in range(MAX_COUNT):
    countList.append(0)
  for t in timestamps:
    index = int(t/STEP)
    countList[index] += 1

start = time.time()

myNet = Network.Network()
myNet.loadRelationFile('./topology/dataset_100a.txt')
myNet.searchTopAS()
myNet.exchangeRoutingTable()
myNet.distributeNetAddr()

elapsed = time.time() - start
print "routing finished"
print "%f[sec]" % (elapsed)

# 各ネットワークから一定の正規確率でtracerouteを実行
for i in range(1):
  for net in myNet.as_list:
    noiseCounts = np.random.poisson(80, 300)
    for j in range(0, len(noiseCounts)):
      startTime = j * 1000
      for k in range(noiseCounts[j]):
        dstNet = random.randint(1, 30 + 1)
        dstHost = random.randint(2, 254 + 1)
        dstAddr = dstNet << 16 | dstHost
        srcAddr = net.networkAddress | 0x02
        elapsed = myNet.traceroute(srcAddr, dstAddr, startTime)

elapsed = time.time() - start
print "traceroute finished"
print "%f[sec]" % (elapsed)
