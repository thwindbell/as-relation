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

def writeGraphToFile(g, path):
  lines = []
  mapping = {}
  seq = 1

  for e in g.edges_iter():
    if e[0] not in mapping:
      mapping[e[0]] = seq
      seq += 1
    if e[1] not in mapping:
      mapping[e[1]] = seq
      seq += 1
    line = "%d|%d|0\n" % (mapping[e[0]], mapping[e[1]])
    lines.append(line)
  
  outputFile = open(path, "w")
  str = "# size = %d\n" % len(g.nodes())
  outputFile.write(str)
  for line in lines: 
    outputFile.write(line)

if __name__ == '__main__':
  g = waxman(100, 0.2, 0.2)
  if (g != None):
    writeGraphToFile(g, MyConf.WAXMAN + "waxman100-0.2-0.2")
  else:
    print "The graph is not connected."

  g = waxman(1000, 0.2, 0.2)
  if (g != None):
    writeGraphToFile(g, MyConf.WAXMAN + "waxman1000-0.2-0.2")
  else:
    print "The graph is not connected."
  
  g = barabasi_albert(100, 1)
  if (g != None):
    writeGraphToFile(g, MyConf.BA + "ba100-1")
  else:
    print "The graph is not connected."

  g = barabasi_albert(1000, 1)
  if (g != None):
    writeGraphToFile(g, MyConf.BA + "ba1000-1")
  else:
    print "The graph is not connected."

