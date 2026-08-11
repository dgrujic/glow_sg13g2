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
from sympy import And, Or
from sympy.abc import x, y, z
from glow_utils.symmosfet import SymNMOS, SymPMOS

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'OA21_D2',
                 'pinList' : ['A', 'B', 'C', 'Y', 'VDD', 'VSS'],
                 'description' : 'OA21 with drive strength x2'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    wn = 550e-9
    wp = 800e-9
    wpp = 650e-9
    wninv = SymTech.technology['invx2WN']
    wpinv = SymTech.technology['invx2WP']
    lmin = SymTech.technology['Lmin']

    OA21_D2 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])

    n0 = SymNMOS("N0", ['nabp', 'A', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n1 = SymNMOS("N0", ['nabp', 'B', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n2 = SymNMOS("N0", ['nabp', 'C', 'NY', 'VSS'], {'w' : wn, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['NY', 'C', 'VDD', 'VDD'], {'w' : wpp, 'l' : lmin })
    p1 = SymPMOS("P1", ['nabs', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P1", ['nabs', 'B', 'NY', 'VDD'], {'w' : wp, 'l' : lmin })

    inv1 = inv_par('inv1', ['NY', 'Y', 'VDD', 'VSS'], {'WN' : wninv, 'WP' : wpinv})
    OA21_D2.addElement([n0, n1, n2, p0, p1, p2, inv1])

    # Flatten the circuit
    if genFlat:
        OA21_D2_flat = OA21_D2.flat()
    if anonimize:
        OA21_D2_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ And(Or(x, y), z) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

