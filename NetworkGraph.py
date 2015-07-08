#!/usr/bin/python
# -*- coding: utf-8 -*-

import Network

myNet = Network.Network()
myNet.loadRelationFile('./modified_dataset/dataset_3000a.txt')
myNet.searchTopAS()
myNet.exchangeRoutingTable()
myNet.distributeNetAddr()
myNet.drawGraph()
