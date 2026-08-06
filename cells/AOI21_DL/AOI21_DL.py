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
    cellInfo = { 'name' : 'AOI21_DL',
                 'pinList' : ['A', 'B', 'C', 'Y', 'VDD', 'VSS'],
                 'description' : 'AOI21 with weak drive strength'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AOI21_DL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wns = 600e-9
    wnp = wns / 2
    wp = 3 * wnp
    lmin = SymTech.technology['Lmin']

    # Pull-down network
    n0 = SymNMOS("N0", ['n0', 'A', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })
    n1 = SymNMOS("N1", ['Y', 'B', 'n0', 'VSS'], {'w' : wns, 'l' : lmin })
    n2 = SymNMOS("N2", ['Y', 'C', 'VSS', 'VSS'], {'w' : wnp, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['n1', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1 = SymPMOS("P1", ['n1', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P2", ['Y', 'C', 'n1', 'VDD'], {'w' : wp, 'l' : lmin })

    AOI21_DL.addElement([n0, n1, n2, p0, p1, p2])

    # Flatten the circuit
    if genFlat:
        AOI21_DL_flat = AOI21_DL.flat()
    if anonimize:
        AOI21_DL_flat.anonimize()

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

