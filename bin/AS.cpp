#include <iostream>
#include <string>
#include <vector>
#include <map>

using namespace std;

class Route {
public:
  int nexthop;
  int distance;

  Route() {
    nexthop = -1;
    distance = 0;
  }

  Route(const Route &r) {
    nexthop = r.nexthop;
    distance = r.distance;
  }

  Route &operator=(const Route &r) {
    return *this;
  }
};

class Log {
public:
  int time;
  unsigned int src;
  unsigned int dst;

  Log() {
    time = 0;
    src = 0;
    dst = 0;
  }

  Log(const Log &l) {
    time = l.time;
    src = l.src;
    dst = l.dst;
  }

  Log &operator=(const Log &l) {
    return *this;
  }
};
bool operator<(const Log &a, const Log &b)
{
  return a.time < b.time;
}
bool operator>(const Log &a, const Log &b)
{
  return a.time > b.time;
}
bool operator==(const Log &a, const Log &b)
{
  if (a.time == b.time &&
      a.src == b.src &&
      a.dst == b.dst) {
    return true;
  } else {
    return false;
  }
}
bool operator!=(const Log &a, const Log &b)
{
  if (a.time != b.time ||
      a.src != b.src ||
      a.dst != b.dst) {
    return true;
  } else {
    return false;
  }
}

class AS {
public:
  int asNumber;
  unsigned int networkAddress;
  unsigned int netmask;
  map<int, Route *> customerTable;
  map<int, Route *> peerTable;
  map<int, Route *> providerTable;
  map<int, AS &> customerNodes;
  map<int, AS &> peerNodes;
  map<int, AS &> providerNodes;
  map<int, AS &> allCustomerNodes;
  vector<Log *> tracerouteLog;
  vector<Route *> allRoutes;

  AS() {
    asNumber = -1;
  }

  AS(int n) {
    asNumber = n;
    networkAddress = 0x0A000000;
    netmask = 0xFFff0000;
    allCustomerNodes.insert(pair<int, AS &>(asNumber, *this));
  }

  ~AS() {
    customerTable.clear();
    peerTable.clear();
    providerTable.clear();

    for (int i=0; i<tracerouteLog.size(); i++) {
      Log *l = tracerouteLog[i];
      tracerouteLog[i] = NULL;
      delete l;
    }
    for (int i=0; i<allRoutes.size(); i++) {
      Route *r = allRoutes[i];
      allRoutes[i] = NULL;
      delete r;
    }
    
    tracerouteLog.clear();
    allRoutes.clear();
  }

  void init() {
    Route *r = createRoute();
    r->nexthop = -1;
    r->distance = 0;
    customerTable.insert(pair<int, Route *>(asNumber, r));
  }

  void addNode(AS &node, map<int, AS &> &list) {
    list.insert(pair<int, AS &>(node.asNumber, node));
  }
  void addProviderAS(AS &node) {
    this->addNode(node, this->providerNodes);
  }
  void addPeerAS(AS &node) {
    this->addNode(node, this->peerNodes);
  }
  void addCustomerAS(AS &node) {
    this->addNode(node, this->customerNodes);
  }

  void mergeTable(map<int, Route *> &originalTable, 
      map<int, Route *> &additionalTable, int dataSource) {
    map<int, Route *>::iterator itrO;
    map<int, Route *>::iterator itrA;
    int dst = -1;
    Route *original, *additional;

    for (itrA=additionalTable.begin(); itrA!=additionalTable.end(); itrA++) {
      dst = itrA->first;
      additional = itrA->second;
      itrO = originalTable.find(dst);
      if (itrO != originalTable.end()) {
        original = itrO->second;
        if (additional->distance+1 < original->distance) {
          original->nexthop = dataSource;
          original->distance = additional->distance + 1;
        }
      } else {
        Route *r = createRoute();
        r->nexthop = dataSource;
        r->distance = additional->distance + 1;
        originalTable.insert(pair<int, Route *>(dst, r));
      }
    } 
  }

  map<int, Route *> &mergeCustomerTable() {
    if (customerTable.size() != 1) {
      return customerTable;
    }

    map<int, AS &>::iterator itr = customerNodes.begin();
    int customerNumber = -1;
    AS *customerNode;
    while (itr != customerNodes.end()) {
      customerNumber = itr->first;
      customerNode = &itr->second;
      map<int, Route *> additionalTable = customerNode->mergeCustomerTable();
      this->mergeTable(customerTable, additionalTable, customerNumber);
      itr++;
    }
    return customerTable;
  }

