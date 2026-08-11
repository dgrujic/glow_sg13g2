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
from sympy.abc import x

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'CLKBUF_D16',
                 'pinList' : ['A', 'Y', 'VDD', 'VSS'],
                 'description' : 'Clock buffer with drive strength x16'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    wnin = 1400e-9
    ngnin = 2
    wpin = 3 * wnin
    ngpin = 2

    wnout = 4000e-9
    ngn = 8
    wpout = 3 * wnout
    ngp = 8

    CLKBUF_D16 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    inv1 = inv_par('inv1', ['A', 'AN', 'VDD', 'VSS'], {'WN' : wnin, 'WP' : wpin})
    inv2 = inv_par('inv2', ['AN', 'Y', 'VDD', 'VSS'], {'WN' : wnout, 'WP' : wpout, 'NGN' : ngn, 'NGP' : ngp})
    CLKBUF_D16.addElement([inv1, inv2])

    # Flatten the circuit
    if genFlat:
        CLKBUF_D16_flat = CLKBUF_D16.flat()
    if anonimize:
        CLKBUF_D16_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ x ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

