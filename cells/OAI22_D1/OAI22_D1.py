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
from sympy import Not, And, Or
from sympy.abc import x, y, z, w
from glow_utils.symmosfet import SymNMOS, SymPMOS

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'OAI22_D1',
                 'pinList' : ['A', 'B', 'C', 'D', 'Y', 'VDD', 'VSS'],
                 'description' : 'OAI22 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    wn = 900e-9
    wp = 1270e-9
    wpp = wp
    lmin = SymTech.technology['Lmin']

    OAI22_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])

    n0 = SymNMOS("N0", ['nabp', 'C', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n1 = SymNMOS("N1", ['nabp', 'D', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n2 = SymNMOS("N2", ['nabp', 'A', 'Y', 'VSS'], {'w' : wn, 'l' : lmin })
    n3 = SymNMOS("N3", ['nabp', 'B', 'Y', 'VSS'], {'w' : wn, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['nabs', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1 = SymPMOS("P1", ['nabs', 'B', 'Y', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P2", ['ncds', 'C', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p3 = SymPMOS("P3", ['ncds', 'D', 'Y', 'VDD'], {'w' : wpp, 'l' : lmin })

    OAI22_D1.addElement([n0, n1, n2, n3, p0, p1, p2, p3])

    # Flatten the circuit
    if genFlat:
        OAI22_D1_flat = OAI22_D1.flat()
    if anonimize:
        OAI22_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(And(Or(x, y), Or(z, w))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

