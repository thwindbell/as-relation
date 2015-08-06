#! /bin/sh
#
# bat.sh
# Copyright (C) 2015 takayuki <takayuki@Takayukis-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.
#
TOPO="waxman/waxman100-0.2-0.2"
ENV="waxman100-0.2-0.2"
NUMBER_OF_AS="100"
echo ${ENV}
python CountDegree.py < ../topology/${TOPO} > ../env/${ENV}/degree
python NetworkSimulator.py ${TOPO} ${ENV} ${NUMBER_OF_AS} 100 100
# python TPFP.py ${ENV} ${NUMBER_OF_AS}
# python bestThreshold.py ${ENV} ${NUMBER_OF_AS}
# python AUC.py ${ENV} ${NUMBER_OF_AS}

TOPO="waxman/waxman1000-0.2-0.2"
ENV="waxman1000-0.2-0.2"
NUMBER_OF_AS="1000"
echo ${ENV}
python CountDegree.py < ../topology/${TOPO} > ../env/${ENV}/degree
python NetworkSimulator.py ${TOPO} ${ENV} ${NUMBER_OF_AS} 100 100
# python TPFP.py ${ENV} ${NUMBER_OF_AS}
# python bestThreshold.py ${ENV} ${NUMBER_OF_AS}
# python AUC.py ${ENV} ${NUMBER_OF_AS}

TOPO="ba/ba100-1"
ENV="ba100-1"
NUMBER_OF_AS="100"
echo ${ENV}
python CountDegree.py < ../topology/${TOPO} > ../env/${ENV}/degree
python NetworkSimulator.py ${TOPO} ${ENV} ${NUMBER_OF_AS} 100 100
# python TPFP.py ${ENV} ${NUMBER_OF_AS}
# python bestThreshold.py ${ENV} ${NUMBER_OF_AS}
# python AUC.py ${ENV} ${NUMBER_OF_AS}

TOPO="ba/ba1000-1"
ENV="ba1000-1"
NUMBER_OF_AS="1000"
echo ${ENV}
python CountDegree.py < ../topology/${TOPO} > ../env/${ENV}/degree
python NetworkSimulator.py ${TOPO} ${ENV} ${NUMBER_OF_AS} 100 100
# python TPFP.py ${ENV} ${NUMBER_OF_AS}
# python bestThreshold.py ${ENV} ${NUMBER_OF_AS}
# python AUC.py ${ENV} ${NUMBER_OF_AS}
