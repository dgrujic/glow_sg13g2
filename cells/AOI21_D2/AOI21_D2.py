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
from sympy.abc import x, y, z

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'AOI21_D2',
                 'pinList' : ['A', 'B', 'C', 'Y', 'VDD', 'VSS'],
                 'description' : 'AOI21 with drive strength x2'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AOI21_D2 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wns = 900e-9
    wnp = SymTech.technology['invx1WN']
    ngn = 2
    wp = 2 * wnp
    lmin = SymTech.technology['Lmin']

    # Pull-down network
    n0 = SymNMOS("N0", ['n0', 'A', 'VSS', 'VSS'], {'w' : ngn * wns, 'l' : lmin, 'ng' : ngn })
    n1 = SymNMOS("N1", ['Y', 'B', 'n0', 'VSS'], {'w' : ngn * wns, 'l' : lmin, 'ng' : ngn })
    n2 = SymNMOS("N2", ['Y', 'C', 'VSS', 'VSS'], {'w' : ngn * wnp, 'l' : lmin, 'ng' : ngn })

    # Pull-up network
    p0_0 = SymPMOS("P0_0", ['n1_0', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1_0 = SymPMOS("P1_0", ['n1_0', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2_0 = SymPMOS("P2_0", ['Y', 'C', 'n1_0', 'VDD'], {'w' : wp, 'l' : lmin })

    p0_1 = SymPMOS("P0_1", ['n1_1', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1_1 = SymPMOS("P1_1", ['n1_1', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2_1 = SymPMOS("P2_1", ['Y', 'C', 'n1_1', 'VDD'], {'w' : wp, 'l' : lmin })

    AOI21_D2.addElement([n0, n1, n2, p0_0, p0_1, p1_0, p1_1, p2_0, p2_1])

    # Flatten the circuit
    if genFlat:
        AOI21_D2_flat = AOI21_D2.flat()
    if anonimize:
        AOI21_D2_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(Or(x, And(y, z))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

