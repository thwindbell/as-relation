#!/usr/bin/python
# -*- coding: utf-8 -*-

import Network
import collections
import sys
import numpy as np
import numpy.random as random

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

myNet = Network.Network()
myNet.loadRelationFile('./topology/dataset_30a.txt')
myNet.searchTopAS()
myNet.exchangeRoutingTable()
myNet.distributeNetAddr()

argv = sys.argv
if len(argv) != 5:
  print "Usage: python TPFPSimulator.py attackOutputDir noiseOutputDir burstOutputDir LoopCount\n"
  sys.exit(1)
attackOutputDir = argv[1]
noiseOutputDir = argv[2]
burstOutputDir = argv[3]
LOOP_COUNT = int(argv[4])

"""

for i in range(LOOP_COUNT):
  # 100台のボットと100台のデコイをランダムに配置してtracerouteを実行
  botCounts   = collections.defaultdict(int)
  decoyCounts = collections.defaultdict(int)
  botList = []
  decoyList = []
  for j in range(100):
    botNet    = random.randint(1, 30 + 1)
    decoyNet  = random.randint(1, 30 + 1)  
    botCounts[botNet] += 1
    decoyCounts[decoyNet] += 1

  for j in range(1, 30 + 1):
    botCount    = botCounts[j]
    decoyCount  = decoyCounts[j]
    botNet    = j << 16
    decoyNet  = j << 16
    for k in range(2, 2 + botCount):
      botAddr = botNet | k
      botList.append(botAddr)
    for k in range(2, 2 + decoyCount):
      decoyAddr = decoyNet | k
      decoyList.append(decoyAddr)

  for src in botList:
    interval = 5
    startTime = 270000
    for dst in decoyList:
      elapsed = myNet.traceroute(src, dst, startTime)
      startTime += elapsed + interval

  # 各ASのログを保存
  for node in myNet.as_list.values():
    as_number = node.as_number
    countList = []
    logToCount(node.tracerouteLog, countList, 300, 1000)
    path = "%s/%02d-%04d.txt" % (attackOutputDir, as_number, i)
    outputFile = open(path, 'w')
    for c in countList:
      line = "%d\n" % c
      outputFile.write(line)
  myNet.clearASLog()

# 各ネットワークから一定の正規確率でtracerouteを実行
for i in range(LOOP_COUNT):
  for net in myNet.as_list.values():
    noiseCounts = np.random.poisson(80, 300)
    for j in range(0, len(noiseCounts)):
      startTime = j * 1000
      for k in range(noiseCounts[j]):
        dstNet = random.randint(1, 30 + 1)
        dstHost = random.randint(2, 254 + 1)
        dstAddr = dstNet << 16 | dstHost
        srcAddr = net.networkAddress | 0x02
        elapsed = myNet.traceroute(srcAddr, dstAddr, startTime)

  # 各ASのログを保存
  for node in myNet.as_list.values():
    as_number = node.as_number
    countList = []
    logToCount(node.tracerouteLog, countList, 300, 1000)
    path = "%s/%02d-%04d.txt" % (noiseOutputDir, as_number, i)
    outputFile = open(path, 'w')
    for c in countList:
      line = "%d\n" % c
      outputFile.write(line)
  myNet.clearASLog()

"""

# 各ネットワークからランダムな時間に1度バースト的なtracerouteを実行
for i in range(LOOP_COUNT):
  for net in myNet.as_list.values():
    destCounts = collections.defaultdict(int)
    for j in range(100):
      destNet = random.randint(1, 30 + 1)
      destCounts[destNet] += 1

    srcAddr = net.networkAddress | 0x02
    destList = []
    for j in range(1, 30 + 1):
      destCount = destCounts[j]
      for k in range(destCount):
        destAddr = j << 16 | random.randint(2, 254 + 1)
        destList.append(destAddr)
    
    interval = 5
    startTime = random.randint(0, 3000000)
    for dst in destList:
      elapsed = myNet.traceroute(srcAddr, dst, startTime)

  # 各ASのログを保存
  for node in myNet.as_list.values():
    as_number = node.as_number
    countList = []
    logToCount(node.tracerouteLog, countList, 300, 1000)
    path = "%s/%02d-%04d.txt" % (burstOutputDir, as_number, i)
    outputFile = open(path, 'w')
    for c in countList:
      line = "%d\n" % c
      outputFile.write(line)
  myNet.clearASLog()


