#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt

nodeList = [10, 100, 1000]
lambdaList = [10, 100, 1000, 10000]
accuracyNumbers = {}


for node in nodeList:
  accuracyNumbers[node] = []
  path = "./accuracyNumber/node%d" % (node)

  for line in open(path, 'r'):
    para = line.split(',')
    n = int(para[1])
    accuracyNumbers[node].append(n)

fig = plt.figure(figsize=(20, 12))
plt.rcParams['font.size'] = 30
plt.tick_params(pad=15)
plt.xticks([0,1,2,3],["10","100","1,000","10,000"])
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('$\lambda$', fontsize=40)
ax.set_ylabel('Number of ASes (AUC $\geq$ 0.9)', fontsize=40)
ax.set_ylim([8, 30])
ax.set_xlim([-0.1,3.1])
plt.plot(accuracyNumbers[10], 'o-', markersize=25, color="0.75", label="Total Number of ASes : 10")
plt.plot(accuracyNumbers[100], 'v-', markersize=25, color="0.5", label="Total Number of ASes : 100")
plt.plot(accuracyNumbers[1000], 's-', markersize=25, color="0.25", label="Total Number of ASes : 1,000")
ax.legend(loc="best")
plt.savefig("./plot/accuracyNumber.eps")
plt.show()
plt.close()
