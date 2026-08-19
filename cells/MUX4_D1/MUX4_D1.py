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
from sympy import symbols
from sympy.abc import x, y, z, w

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'MUX4_D1',
                 'pinList' : ['I0', 'I1', 'I2', 'I3', 'S0', 'S1', 'Y', 'VDD', 'VSS'],
                 'description' : 'MUX4 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    MUX4_D1 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    inv_ctrl0_wn = 500e-9
    inv_ctrl0_wp = 3 * inv_ctrl0_wn / 2
    inv_ctrl1_wn = 300e-9
    inv_ctrl1_wp = 3 * inv_ctrl1_wn / 2
    inv_wn = SymTech.technology['invx1WN']
    inv_wp = SymTech.technology['invx1WP']

    inv_inst_S0 = inv_par('inv_inst_S0', ['S0', 'S0B', 'VDD', 'VSS'], {'WN' : inv_ctrl0_wn, 'WP' : inv_ctrl0_wp})
    inv_inst_S1 = inv_par('inv_inst_S1', ['S1', 'S1B', 'VDD', 'VSS'], {'WN' : inv_ctrl1_wn, 'WP' : inv_ctrl1_wp})
    inv_inst_Y = inv_par('inv_inst_y', ['NY', 'Y', 'VDD', 'VSS'], {'WN' : inv_wn, 'WP' : inv_wp})

    mux_wn = SymTech.technology['mux3x1WN']
    mux_wp = 3 * mux_wn / 2
    tg_wn = SymTech.technology['mux3x1WN']
    tg_wp = 3 * SymTech.technology['mux3x1WN'] / 2
    invz_inst_I0 = invz_par('invz_inst_I0', ['I0', 'S0B', 'S0', 'int0NY', 'VDD', 'VSS'], {'WN' : mux_wn, 'WP' : mux_wp})
    invz_inst_I1 = invz_par('invz_inst_I1', ['I1', 'S0', 'S0B', 'int0NY', 'VDD', 'VSS'], {'WN' : mux_wn, 'WP' : mux_wp})
    invz_inst_I2 = invz_par('invz_inst_I2', ['I2', 'S0B', 'S0', 'int1NY', 'VDD', 'VSS'], {'WN' : mux_wn, 'WP' : mux_wp})
    invz_inst_I3 = invz_par('invz_inst_I3', ['I3', 'S0', 'S0B', 'int1NY', 'VDD', 'VSS'], {'WN' : mux_wn, 'WP' : mux_wp})

    tgate_inst1 = tgate_par('tgate_inst1', ['int0NY', 'NY', 'S1B', 'S1', 'VDD', 'VSS'], {'WN' : tg_wn, 'WP' : tg_wp})
    tgate_inst2 = tgate_par('tgate_inst2', ['int1NY', 'NY', 'S1', 'S1B', 'VDD', 'VSS'], {'WN' : tg_wn, 'WP' : tg_wp})

    MUX4_D1.addElement([inv_inst_S0, inv_inst_S1, inv_inst_Y])
    MUX4_D1.addElement([invz_inst_I0, invz_inst_I1, invz_inst_I2, invz_inst_I3])
    MUX4_D1.addElement([tgate_inst1, tgate_inst2])

    # Flatten the circuit
    if genFlat:
        MUX4_D1_flat = MUX4_D1.flat()
    if anonimize:
        MUX4_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    s0, s1 = symbols('s0 s1')
    expectedFns = [ Or(And(x, And(Not(s0), Not(s1))), And(y, And(s0, Not(s1))), And(z, And(Not(s0), s1)), And(w, And(s0, s1))) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

