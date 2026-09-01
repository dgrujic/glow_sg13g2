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
from sympy import Not
from sympy.abc import x

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'DLY2_D1',
                 'pinList' : ['A', 'Y', 'VDD', 'VSS'],
                 'description' : 'Delay x2 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()
    wn = 600e-9
    wp = 900e-9
    lch = 2 * SymTech.technology['Lmin']

    DLY2_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    inv1 = inv_par('inv1', ['A', 'n0', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
    inv2 = inv_par('inv2', ['n0', 'n1', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp, 'L' : lch})
    inv3 = inv_par('inv3', ['n1', 'n2', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp, 'L' : lch})
    inv4 = inv_par('inv4', ['n2', 'Y', 'VDD', 'VSS'], {'WN' : wn / 2, 'WP' : wp})
    DLY2_D1.addElement([inv1, inv2, inv3, inv4])

    # Flatten the circuit
    if genFlat:
        DLY2_D1_flat = DLY2_D1.flat()
    if anonimize:
        DLY2_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ x ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

