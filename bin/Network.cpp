/*
 * Network.cpp
 * Copyright (C) 2015 takayuki <takayuki@Takayukis-MacBook-Pro.local>
 *
 * Distributed under terms of the MIT license.
 */

#include "AS.cpp"
#include <fstream>
#include <algorithm>
using namespace std;

class Network {
public:
  map<unsigned int, int> addrToAsNumber;
  map<int, AS *> asDict;
  vector<AS *> asList;
  vector<int> topAsNumbers;
  
  ~Network() {
    this->addrToAsNumber.clear();
    this->asDict.clear();
    this->topAsNumbers.clear();
    for (int i=0; i<asList.size(); i++) {
      delete asList[i];
      asList[i] = NULL;
    }
    this->asList.clear();
  }

  AS *createAS() {
    AS *a = new AS();
    asList.push_back(a);
    return a;
  }

  int loadFile(string &filename) {
    map<int, AS *>::iterator itr;
    string str;
    int i, node1, node2, connectionType;
    AS *provider, *customer, *peer1, *peer2;
    AS *node;

    ifstream fin(filename);
    if (!fin) {
      cout << "error : open input file" << endl;
      return -1;
    }

    fin.unsetf(ios::skipws);
    while (getline(fin, str)) {
      vector<string> para = AS::split(str, "|");
      if (para.size() != 3) {
        continue;
      }

      node1 = stoi(para[0]);
      node2 = stoi(para[1]);
      connectionType = stoi(para[2]);

      itr = asDict.find(node1);
      if (itr == asDict.end()) {
        node = createAS();
        *node = AS::AS(node1);
        asDict.insert(pair<int, AS *>(node1, node));
      }
      itr = asDict.find(node2);
      if (itr == asDict.end()) {
        node = createAS();
        *node = AS::AS(node2);
        asDict.insert(pair<int, AS *>(node2, node));
      }

      if (connectionType == -1) {
        itr = asDict.find(node1);
        provider = itr->second;
        itr = asDict.find(node2);
        customer = itr->second;
        provider->addCustomerAS(*customer);
        customer->addProviderAS(*provider);
      } else if (connectionType == 0) {
        itr = asDict.find(node1);
        peer1 = itr->second;
        itr = asDict.find(node2);
        peer2 = itr->second;
        peer1->addPeerAS(*peer2);
        peer2->addPeerAS(*peer1);
      }
      sort(asList.begin(), asList.end());
    }

    for (int i=0; i<asList.size(); i++) {
      asList[i]->init();
    }
    return 0;
  }

  vector<int> &searchTopAs() {
    map<int, AS *>::iterator itr = this->asDict.begin();
    while (itr != this->asDict.end()) {
      if (itr->second->providerNodes.size() == 0) {
        this->topAsNumbers.push_back(itr->first);
      }
      itr++;
    }
    sort(this->topAsNumbers.begin(), this->topAsNumbers.end());
    return this->topAsNumbers;
  }

  void exchangeRouteingTable() {
    map<int, AS *>::iterator itrDict;
    AS *node;
    int i;
    
    for (i=0; i<topAsNumbers.size(); i++) {
      cout << "TopAsNumbers:" << topAsNumbers[i] << endl;
      itrDict = this->asDict.find(topAsNumbers[i]);
      node = itrDict->second;
      node->mergeCustomerTable();
    }

    for (i=0; i<asList.size(); i++) {
      cout << "AllAs:" << asList[i]->asNumber << endl; 
      node = asList[i];
      node->mergePeerTable();
    }

    for (i=0; i<topAsNumbers.size(); i++) {
      cout << "TopAsNumbers:" << topAsNumbers[i] << endl;
      itrDict = this->asDict.find(topAsNumbers[i]);
      node = itrDict->second;
      node->transit();
    }
  }

  void distributeNetAddr() {
    map<int, AS *>::iterator itr = this->asDict.begin();
    AS *node;
    while (itr != this->asDict.end()) {
      node = itr->second;
      node->networkAddress = (unsigned int)(node->asNumber<<16);
      node->netmask = 0xFFff0000;
      this->addrToAsNumber.insert(
          pair<unsigned int, int>(node->networkAddress, node->asNumber));
      itr++;
    }
  }

  int traceroute(unsigned int src, unsigned int dst,
      unsigned int startTime=0, int packets=3) {
    unsigned int delay = 13;
    unsigned int elapsed = 0;
    unsigned int mask = 0xFFff0000;
    unsigned int srcNet, dstNet;
    int srcAsNumber, dstAsNumber, i, nexthop;
    AS *current;
    Route *r;
    map<unsigned int, int>::iterator itrAddr;
    map<int, AS *>::iterator itrDict;
    map<int, Route *>::iterator itrTable;
    
    srcNet = src & mask;
    dstNet = dst & mask;
    itrAddr = this->addrToAsNumber.find(srcNet);
    srcAsNumber = itrAddr->second;
    itrAddr = this->addrToAsNumber.find(dstNet);
    dstAsNumber = itrAddr->second;

    itrDict = this->asDict.find(srcAsNumber);
    current = itrDict->second;
    while (1) {
      for (i=0; i<packets; i++) {
        elapsed += delay;
        current->addLog(src, dst, startTime + elapsed);
      }
      if ((itrTable = current->customerTable.find(dstAsNumber))
            != current->customerTable.end()) {
        r = itrTable->second;
      } else if ((itrTable = current->peerTable.find(dstAsNumber))
          != current->peerTable.end()) {
        r = itrTable->second;
      } else if ((itrTable = current->providerTable.find(dstAsNumber))
          != current->providerTable.end()) {
        r = itrTable->second;
      } else {
        return -1;
      }
      nexthop = r->nexthop;
      if (nexthop == -1) {
        break;
      } else {
        itrDict = this->asDict.find(nexthop);
        current = itrDict->second;
      }
    }
    return elapsed;
  }

  void crearAsLog() {
    map<int, AS *>::iterator itr = this->asDict.begin();
    while (itr != this->asDict.end()) {
      itr->second->clearLog();
      itr++;
    }
  }

  void toString() {
    map<int, AS *>::iterator itr = asDict.begin();
    while (itr != asDict.end()) {
      itr->second->toString();
      itr->second->printLog();
      itr++;
    }
  }
};

int main() {
  string filename = "./topology/test.txt";
  Network myNet;
  myNet.loadFile(filename);
  myNet.searchTopAs();
  for (int i=0; i<myNet.topAsNumbers.size(); i++) {
    cout << "TOP AS : " << myNet.topAsNumbers[i] << endl;
  }
  myNet.exchangeRouteingTable();
  myNet.distributeNetAddr();
  myNet.toString();

  myNet.traceroute((7<<16 | 1), (14<<16 | 1), 0, 3);

  return 0;
}
