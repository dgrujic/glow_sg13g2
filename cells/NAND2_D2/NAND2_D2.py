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
from sympy import Nand
from sympy.abc import x, y

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'NAND2_D2',
                 'pinList' : ['A', 'B', 'Y', 'VDD', 'VSS'],
                 'description' : 'NAND2 with drive strength x2'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()
    wp = SymTech.technology['invx2WP']
    wn = 725e-9

    NAND2_D2 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    nand2_pun1 = nand2_pun_par('nand2_pun1', cellInfo['pinList'], {'WN' : wn, 'WP' : wp})
    nand2_pdn1 = nand2_pdn_par('nand2_pdn1', cellInfo['pinList'], {'WN' : wn, 'WP' : wp})
    nand2_pdn2 = nand2_pdn_par('nand2_pdn2', cellInfo['pinList'], {'WN' : wn, 'WP' : wp})
    NAND2_D2.addElement([nand2_pdn1, nand2_pdn2, nand2_pun1])

    # Flatten the circuit
    if genFlat:
        NAND2_D2_flat = NAND2_D2.flat()
    if anonimize:
        NAND2_D2_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Nand(x, y) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

