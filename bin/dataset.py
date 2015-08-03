#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import AS
import collections
import random

if __name__ == '__main__':

  MAX_LEVEL = 100

  all_as_numbers = []
  as_list = {}
  top_as_list = {}
  all_edges = []

  for line in sys.stdin:
    if line.startswith('#'):
      continue  # コメント行は飛ばす
    para = line.split('|')
    if len(para) != 3:
      continue  # 改行 or その他の関係無い行は飛ばす

    node1 = int(para[0])
    node2 = int(para[1])
    connection_type = int(para[2])
    edge = {}
    edge['node1'] = node1
    edge['node2'] = node2
    edge['type'] = connection_type
    all_edges.append(edge)

    # as_listに存在しないASをas_listとall_as_numbersに追加
    if node1 not in as_list:
      as_list[node1] = AS.AS(node1)
      all_as_numbers.append(node1)
    if node2 not in as_list:
      as_list[node2] = AS.AS(node2)
      all_as_numbers.append(node2)

    if connection_type == -1:
      # transit connetion, node1 provide node2
      provider = as_list[node1]
      customer = as_list[node2]
      provider.customerNodes[customer.as_number] = customer
      customer.providerNodes[provider.as_number] = provider

    elif connection_type == 0:
      # peer connection
      peer1 = as_list[node1]
      peer2 = as_list[node2]
      peer1.peerNodes[peer2.as_number] = peer2
      peer2.peerNodes[peer1.as_number] = peer1


  all_as_numbers.sort()
  # print "全ノード数:%d" % (len(as_list))

  # トップレベルAS(providerNodesが空)の探索
  for node in as_list.values():
    if len(node.providerNodes) == 0:
      top_as_list[node.as_number] = node

  # トップレベルASから再帰的にネットワークサイズを計算
  for node in top_as_list.values():
    node.mergeCustomerNodes()

  # 指定したネットワークサイズのノードを探索
  root_node = None
  for as_number in all_as_numbers:
    node = as_list[as_number]
    networkSize = 1000
    th = 5
    error = networkSize - len(node.allCustomerNodes)
    error = abs(error)
    if (error <= th):
      root_node = as_list[as_number]
      break

  # root_node配下のノードをデータセットとして出力
  print "# root_node:%d" % root_node.as_number
  print "# size:%d" % len(root_node.allCustomerNodes)
  if root_node != None:
    for edge in all_edges:
      node1 = edge['node1']
      node2 = edge['node2']
      connection_type = edge['type']
      if node1 not in root_node.allCustomerNodes:
        continue
      if node2 not in root_node.allCustomerNodes:
        continue
      print "%d|%d|%d" % (node1, node2, connection_type)

'''
  # 全ASの情報を番号順に出力
  for as_number in all_as_numbers:
    node = as_list[as_number]
    providerNodes = node.providerNodes.keys()
    peerNodes     = node.peerNodes.keys()
    customerNodes = node.customerNodes.keys()
    allCustomerNodes = node.allCustomerNodes.keys()
    providerNodes.sort()
    peerNodes.sort()
    customerNodes.sort()
    allCustomerNodes.sort()
    size = len(node.allCustomerNodes)

    print "node:%d" % as_number
    print "\tsize:%d" % size
    print "\tproviderNodes:",
    print providerNodes
    print "\tpeerNodes:",
    print peerNodes
    print "\tcustomerNodes:",
    print customerNodes
    print "\tallCustomerNodes:",
    print allCustomerNodes
'''
