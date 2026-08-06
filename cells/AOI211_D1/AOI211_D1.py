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
    cellInfo = { 'name' : 'AOI211_D1',
                 'pinList' : ['A', 'B', 'C', 'D', 'Y', 'VDD', 'VSS'],
                 'description' : 'AOI211 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AOI211_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wnp = SymTech.technology['invx1WN']
    wns = 900e-9
    wp = 2 * wnp
    lmin = SymTech.technology['Lmin']

    # Pull-down network
    n0 = SymNMOS("N0", ['Y', 'D', 'VSS', 'VSS'], {'w' : wnp, 'l' : lmin })
    n1 = SymNMOS("N1", ['Y', 'C', 'VSS', 'VSS'], {'w' : wnp, 'l' : lmin })
    n2 = SymNMOS("N2", ['n0', 'B', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })
    n3 = SymNMOS("N3", ['Y', 'A', 'n0', 'VSS'], {'w' : wns, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['n1', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1 = SymPMOS("P1", ['n1', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P2", ['n2', 'C', 'n1', 'VDD'], {'w' : wp, 'l' : lmin })
    p3 = SymPMOS("P3", ['Y', 'D', 'n2', 'VDD'], {'w' : wp, 'l' : lmin })

    AOI211_D1.addElement([n0, n1, n2, n3, p0, p1, p2, p3])

    # Flatten the circuit
    if genFlat:
        AOI211_D1_flat = AOI211_D1.flat()
    if anonimize:
        AOI211_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(Or(And(x, y), z, w)) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

