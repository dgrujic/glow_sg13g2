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
    cellInfo = { 'name' : 'OAI2N1_D1',
                 'pinList' : ['A', 'B', 'C', 'Y', 'VDD', 'VSS'],
                 'description' : 'OAI2N1 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    wn = 340e-9
    wns = 700e-9
    wps = 980e-9
    wp = 400e-9
    lmin = SymTech.technology['Lmin']

    OAI2N1_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])

    n0 = SymNMOS("N0", ['Y', 'ny', 'nc', 'VSS'], {'w' : wns, 'l' : lmin })
    n1 = SymNMOS("N1", ['nabs', 'B', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n2 = SymNMOS("N2", ['nabs', 'A', 'ny', 'VSS'], {'w' : wn, 'l' : lmin })
    n3 = SymNMOS("N3", ['nc', 'C', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['Y', 'ny', 'VDD', 'VDD'], {'w' : wps, 'l' : lmin })
    p1 = SymPMOS("P1", ['ny', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P2", ['ny', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p3 = SymPMOS("P3", ['Y', 'C', 'VDD', 'VDD'], {'w' : wps, 'l' : lmin })

    OAI2N1_D1.addElement([n0, n1, n2, n3, p0, p1, p2, p3])

    # Flatten the circuit
    if genFlat:
        OAI2N1_D1_flat = OAI2N1_D1.flat()
    if anonimize:
        OAI2N1_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ (Or(And(x, y), Not(z))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

