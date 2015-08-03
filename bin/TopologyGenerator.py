#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © Takayuki Hirayama <hirayama@sasase.ics.keio.ac.jp>
#
# Distributed under terms of the MIT license.

import networkx as nx
import MyConf

MAX_ITERATION = 50;

def barabasi_albert(n, m):
  g = None
  for i in range(MAX_ITERATION):
    g = nx.barabasi_albert_graph(n, m);
    if (nx.algorithms.components.is_connected(g) == True):
      break
    else:
      g = None
  return g

def watts_strogatz(n, k, p):
  g = None
  for i in range(MAX_ITERATION):
    g = nx.watts_strogatz_graph(n, k, p)
    if (nx.algorithms.components.is_connected(g) == True):
      break;
    else:
      g = None
  return g

def waxman(n, alpha=0.4, beta=0.1):
  g = None
  for i in range(MAX_ITERATION):
    g = nx.waxman_graph(n, alpha, beta)
    if (nx.algorithms.components.is_connected(g) == True):
      break;
    else:
      g = None
  return g

def writeGraphToFile(g, filename):
  path = MyConf.TOPOLOGY + filename
  outputFile = open(path, "w")
  str = "# size = %d\n" % len(g.nodes())
  outputFile.write(str)
  for e in g.edges_iter(): 
    str = "%d|%d|0\n" % (e[0], e[1])
    outputFile.write(str)

if __name__ == '__main__':
  g = barabasi_albert(10, 2)
  if (g != None):
    writeGraphToFile(g, "testtopo.txt")
