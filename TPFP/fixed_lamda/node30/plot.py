#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt

burstFile = './burst/01-0005.txt'
randomFile = './noise/01-0005.txt'

burst = []
random = []
for line in open(burstFile, 'r'):
  count = int(line)
  burst.append(count)
for line in open(randomFile, 'r'):
  count = int(line)
  random.append(count)

for i in range(len(burst)):
  burst[i] += random[i]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title('Traceroute Count')
ax.set_xlabel('Time[sec]')
ax.set_ylabel('Count')
plt.plot(random, 'ro-', label='random noise only')
plt.plot(burst, 'bv-', label='random noise + burst noise')
ax.legend(loc='best')

plt.savefig('output.png')
plt.show()
