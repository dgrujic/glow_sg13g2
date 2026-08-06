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
from sympy.abc import x, y, z, w, v, u

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'AOI222_D1',
                 'pinList' : ['A', 'B', 'C', 'D', 'E', 'F', 'Y', 'VDD', 'VSS'],
                 'description' : 'AOI222 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AOI222_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    wns = 900e-9
    wp = SymTech.technology['invx2WP']
    lmin = SymTech.technology['Lmin']

    # Pull-down network
    n0 = SymNMOS("N0", ['nc', 'D', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })
    n1 = SymNMOS("N1", ['Y', 'C', 'nc', 'VSS'], {'w' : wns, 'l' : lmin })
    n2 = SymNMOS("N2", ['na', 'B', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })
    n3 = SymNMOS("N3", ['Y', 'A', 'na', 'VSS'], {'w' : wns, 'l' : lmin })
    n4 = SymNMOS("N4", ['Y', 'E', 'ne', 'VSS'], {'w' : wns, 'l' : lmin })
    n5 = SymNMOS("N5", ['ne', 'F', 'VSS', 'VSS'], {'w' : wns, 'l' : lmin })

    # Pull-up network
    p0 = SymPMOS("P0", ['nab', 'A', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p1 = SymPMOS("P1", ['nab', 'B', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })
    p2 = SymPMOS("P2", ['ncd', 'C', 'nab', 'VDD'], {'w' : wp, 'l' : lmin })
    p3 = SymPMOS("P3", ['ncd', 'D', 'nab', 'VDD'], {'w' : wp, 'l' : lmin })
    p4 = SymPMOS("P4", ['Y', 'E', 'ncd', 'VDD'], {'w' : wp, 'l' : lmin })
    p5 = SymPMOS("P5", ['Y', 'F', 'ncd', 'VDD'], {'w' : wp, 'l' : lmin })

    AOI222_D1.addElement([n0, n1, n2, n3, n4, n5, p0, p1, p2, p3, p4, p5])

    # Flatten the circuit
    if genFlat:
        AOI222_D1_flat = AOI222_D1.flat()
    if anonimize:
        AOI222_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(Or(And(x, y), And(z, w), And(v, u))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

