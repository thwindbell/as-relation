#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © Takayuki Hirayama <hirayama@sasase.ics.keio.ac.jp>
#
# Distributed under terms of the MIT license.

import sys
import networkx as nx
from networkx.algorithms.approximation import vertex_cover

if __name__ == '__main__':
  G = nx.Graph()

  for line in sys.stdin:
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    if line.startswith('#'):
      continue
    
    para = line.split('|')
    if len(para) != 3:
      continue
    node1 = int(para[0])
    node2 = int(para[1])
    if G.has_node(node1)==False:
      G.add_node(node1)
    if G.has_node(node2)==False:
      G.add_node(node2)
    G.add_edge(node1, node2)

  nodes = G.nodes()
  vc = vertex_cover.min_weighted_vertex_cover(G)

  is_vc = 0
  for node in sorted(nodes):
    if node in vc:
      is_vc = 1
    else:
      is_vc = 0
    print "%d, %d" % (node, is_vc)