  map<int, Route *> &mergePeerTable() {
    map<int, AS &>::iterator itr = peerNodes.begin();
    int peerNumber = -1;
    AS *peerNode;
    while (itr != peerNodes.end()) {
      peerNumber = itr->first;
      peerNode = &itr->second;
      mergeTable(peerTable, peerNode->customerTable, peerNumber);
      itr++;
    }
    return peerTable;
  }

  void transit() {
    map<int, AS &>::iterator itr = this->customerNodes.begin();
    int customerNumber = -1;
    AS *customerNode;
    while (itr != this->customerNodes.end()) {
      customerNumber = itr->first;
      customerNode = &itr->second;
      customerNode->mergeTable(
          customerNode->providerTable, this->providerTable, this->asNumber);
      customerNode->mergeTable(
          customerNode->providerTable, this->peerTable, this->asNumber);
      customerNode->mergeTable(
          customerNode->providerTable, this->customerTable, this->asNumber);
      customerNode->transit();
      itr++;
    }
  }

  map<int, AS &> &mergeCustomerNodes() {
    if (allCustomerNodes.size() != 1) {
      return allCustomerNodes;
    }

    map<int, AS &>::iterator itr = customerNodes.begin();
    while (itr != customerNodes.end()) {
      AS customerNode = itr->second;
      map<int, AS &>::iterator itr_c = customerNode.customerNodes.begin();
      while (itr_c != customerNode.customerNodes.end()) {
        int key = itr_c->first;
        AS value = itr_c->second;
        this->allCustomerNodes.insert(pair<int, AS &>(key, value));
        itr_c++;
      }
      itr++;
    }
    return this->allCustomerNodes;
  }

  Route *createRoute() {
    Route *r = new Route();
    this->allRoutes.push_back(r);
    return r;
  }

  void addLog(int src, int dst, int time) {
    Log *l = new Log();
    l->src = src;
    l->dst = dst;
    l->time = time;
    this->tracerouteLog.push_back(l);
  }

  void clearLog() {
    this->tracerouteLog.clear();
  }

  void printLog() {
    cout << "AS Number : " << this->asNumber << endl;
    vector<Log *>::iterator itr = this->tracerouteLog.begin();
    string strSrc, strDst;
    Log *l;
    while (itr != this->tracerouteLog.end()) {
      l = *itr;
      strSrc = AS::intAddrToStr(l->src);
      strDst = AS::intAddrToStr(l->dst);
      cout << "\t" << l->time << ", " << strSrc << ", " << strDst << endl;
      itr++;
    }
  }

  bool isHostAddress(int addr) {
    if ((addr & this->netmask) == this->networkAddress) {
      return true;
    } else {
      return false;
    }
  }

  void toString() {
    cout << "AS Number : " << this->asNumber << endl;;
    cout << "\tNetwork Address : "
      << AS::intAddrToStr(this->networkAddress) << endl;
    cout << "\tNetmask : " << AS::intAddrToStr(this->netmask) << endl;

    cout << "\tProvider Nodes : " << endl;
    map<int, AS &>::iterator itr_n = this->providerNodes.begin();
    while (itr_n != this->providerNodes.end()) {
      cout << "\t\t" << itr_n->second.asNumber << endl;
      itr_n++;
    }
    cout << endl;

    cout << "\tPeer Nodes : " << endl;
    itr_n = this->peerNodes.begin();
    while (itr_n != this->peerNodes.end()) {
      cout << "\t\t" << itr_n->second.asNumber << endl;
      itr_n++;
    }
    cout << endl;

    cout << "\tCustomer Nodes : " << endl;
    itr_n = this->customerNodes.begin();
    while (itr_n != this->customerNodes.end()) {
      cout << "\t\t" << itr_n->second.asNumber << endl;
      itr_n++;
    }
    cout << endl;

    cout << "\tProvider Table : " << endl;
    cout << "\t\tDestination, Nexthop, Distance" << endl;
    map<int, Route *>::iterator itr_t = this->providerTable.begin();
    while (itr_t != this->providerTable.end()) {
      cout << "\t\t" << itr_t->first << ", "
        << itr_t->second->nexthop << ", "
        << itr_t->second->distance << endl;
      itr_t++;
    }
    cout << endl;

    cout << "\tPeer Table : " << endl;
    cout << "\t\tDestination, Nexthop, Distance" << endl;
    itr_t = this->peerTable.begin();
    while (itr_t != this->peerTable.end()) {
      cout << "\t\t" << itr_t->first << ", "
        << itr_t->second->nexthop << ", "
        << itr_t->second->distance << endl;
      itr_t++;
    }
    cout << endl;

    cout << "\tCustomer Table : " << endl;
    cout << "\t\tDestination, Nexthop, Distance" << endl;
    itr_t = this->customerTable.begin();
    while (itr_t != this->customerTable.end()) {
      cout << "\t\t" << itr_t->first << ", "
        << itr_t->second->nexthop << ", "
        << itr_t->second->distance << endl;
      itr_t++;
    }
    cout << endl;
  }

