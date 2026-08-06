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
    cellInfo = { 'name' : 'AOI211_D2',
                 'pinList' : ['A', 'B', 'C', 'D', 'Y', 'VDD', 'VSS'],
                 'description' : 'AOI211 with drive strength x2'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AOI211_D2 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wnp = SymTech.technology['invx1WN']
    wns = 900e-9
    wp = 2 * wnp
    lmin = SymTech.technology['Lmin']

    # Pull-down network
    n0_0 = SymNMOS("N0_0", ['Y', 'D', 'VSS', 'VSS'], {'w' : wnp, 'l' : lmin })
    n1_0 = SymNMOS("N1_0", ['Y', 'C', 'VSS', 'VSS'], {'w' : wnp, 'l' : lmin })
    n2_0 = SymNMOS("N2_0", ['n0_0', 'B', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })
    n3_0 = SymNMOS("N3_0", ['Y', 'A', 'n0_0', 'VSS'], {'w' : wns, 'l' : lmin })

    n0_1 = SymNMOS("N0_1", ['Y', 'D', 'VSS', 'VSS'], {'w' : wnp, 'l' : lmin })
    n1_1 = SymNMOS("N1_1", ['Y', 'C', 'VSS', 'VSS'], {'w' : wnp, 'l' : lmin })
    n2_1 = SymNMOS("N2_1", ['n0_1', 'B', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })
    n3_1 = SymNMOS("N3_1", ['Y', 'A', 'n0_1', 'VSS'], {'w' : wns, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['n1', 'A', 'VDD', 'VDD'], {'w' : 2 * wp, 'l' : lmin, 'ng' : 2 })
    p1 = SymPMOS("P1", ['n1', 'B', 'VDD', 'VDD'], {'w' : 2 * wp, 'l' : lmin, 'ng' : 2 })

    p2_0 = SymPMOS("P2", ['n2_0', 'C', 'n1', 'VDD'], {'w' : wp, 'l' : lmin })
    p3_0 = SymPMOS("P3", ['Y', 'D', 'n2_0', 'VDD'], {'w' : wp, 'l' : lmin })

    p2_1 = SymPMOS("P2", ['n2_1', 'C', 'n1', 'VDD'], {'w' : wp, 'l' : lmin })
    p3_1 = SymPMOS("P3", ['Y', 'D', 'n2_1', 'VDD'], {'w' : wp, 'l' : lmin })


    AOI211_D2.addElement([n0_0, n0_1, n1_0, n1_1, n2_0, n2_1, n3_0, n3_1, p0, p1, p2_0, p2_1, p3_0, p3_1])

    # Flatten the circuit
    if genFlat:
        AOI211_D2_flat = AOI211_D2.flat()
    if anonimize:
        AOI211_D2_flat.anonimize()

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

