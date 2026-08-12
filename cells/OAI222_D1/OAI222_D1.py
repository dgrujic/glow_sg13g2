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
from sympy.abc import x, y, z, w, u, v
from glow_utils.symmosfet import SymNMOS, SymPMOS

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'OAI222_D1',
                 'pinList' : ['A', 'B', 'C', 'D', 'E', 'F', 'Y', 'VDD', 'VSS'],
                 'description' : 'OAI222 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    wn = 1000e-9
    wp = 1270e-9
    lmin = SymTech.technology['Lmin']

    OAI222_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])

    n0 = SymNMOS("N0", ['nefp', 'F', 'Y', 'VSS'], {'w' : wn, 'l' : lmin })
    n1 = SymNMOS("N1", ['nefp', 'E', 'Y', 'VSS'], {'w' : wn, 'l' : lmin })
    n2 = SymNMOS("N2", ['nabp', 'A', 'nefp', 'VSS'], {'w' : wn, 'l' : lmin })
    n3 = SymNMOS("N3", ['nabp', 'B', 'nefp', 'VSS'], {'w' : wn, 'l' : lmin })
    n4 = SymNMOS("N4", ['nabp', 'D', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n5 = SymNMOS("N5", ['nabp', 'C', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    
    # Pull-up network
    p0 = SymPMOS("P0", ['nefs', 'F', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1 = SymPMOS("P1", ['Y', 'E', 'nefs', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P2", ['ncds', 'D', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p3 = SymPMOS("P3", ['Y', 'C', 'ncds', 'VDD'], {'w' : wp, 'l' : lmin })
    p4 = SymPMOS("P4", ['nabs', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p5 = SymPMOS("P5", ['nabs', 'A', 'Y', 'VDD'], {'w' : wp, 'l' : lmin })

    OAI222_D1.addElement([n0, n1, n2, n3, n4, n5, p0, p1, p2, p3, p4, p5])

    # Flatten the circuit
    if genFlat:
        OAI222_D1_flat = OAI222_D1.flat()
    if anonimize:
        OAI222_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(And(Or(x, y), Or(z, w), Or(u, v))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

