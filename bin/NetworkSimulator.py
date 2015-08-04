#!/usr/bin/python
# -*- coding: utf-8 -*-

import Network
import collections
import sys
import numpy.random as random
import MyConf

argv = sys.argv
argc = len(argv)

if argc < 7:
  print "Usage : python NetworkSimulator.py topologyFile outputDir loopCount numberOfAS numberOfBot numberOfDecoyServer"
  sys.exit(0)

TOPOLOGY_FILE = MyConf.TOPOLOGY + argv[1]
OUTPUT_DIR = MyConf.ENV + argv[2] + "/attack_file"
LOOP_COUNT = int(argv[3])
NUMBER_OF_AS = int(argv[4])
NUMBER_OF_BOT = int(argv[5])
NUMBER_OF_DECOY = int(argv[6])

myNet = Network.Network()
myNet.loadRelationFile(TOPOLOGY_FILE)
myNet.searchTopAS()
myNet.exchangeRoutingTable()
myNet.distributeNetAddr()

for i in range(LOOP_COUNT):
  # 100台のボットと100台のデコイをランダムに配置してtracerouteを実行
  botCounts   = collections.defaultdict(int)
  decoyCounts = collections.defaultdict(int)
  botList = []
  decoyList = []
  botNet = 0
  decoyNet = 0
  botCount = 0
  decoyCount = 0
  networkAddr = 0
  botAddr = 0
  decoyAddr = 0
  interval = 0
  startTime = 0
  elapsed = 0

  for j in range(NUMBER_OF_BOT):
    botNet    = random.randint(1, NUMBER_OF_AS + 1)
    botCounts[botNet] += 1
  for j in range(NUMBER_OF_DECOY):
    decoyNet  = random.randint(1, NUMBER_OF_AS + 1)
    decoyCounts[decoyNet] += 1

  for j in range(1, NUMBER_OF_AS + 1):
    botCount    = botCounts[j]
    decoyCount  = decoyCounts[j]
    networkAddr  = j << 16
    for k in range(2, 2+botCount):
      botAddr = networkAddr | k
      botList.append(botAddr)
    for k in range(2, 2+botCount):
      decoyAddr = networkAddr | k
      decoyList.append(decoyAddr)

  for src in botList:
    interval = 5
    startTime = 270000
    for dst in decoyList:
      elapsed = myNet.traceroute(src, dst, startTime)
      startTime += elapsed + interval

  # 各ASのログを保存
  for node in myNet.as_dict.values():
    as_number = node.as_number
    countList = []
    Network.logToCount(node.tracerouteLog, countList, 300, 1000)
    path = "%s/%05d-%04d.txt" % (OUTPUT_DIR, as_number, i)
    outputFile = open(path, 'w')
    for c in countList:
      line = "%d\n" % c
      outputFile.write(line)
  myNet.clearASLog()
"""
# 各ネットワークから一定の正規確率でtracerouteを実行
for i in range(100):
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
"""
