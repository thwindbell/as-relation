#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pylab as pylab
import MyConf

def drawGraph(filename):
  g = nx.DiGraph()
  as_dict = {}
  for line in open(filename, 'r'):
    if line.startswith('#'):
      continue  # コメント行
    para = line.split('|')
    if len(para) != 3:
      continue  # 改行 or その他の関係の無い行

    node1 = int(para[0])
    node2 = int(para[1])
    connection_type = int(para[2])

    if node1 not in as_dict:
      as_dict[node1] = node1
      g.add_node(node1)
    if node2 not in as_dict:
      as_dict[node2] = node2
      g.add_node(node2)

    if (connection_type == -1):
      g.add_edge(node2, node1, weight=1, label='transit')
    elif (connection_type == 0):
      g.add_edge(node1, node2, weight=0, label='peer')

  transit = [(u,v) for (u,v,d) in g.edges(data=True) 
      if d['weight'] > 0.5]
  peer = [(u,v) for (u,v,d) in g.edges(data=True) 
      f d['weight'] <= 0.5]
  pylab.figure(figsize=(4, 4))

  # pos = nx.spring_layout(g)
  pos = nx.circular_layout(g)
  # pos = nx.random_layout(g)

  nx.draw_networkx_nodes(g, pos, node_size=30, node_color='w')
  nx.draw_networkx_edges(g, pos, edgelist=transit, width=1, edge_color='b')
  nx.draw_networkx_edges(g, pos, edgelist=peer, arrows=False, edge_color='g', style='dashed')
  nx.draw_networkx_labels(g, pos, font_size=20, font_color='r')
  pylab.xticks([])
  pylab.yticks([])
  pylab.savefig(MyConf.TEMP + "network.png")
  pylab.show()

drawGraph(MyConf.TOPOLOGY + "testtopo.txt")
