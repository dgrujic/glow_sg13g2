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
from sympy import Or, And, Not
from sympy.abc import x, y, s

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'MUX2N_DL',
                 'pinList' : ['I0', 'I1', 'S0', 'YN', 'VDD', 'VSS'],
                 'description' : 'MUX2 with inverted output and weak drive strength'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    MUX2N_DL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    inv_min_wn = SymTech.technology['invmWN']
    inv_min_wp = SymTech.technology['invmWP']
    inv_inst_S0 = inv_par('inv_inst_S0', ['S0', 'S0B', 'VDD', 'VSS'], {'WN' : inv_min_wn, 'WP' : inv_min_wp})

    mux_wn = SymTech.technology['invx1WN'] / 2
    mux_wp = 3 * mux_wn / 2
    invz_inst_I0 = invz_par('invz_inst_I0', ['I0', 'S0B', 'S0', 'YN', 'VDD', 'VSS'], {'WN' : mux_wn, 'WP' : mux_wp})
    invz_inst_I1 = invz_par('invz_inst_I1', ['I1', 'S0', 'S0B', 'YN', 'VDD', 'VSS'], {'WN' : mux_wn, 'WP' : mux_wp})

    MUX2N_DL.addElement([inv_inst_S0, invz_inst_I0, invz_inst_I1])

    # Flatten the circuit
    if genFlat:
        MUX2N_DL_flat = MUX2N_DL.flat()
    if anonimize:
        MUX2N_DL_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ Not(Or(And(x, Not(s)), And(y, s))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

