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

from pathlib import Path
import importlib
import os
import sys

from glow_parcells import *
from glow_utils.symsim import Symsim
from glow_utils.symtech import SymTech
from sympy import And
from sympy.abc import x, y, z

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'AND3_DL',
                 'pinList' : ['A', 'B', 'C', 'Y', 'VDD', 'VSS'],
                 'description' : 'AND3 with weak drive strength'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AND3_DL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wn = 330e-9
    wp = 300e-9
    nand3_inst = nand3_par('nand3', ['A', 'B', 'C', 'NO', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
    inv_wn = SymTech.technology['invx1WN'] / 2
    inv_wp = SymTech.technology['invx1WP'] / 2
    inv_inst = inv_par('inv_inst', ['NO', 'Y', 'VDD', 'VSS'], {'WN' : inv_wn, 'WP' : inv_wp})
    AND3_DL.addElement([nand3_inst, inv_inst])

    # Flatten the circuit
    if genFlat:
        AND3_DL_flat = AND3_DL.flat()
    if anonimize:
        AND3_DL_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ And(x, y, z) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

