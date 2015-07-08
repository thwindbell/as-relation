#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import collections

if __name__ == '__main__':
  counter = collections.defaultdict(int)

  for line in sys.stdin:
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    if line.startswith('#'):
      continue
    else:
      para = line.split('|')
      if len(para) != 3:
        continue

      node1 = int(para[0])
      node2 = int(para[1])
      connection_type = int(para[2])
      if (connection_type) == -1:
        counter[node1] += 1
        counter[node2] += 1
      else:
        counter[node1] += 0
        counter[node2] += 0

  for node in sorted(counter.keys()):
    degree = counter[node]
    print "%d, %d" % (node, degree)
