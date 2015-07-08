#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt

inputFile = './auclist.txt'

auc = []
degree = []
for line in open(inputFile, 'r'):
  para = line.split(',')
  auc.append(float(para[1]))
  degree.append(float(para[2]))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#ax.set_title('AUC', fontsize=24)
ax.set_xlabel('Degree of AS', fontsize=16)
#ax.set_xlim([0, 13])
#ax.set_ylim([0.90, 1.00])
ax.set_ylabel('AUC', fontsize=16)
plt.plot(degree, auc, 'ro', markersize=15)

for i, item in enumerate(ax.get_xticklabels()):
  fontsize=16
  item.set_fontsize(fontsize)
for i, item in enumerate(ax.get_yticklabels()):
  fontsize=16
  item.set_fontsize(fontsize)

plt.savefig('auc.eps')
plt.show()
