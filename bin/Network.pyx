#!/usr/bin/python
# -*- coding: utf-8 -*-

import AS
import networkx as nx
import pylab
  
def logToCount(logList, countList, int MAX_COUNT, int STEP=1000):
  timestamps = []
  cdef int time = 0
  cdef int i = 0
  cdef int t = 0
  cdef int index = 0
  for line in logList:
    time = line[2]
    timestamps.append(time)

  for i in range(MAX_COUNT):
    countList.append(0)
  for t in timestamps:
    index = int(t/STEP)
    countList[index] += 1

cdef class Network:
  cdef public dict addr_to_as, as_dict
  cdef public list top_as_numbers

  def __init__(self):
    self.addr_to_as = {}
    self.as_dict = {}
    self.top_as_numbers = []

  def loadRelationFile(self, filename):
    for line in open(filename, 'r'):
      if line.startswith('#'):
        continue  # コメント行
      para = line.split('|')
      if len(para) != 3:
        continue  # 改行 or その他の関係の無い行

      node1 = int(para[0])
      node2 = int(para[1])
      connection_type = int(para[2])
      if node1 not in self.as_dict:
        self.as_dict[node1] = AS.AS(node1)
      if node2 not in self.as_dict:
        self.as_dict[node2] = AS.AS(node2)

      if (connection_type == -1):
        # transit connection, node1 provide node2
        provider = self.as_dict[node1]
        customer = self.as_dict[node2]
        provider.customerNodes[customer.as_number] = customer
        customer.providerNodes[provider.as_number] = provider
        # customer -> provider
      elif (connection_type == 0):
        # peer connection
        peer1 = self.as_dict[node1]
        peer2 = self.as_dict[node2]
        peer1.peerNodes[peer2.as_number] = peer2
        peer2.peerNodes[peer1.as_number] = peer1

    return len(self.as_dict)

  def searchTopAS(self):
    for node in self.as_dict.values():
      if len(node.providerNodes) == 0:
        self.top_as_numbers.append(node.as_number)
    
    return len(self.top_as_numbers)

  def exchangeRoutingTable(self):
    # トップレベルASから再帰的に下位ASのcustomerTableを統合
    for as_number in self.top_as_numbers:
      top_as = self.as_dict[as_number]
      top_as.mergeCustomerTable()

    # 全ASでピアにcustomerTableの内容を通知
    for node in self.as_dict.values():
      node.mergePeerTable()

    # トップレベルASから再帰的に下位ASにcustomerTable, peerTable,
    # providerTableの内容を通知
    for as_number in self.top_as_numbers:
      top_as = self.as_dict[as_number]
      top_as.transit()

  def distributeNetAddr(self):
    seq = 1
    for node in self.as_dict.values():
      networkAddr = seq << 16   # 上位16ビットがネットワーク部、下位16ビットがホスト部
      node.networkAddress = networkAddr
      node.netmask = 0xFFff0000
      seq += 1
      self.addr_to_as[networkAddr] = node.as_number

  def traceroute(self, strSrc, strDst, int startTime=0, int packets=3):
    cdef int delay = 13   # delay per router
    cdef int elapsed = 0 # ms
    cdef int src = AS.AS.strAddrToInt(strSrc)
    cdef int dst = AS.AS.strAddrToInt(strDst)
    cdef int mask = 0xFFff0000
    cdef int srcNet = src & mask
    cdef int dstNet = dst & mask

    cdef int src_as_number = self.addr_to_as[srcNet]
    cdef int dst_as_number = self.addr_to_as[dstNet]

    current = self.as_dict[src_as_number]

    cdef int i, nexthop
    while True:
      # ホップ毎に指定されたパケット数を送信する
      for i in range(packets):
        elapsed += delay
        current.addLog(src, dst, startTime + elapsed)
      route = None
      if dst_as_number in current.customerTable:
        route = current.customerTable[dst_as_number]
      elif dst_as_number in current.peerTable:
        route = current.peerTable[dst_as_number]
      elif dst_as_number in current.providerTable:
        route = current.providerTable[dst_as_number]
      else:
        return -1
      
      nexthop = route[0]
      if nexthop == -1:
        break
      else:
        current = self.as_dict[nexthop]

    return elapsed

  def clearASLog(self):
    for node in self.as_dict.values():
      node.clearLog()


