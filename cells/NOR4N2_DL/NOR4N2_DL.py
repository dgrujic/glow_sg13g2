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
from sympy import Nor, Not
from sympy.abc import x, y, z, w

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'NOR4N2_DL',
                 'pinList' : ['AN', 'BN', 'C', 'D', 'Y', 'VDD', 'VSS'],
                 'description' : 'NOR4 with inverted inputs A, B and weak drive strength'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    NOR4N2_DL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    nor4_pins = nor4_par.getTerminals()
    wp = 800e-9
    wn = 300e-9
    nor4 = nor4_par('nor4', nor4_pins, {'WP' : wp, 'WN' : wn})
    inv_wn = 150e-9
    inv_wp = 230e-9
    inv_inst1 = inv_par('inv_inst', ['AN', 'A', 'VDD', 'VSS'], {'WN' : inv_wn, 'WP' : inv_wp})
    inv_inst2 = inv_par('inv_inst', ['BN', 'B', 'VDD', 'VSS'], {'WN' : inv_wn, 'WP' : inv_wp})
    NOR4N2_DL.addElement([inv_inst1, inv_inst2, nor4])

    # Flatten the circuit
    if genFlat:
        NOR4N2_DL_flat = NOR4N2_DL.flat()
    if anonimize:
        NOR4N2_DL_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Nor(Not(x), Not(y), z, w) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)
