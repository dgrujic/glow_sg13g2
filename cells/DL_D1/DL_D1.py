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

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'DL_D1',
                 'pinList' : ['D', 'G', 'Q', 'QN', 'VDD', 'VSS'],
                 'description' : 'Latch with Q and QN outputs and drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    wn = SymTech.technology["invx1WN"]
    wp = SymTech.technology["invx1WP"]

    DL_D1 = Symsubcircuit("DL_D1", ['D', 'G', 'Q', 'QN', 'VDD', 'VSS'])
    inv_g = inv_par("inv_g", ['G', 'gn', 'VDD', 'VSS'], {'WN' : 250e-9, 'WP' : 400e-9})
    inv_gn = inv_par("inv_gn", ['gn', 'g', 'VDD', 'VSS'], {'WN' : 160e-9, 'WP' : 230e-9})

    invz1 = invz_par("invz1", ['qi', 'gn', 'g', 'qin', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 230e-9, 'WEAK' : 1})
    invz2 = invz_par("invz2", ['D', 'g', 'gn', 'qin', 'VDD', 'VSS'], {'WN' : 440e-9, 'WP' : 750e-9})

    inv_Q = inv_par("inv_Q", ['qin', 'Q', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
    inv_qi = inv_par("inv_qi", ['qin', 'qi', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 230e-9})
    inv_QN = inv_par("inv_QN", ['qi', 'QN', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})

    DL_D1.addElement([inv_g, inv_gn, invz1, invz2, inv_Q, inv_qi, inv_QN])

    # Flatten the circuit
    if genFlat:
        DL_D1_flat = DL_D1.flat()
    if anonimize:
        DL_D1_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]

    # Simulate the circuit to check the logic function
    sim = Symsim(circuit, verbose=verbose)
    spec = { 'D' : 'D', 'Q' : 'Q', 'QN' : 'QN', 'G' : 'G' }
    res = sim.latchCheck(spec)

    if verbose:
        # Plot waveforms
        wave = sim.filterResults( ['D', 'G', 'Q', 'QN'] )
        print("Simulation waveform")
        sres = sim.plotResults(wave)
        for name in sres.keys():
            print(sres[name])
    return res