  static vector<string> split(const string &str, const string &delim){
    vector<string> res;
    size_t current = 0, found, delimlen = delim.size();
    while((found = str.find(delim, current)) != string::npos){
      res.push_back(string(str, current, found - current));
      current = found + delimlen;
    }
    res.push_back(string(str, current, str.size() - current));
    return res;
  }
  
  static unsigned int strAddrToInt(const string &addr) {
    vector<string> bytes;
    unsigned int intAddr = 0;
    bytes = split(addr, ".");
    vector<string>::iterator itr = bytes.begin();
    while (itr != bytes.end()) {
      intAddr = intAddr << 8;
      cout << *itr << endl;
      intAddr += stoi(*itr);
      itr++;
    }
    return intAddr; 
  }
  static string intAddrToStr(unsigned int addr) {
    unsigned int bytes[4];
    char buf[256];
    string strAddr;
    int i;
    for (i=0; i<4; i++) {
      bytes[i] = (unsigned int)(addr & 0x000000FF);
      addr = addr >> 8;
    }
    sprintf(buf, "%d.%d.%d.%d", bytes[3], bytes[2], bytes[1], bytes[0]);
    strAddr = string(buf);
    return strAddr;
  }
};

bool operator<(const AS &a, const AS &b)
{
  return a.asNumber < b.asNumber;
}
bool operator>(const AS &a, const AS &b)
{
  return a.asNumber > b.asNumber;
}
bool operator==(const AS &a, const AS &b)
{
  return a.asNumber == b.asNumber;
}
bool operator!=(const AS &a, const AS &b)
{
  return a.asNumber != b.asNumber;
}
/*
int main() {
  AS asList[14];
  int i;
  for (i=0; i<14; i++) {
    AS node = AS(i);
    asList[i] = node;
  }
  for (i=0; i<14; i++) {
    asList[i].init();
  }
  asList[0].addPeerAS(asList[1]);
  asList[1].addPeerAS(asList[0]);
  
  asList[0].addCustomerAS(asList[2]);
  asList[0].addCustomerAS(asList[3]);
  asList[1].addCustomerAS(asList[4]);
  asList[1].addCustomerAS(asList[5]);
  asList[2].addProviderAS(asList[0]);
  asList[3].addProviderAS(asList[0]);
  asList[4].addProviderAS(asList[1]);
  asList[5].addProviderAS(asList[1]);
  
  asList[2].addCustomerAS(asList[6]);
  asList[2].addCustomerAS(asList[7]);
  asList[3].addCustomerAS(asList[8]);
  asList[3].addCustomerAS(asList[9]);
  asList[4].addCustomerAS(asList[10]);
  asList[4].addCustomerAS(asList[11]);
  asList[5].addCustomerAS(asList[12]);
  asList[5].addCustomerAS(asList[13]);
  asList[6].addProviderAS(asList[2]);
  asList[7].addProviderAS(asList[2]);
  asList[8].addProviderAS(asList[3]);
  asList[9].addProviderAS(asList[3]);
  asList[10].addProviderAS(asList[4]);
  asList[11].addProviderAS(asList[4]);
  asList[12].addProviderAS(asList[5]);
  asList[13].addProviderAS(asList[5]);
  
  for (i=0; i<14; i++) {
    asList[i].toString();
  }

  asList[0].mergeCustomerTable();
  asList[1].mergeCustomerTable();

  for (i=0; i<14; i++) {
    asList[i].mergePeerTable();
  }

  asList[0].transit();
  asList[1].transit();

  for (i=0; i<14; i++) {
    asList[i].toString();
  }
  
  return 0;
}
*/
