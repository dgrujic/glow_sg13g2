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
from glow_utils.symmosfet import SymNMOS, SymPMOS
from sympy import And, Or, Not
from sympy.abc import x, y, z, w

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'AOI22_D1',
                 'pinList' : ['A', 'B', 'C', 'D', 'Y', 'VDD', 'VSS'],
                 'description' : 'AOI22 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AOI22_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wn = 900e-9
    wp = 2 * SymTech.technology['invx1WN']
    lmin = SymTech.technology['Lmin']

    # Pull-down network
    n0 = SymNMOS("N0", ['n0', 'D', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n1 = SymNMOS("N1", ['Y', 'C', 'n0', 'VSS'], {'w' : wn, 'l' : lmin })
    n2 = SymNMOS("N2", ['n1', 'B', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })
    n3 = SymNMOS("N3", ['Y', 'A', 'n1', 'VSS'], {'w' : wn, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['n2', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1 = SymPMOS("P1", ['n2', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P2", ['Y', 'C', 'n2', 'VDD'], {'w' : wp, 'l' : lmin })
    p3 = SymPMOS("P3", ['Y', 'D', 'n2', 'VDD'], {'w' : wp, 'l' : lmin })

    AOI22_D1.addElement([n0, n1, n2, n3, p0, p1, p2, p3])

    # Flatten the circuit
    if genFlat:
        AOI22_D1_flat = AOI22_D1.flat()
    if anonimize:
        AOI22_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(Or(And(x, y), And(z, w))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

