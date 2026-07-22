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
    cellInfo = { 'name' : 'INV_D12',
                 'pinList' : ['A', 'Y', 'VDD', 'VSS'],
                 'description' : 'Inverter with drive strength x12'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()
    ngates = 6
    wn = ngates * SymTech.technology['invx2WN']
    wp = ngates * SymTech.technology['invx2WP']

    INV_D12 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    inv12 = inv_par('inv12', ['A', 'Y', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp, 'NGN' : ngates, 'NGP' : ngates})
    INV_D12.addElement(inv12)

    # Flatten the circuit
    if genFlat:
        INV_D12_flat = INV_D12.flat()
    if anonimize:
        INV_D12_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(x) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

