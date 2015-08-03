#include "Network.cpp"
#include <time.h>
#include <cstdlib>

int main() {
  string filename = "./topology/dataset_100a.txt";
  int start = clock();
  int elapsed = 0;
  Network myNet = Network::Network();
  myNet.loadFile(filename);
  myNet.searchTopAs();
  myNet.exchangeRouteingTable();
  myNet.distributeNetAddr();
  
  elapsed = clock() - start;
  cout << "routing finished" << endl;
  cout << ((double)elapsed/(double)CLOCKS_PER_SEC) << "SEC" << endl;

  AS *node;
  map<int, AS &>::iterator  itr = myNet.asDict.begin();
  int i, j, startTime;
  unsigned int dstNet, dstHost, dstAddr, srcAddr;
  while (itr != myNet.asDict.end()) {
    node = &(itr->second);
    for (i=0; i<300; i++) {
      startTime = i * 1000;
      for (j=0; j<80; j++) {
        dstNet = rand()%100+1;
        dstHost = rand()%254+1;
        dstAddr = dstNet<<16 | dstHost;
        srcAddr = node->networkAddress;
        elapsed = myNet.traceroute(srcAddr, dstAddr, startTime, 3);
      }
    }
    itr++;
  }

  elapsed = clock() - start;
  cout << "traceroute finished" << endl;
  cout << ((double)elapsed/(double)CLOCKS_PER_SEC) << "SEC" << endl;
  return 0;
}
