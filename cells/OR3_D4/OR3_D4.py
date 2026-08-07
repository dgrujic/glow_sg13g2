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
from sympy.abc import x, y, z

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'OR3_D4',
                 'pinList' : ['A', 'B', 'C', 'Y', 'VDD', 'VSS'],
                 'description' : 'OR3 with drive strength x4'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    OR3_D4 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wn = 800e-9
    wp = 3 * wn
    ng_nor = 2
    nor3_inst = nor3_par('nor3', ['A', 'B', 'C', 'NO', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp, 'NGN' : ng_nor, 'NGP' : ng_nor})
    inv_wn = 3 * SymTech.technology['invx2WP'] / 2
    inv_wp = 2 * SymTech.technology['invx2WP']
    ng = 3
    inv_inst = inv_par('inv_inst', ['NO', 'Y', 'VDD', 'VSS'], {'WN' : inv_wn, 'WP' : inv_wp, 'NGN' : ng, 'NGP' : ng})
    OR3_D4.addElement([nor3_inst, inv_inst])

    # Flatten the circuit
    if genFlat:
        OR3_D4_flat = OR3_D4.flat()
    if anonimize:
        OR3_D4_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Or(x, y, z) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

