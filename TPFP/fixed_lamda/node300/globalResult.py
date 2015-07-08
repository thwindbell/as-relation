#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt

attackFile = './globalDetectorResult.txt'
noiseFile = './globalDetectorResultWithNoise.txt'

randomTP = []
randomFP = []
burstTP = []
burstFP = []
for line in open(attackFile, 'r'):
  para = line.split(',')
  randomTP.append(float(para[0]))
  randomFP.append(float(para[1]))
for line in open(noiseFile, 'r'):
  para = line.split(',')
  burstTP.append(float(para[0]))
  burstFP.append(float(para[1]))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title('ROC Curve')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.0])
plt.plot(randomFP, randomTP, 'ro-', linewidth=3, markersize=10, label='random noise only')
plt.plot(burstFP, burstTP, 'bv-', linewidth=3, markersize=10, label='random noise + burst noise')
ax.legend(loc='best')

plt.savefig('output.png')
plt.show()
