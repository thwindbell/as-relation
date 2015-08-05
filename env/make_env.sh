#! /bin/sh
#
# make_env.sh
# Copyright (C) 2015 takayuki <takayuki@Takayukis-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.
#

BASE=$*
echo "$BASE"
mkdir ${BASE}
mkdir ${BASE}/attack_file/
mkdir ${BASE}/threshold/
mkdir ${BASE}/bestTrhreshold/
mkdir ${BASE}/AUC/
echo "*" > ${BASE}/.gitignore
