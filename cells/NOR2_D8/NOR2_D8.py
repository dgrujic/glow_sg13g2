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

from glow_parcells import *
from glow_utils.symsim import Symsim
from glow_utils.symtech import SymTech
from sympy import Nor
from sympy.abc import x, y

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'NOR2_D8',
                 'pinList' : ['A', 'B', 'Y', 'VDD', 'VSS'],
                 'description' : 'NOR2 with drive strength x8'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    NOR2_D8 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])

    wn = SymTech.technology['invx2WN']
    # NMOS is 2*wn, and there are 3 PMOS in parallel, so the PMOS size is 4/3
    # Round so that it fits the manufacturing grid
    wp = round(wn * 1e8 * 4.0/3.0) / 1e8
    ngn = 4
    nor2_pun1 = nor2_pun_par('nor2_pun1', cellInfo['pinList'], {'WP' : wp})
    nor2_pun2 = nor2_pun_par('nor2_pun2', cellInfo['pinList'], {'WP' : wp})
    nor2_pun3 = nor2_pun_par('nor2_pun3', cellInfo['pinList'], {'WP' : wp})
    nor2_pun4 = nor2_pun_par('nor2_pun4', cellInfo['pinList'], {'WP' : wp})
    nor2_pun5 = nor2_pun_par('nor2_pun5', cellInfo['pinList'], {'WP' : wp})
    nor2_pun6 = nor2_pun_par('nor2_pun6', cellInfo['pinList'], {'WP' : wp})
    nor2_pdn1 = nor2_pdn_par('nor2_pdn1', cellInfo['pinList'], {'WN' : ngn * wn, 'NGN' : ngn})
    NOR2_D8.addElement([nor2_pdn1, nor2_pun1, nor2_pun2, nor2_pun3, nor2_pun4, nor2_pun5, nor2_pun6])
    
    # Flatten the circuit
    if genFlat:
        NOR2_D8_flat = NOR2_D8.flat()
    if anonimize:
        NOR2_D8_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Nor(x, y) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

