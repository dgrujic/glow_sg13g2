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
from sympy import Or
from sympy.abc import x, y, z, w

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'OR4_D1',
                 'pinList' : ['A', 'B', 'C', 'D', 'Y', 'VDD', 'VSS'],
                 'description' : 'OR4 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    OR4_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wn = 220e-9
    wp = 3 * wn
    nor4_inst = nor4_par('nor4', ['A', 'B', 'C', 'D', 'NO', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
    inv_wn = SymTech.technology['invx1WN']
    inv_wp = SymTech.technology['invx1WP']
    inv_inst = inv_par('inv_inst', ['NO', 'Y', 'VDD', 'VSS'], {'WN' : inv_wn, 'WP' : inv_wp})
    OR4_D1.addElement([nor4_inst, inv_inst])

    # Flatten the circuit
    if genFlat:
        OR4_D1_flat = OR4_D1.flat()
    if anonimize:
        OR4_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Or(x, y, z, w) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)
