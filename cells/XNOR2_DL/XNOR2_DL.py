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
from sympy import Xor, Not
from sympy.abc import x, y

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'XNOR2_DL',
                 'pinList' : ['A', 'B', 'Y', 'VDD', 'VSS'],
                 'description' : 'XNOR2 with weak drive strength'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    XNOR2_DL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    lmin = SymTech.technology['Lmin']
    wn = 300e-9
    wp = 400e-9

    wnmin = 200e-9
    wpmin = 300e-9

    # NMOS
    n0 = SymNMOS("N0", ['BN', 'AN', 'Y', 'VSS'], {'w' : wnmin, 'l' : lmin })
    n1 = SymNMOS("N1", ['BI', 'A', 'Y', 'VSS'], {'w' : wnmin, 'l' : lmin })

    # PMOS
    p0 = SymPMOS("P0", ['BN', 'A', 'Y', 'VDD'], {'w' : wpmin, 'l' : lmin })
    p1 = SymPMOS("P1", ['BI', 'AN', 'Y', 'VDD'], {'w' : wpmin, 'l' : lmin })

    inv_inst1 = inv_par('inv_inst', ['BN', 'BI', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
    inv_inst2 = inv_par('inv_inst', ['B', 'BN', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
    inv_inst3 = inv_par('inv_inst', ['A', 'AN', 'VDD', 'VSS'], {'WN' : wnmin, 'WP' : wpmin})
    XNOR2_DL.addElement([inv_inst1, inv_inst2, inv_inst3, n0, n1, p0, p1])

    # Flatten the circuit
    if genFlat:
        XNOR2_DL_flat = XNOR2_DL.flat()
    if anonimize:
        XNOR2_DL_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(Xor(x, y)) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)
