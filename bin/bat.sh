#! /bin/sh
#
# bat.sh
# Copyright (C) 2015 takayuki <takayuki@Takayukis-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.
#

TOPO="waxman/waxman1000-0.2-0.2"
ENV="waxman1000-0.2-0.2"
NUMBER_OF_AS="1000"
# python NetworkSimulator.py ${TOPO} ${ENV} ${NUMBER_OF_AS} 100 100
python TPFP.py ${ENV} ${NUMBER_OF_AS}
python bestThreshold.py ${ENV} ${NUMBER_OF_AS}
python AUC.py ${ENV} ${NUMBER_OF_AS}

TOPO="ba/ba100-1"
ENV="ba100-1"
NUMBER_OF_AS="100"
python NetworkSimulator.py ${TOPO} ${ENV} ${NUMBER_OF_AS} 100 100
python TPFP.py ${ENV} ${NUMBER_OF_AS}
python bestThreshold.py ${ENV} ${NUMBER_OF_AS}
python AUC.py ${ENV} ${NUMBER_OF_AS}

TOPO="ba/ba1000-1"
ENV="ba1000-1"
NUMBER_OF_AS="1000"
python NetworkSimulator.py ${TOPO} ${ENV} ${NUMBER_OF_AS} 100 100
python TPFP.py ${ENV} ${NUMBER_OF_AS}
python bestThreshold.py ${ENV} ${NUMBER_OF_AS}
python AUC.py ${ENV} ${NUMBER_OF_AS}

