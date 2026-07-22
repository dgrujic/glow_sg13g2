#!/bin/bash

########################################################################
#
# Copyright 2026 Dr. Dušan Grujić (dusan.grujic@etf.bg.ac.rs)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file cell_name"
    exit 1
fi

# Check if PDK_ROOT and PDK are set
if [ -z "$PDK_ROOT" ]; then
    echo "PDK_ROOT is not set"
    exit 1
fi
if [ -z "$PDK" ]; then
    echo "PDK is not set"
    exit 1
fi

echo -n "Checking $2"

echo -e -n "\t | GDSINFO "

# Perform checks with gdsinfo
gdsinfo $1 -c $2 --noref --errlay *,* --uselay 1,0 --uselay 5,0 --uselay 6,0 --uselay 8,0 --uselay 8,2 --uselay 8,25 --uselay 14,0 --uselay 31,0 --uselay 189,* --label VDD --label VSS --nolabel 'vdd!' --nolabel 'vss!' > /dev/null  2>&1

GDSINFO_STATUS=$?

if [ "$GDSINFO_STATUS" -eq 0 ]; then
    echo -e -n "OK"
else
    echo -e -n "ERROR"
fi

# Run DRC
echo -e -n "\t | DRC "
rm -rf drc

python3 $PDK_ROOT/$PDK/libs.tech/klayout/tech/drc/run_drc.py --path=$1 --topcell=$2 --no_density --run_dir=drc > /dev/null 2>&1

if grep -q "No DRC violations detected" drc/drc_run*.log; then
    DRC_STATUS=0
    echo -e -n "OK"
else
    DRC_STATUS=1
    echo -e -n "ERROR"
fi

# Run LVS
echo -e -n "\t | LVS "
rm -rf lvs

python3 $PDK_ROOT/$PDK/libs.tech/klayout/tech/lvs/run_lvs.py --layout=$1 --topcell=$2 --netlist=$2.cdl --run_dir=lvs > /dev/null 2>&1

if grep -q "PASS (netlists match)" lvs/lvs_run*.log; then
    LVS_STATUS=0
    echo -e -n "OK"
else
    LVS_STATUS=1
    echo -e -n "ERROR"
fi

if [ "$GDSINFO_STATUS" -eq 0 ] && [ "$DRC_STATUS" -eq 0 ] && [ "$LVS_STATUS" -eq 0 ]; then
    echo -e "\t | ALL OK"
    exit 0
else
    echo -e "\t | ERRORS"
    exit 1
fi




