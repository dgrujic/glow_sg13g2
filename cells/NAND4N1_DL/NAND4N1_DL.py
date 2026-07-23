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
from sympy import Nand, Not
from sympy.abc import x, y, z, w

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'NAND4N1_DL',
                 'pinList' : ['AN', 'B', 'C', 'D', 'Y', 'VDD', 'VSS'],
                 'description' : 'NAND4 with inverted input A and weak drive strength'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    NAND4N1_DL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wn = 360e-9
    wp = 300e-9
    nand4_cell_pins = nand4_par.getTerminals()
    nand4_inst = nand4_par('nand4', nand4_cell_pins, {'WN' : wn, 'WP' : wp})
    inv_wn = 150e-9
    inv_wp = 230e-9
    inv_inst = inv_par('inv_inst', ['AN', 'A', 'VDD', 'VSS'], {'WN' : inv_wn, 'WP' : inv_wp})
    NAND4N1_DL.addElement([nand4_inst, inv_inst])

    # Flatten the circuit
    if genFlat:
        NAND4N1_DL_flat = NAND4N1_DL.flat()
    if anonimize:
        NAND4N1_DL_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Nand(Not(x), y, z, w) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

