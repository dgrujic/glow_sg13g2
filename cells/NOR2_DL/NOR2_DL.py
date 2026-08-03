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
from glow_utils.symtech import SymTech

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'NOR2_DL',
                 'pinList' : ['A', 'B', 'Y', 'VDD', 'VSS'],
                 'description' : 'NOR2 with weak drive strength'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    NOR2_DL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wn = SymTech.technology['invx1WN'] / 2
    wp = 3 * wn / 2
    nor2 = nor2_par('nor2', cellInfo['pinList'], {"WP" : wp, "WN" : wn})
    NOR2_DL.addElement(nor2)

    # Flatten the circuit
    if genFlat:
        NOR2_DL_flat = NOR2_DL.flat()
    if anonimize:
        NOR2_DL_flat.anonimize()

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
