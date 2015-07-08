#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
  lines = []
  mapping = {}
  seq = 1

  for line in sys.stdin:
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    if line.startswith('#'):
      lines.append(line)
      continue
    else:
      para = line.split('|')
      if len(para) != 3:
        lines.append(line)
        continue

      node1 = int(para[0])
      node2 = int(para[1])
      connectionType = int(para[2])
      if node1 not in mapping:
        mapping[node1] = seq
        seq += 1
      if node2 not in mapping:
        mapping[node2] = seq
        seq += 1
      line = "%d|%d|%d" % (mapping[node1], mapping[node2], connectionType)
    lines.append(line)
  for line in lines:
    print line
