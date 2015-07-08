#!/usr/bin/python
# -*- coding: utf-8 -*-

class AS:
  def __init__(self, as_number):
    self.as_number = as_number
    self.networkAddress = 0x0A000000  # 10.0.0.0
    self.netmask        = 0xFFff0000  # 255.255.0.0

    self.customerTable = {}
    self.peerTable = {}
    self.providerTable = {}
    self.customerNodes = {}
    self.peerNodes = {}
    self.providerNodes = {}
    self.allCustomerNodes = {}

    self.routerList = []
    self.tracerouteLog = []

    # ルーティングテーブルに自分自身を追加
    self.customerTable[self.as_number] = {"Nexthop":-1, "Distance":0}
    self.allCustomerNodes[self.as_number] = self
 
    # 受け取ったテーブルを自身のテーブルに統合
  def mergeTable(self, original, additional, dataSource):
    for dst, value in additional.iteritems():
      new_distance = value["Distance"] + 1

      if (dst in original):
        original_value = original[dst]
        original_distance = original_value["Distance"]
        if (new_distance > original_distance):
          continue

      original[dst] = {"Nexthop":dataSource, "Distance":new_distance}

  def mergeCustomerTable(self):
    if len(self.customerTable) != 1:
      return self.customerTable

    for customer_number, customer in self.customerNodes.iteritems():
      additionalTable = customer.mergeCustomerTable()
      self.mergeTable(self.customerTable,
            additionalTable, customer_number)
    return self.customerTable

  def mergePeerTable(self):
    for peer_number, peer in self.peerNodes.iteritems():
      self.mergeTable(self.peerTable, peer.customerTable, peer_number)
    return self.peerTable

  def transit(self):
    for customer_number, customer in self.customerNodes.iteritems():
      customer.mergeTable(customer.providerTable, 
                            self.providerTable, self.as_number)
      customer.mergeTable(customer.providerTable,
                            self.peerTable, self.as_number)
      customer.mergeTable(customer.providerTable,
                            self.customerTable, self.as_number)
      customer.transit()

  def mergeCustomerNodes(self):
    if len(self.allCustomerNodes) != 1:
      return self.allCustomerNodes

    for customer in self.customerNodes.values():
      customers = customer.mergeCustomerNodes()
      for key, value in customers.iteritems():
        self.allCustomerNodes[key] = value
    return self.allCustomerNodes

  def addLog(self, src, dst, time=0):
    self.tracerouteLog.append((src, dst, time))

  def clearLog(self):
    self.tracerouteLog = []

  def toString(self):
    print "as_number : %d" % (self.as_number)
    print "\tnetworkAddress :",
    print self.networkAddress
    print "\tproviderNodes"
    print "\t\t",
    for provider in self.providerNodes.values():
      print "%d," % (provider.as_number) ,
    print ""
    print "\tpeerNodes"
    print "\t\t",
    for peer in self.peerNodes.values():
      print "%d," % (peer.as_number) ,
    print ""
    print "\tcustomerNodes"
    print "\t\t",
    for customer in self.customerNodes.values():
      print "%d," % (customer.as_number) ,
    print ""
    print "\tproviderTable"
    print "\t\tDestination, Nexthop, Distance"
    for dst, value in self.providerTable.iteritems():
      nexthop = value["Nexthop"]
      distance = value["Distance"]
      print "\t\t%d, %d, %d" % (dst, nexthop, distance)
    print "\tpeerTable"
    print "\t\tDestination, Nexthop, Distance"
    for dst, value in self.peerTable.iteritems():
      nexthop = value["Nexthop"]
      distance = value["Distance"]
      print "\t\t%d, %d, %d" % (dst, nexthop, distance)
    print "\tcustomerTable"
    print "\t\tDestination, Nexthop, Distance"
    for dst, value in self.customerTable.iteritems():
      nexthop = value["Nexthop"]
      distance = value["Distance"]
      print "\t\t%d, %d, %d" % (dst, nexthop, distance)
    print ""

  def printLog(self):
    print "as_number:%d" % self.as_number
    for line in self.tracerouteLog:
      src = line[0]
      dst = line[1]
      time = line[2]
      strSrc = AS.intAddrToStr(src)
      strDst = AS.intAddrToStr(dst)
      print "\t%d, %s, %s" % (time, strSrc, strDst)

  def printLogWithoutNumber(self):
    for line in self.tracerouteLog:
      src = line[0]
      dst = line[1]
      time = line[2]
      strSrc = AS.intAddrToStr(src)
      strDst = AS.intAddrToStr(dst)
      print "\t%d, %s, %s" % (time, strSrc, strDst)

  def isHostAddress(self, ipaddr):
    ipaddr = AS.strAddrToInt(ipaddr)
    if (ipaddr & self.netmask) == self.networkAddress:
      return True
    else:
      return False
  
  @staticmethod
  def strAddrToInt(addr):
    if isinstance(addr, int) == True:
      return addr
    if isinstance(addr, str) == False:
      return -1

    intAddr = 0
    para = addr.split('.')
    byteArray = map(int, para)
    intAddr += byteArray[0]<<24
    intAddr += byteArray[1]<<16
    intAddr += byteArray[2]<<8
    intAddr += byteArray[3]

    return intAddr

  @staticmethod
  def intAddrToStr(addr):
    if isinstance(addr, str) == True:
      return addr
    if isinstance(addr, int) == False:
      return -1

    stack = []
    for i in range(4):
      byte = addr & 0xFF
      stack.append(byte)
      addr = addr>>8
    stack.reverse()
    strBytes = map(str, stack)
    return '.'.join(strBytes)
