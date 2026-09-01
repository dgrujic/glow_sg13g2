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
    cellInfo = { 'name' : 'DFQ_D4',
                 'pinList' : ['D', 'CLK', 'Q', 'QN', 'VDD', 'VSS'],
                 'description' : 'D flip-flop with Q output with drive strength x4'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    wn = 2 * SymTech.technology["invx2WN"]
    wp = 2 * SymTech.technology["invx2WP"]
    ng = 3

    DFQ_D4 = Symsubcircuit("DFQ_D4", ['D', 'CLK', 'Q', 'QN', 'VDD', 'VSS'])
    # Clock inverters
    inv_clkn = inv_par("inv_clkn", ['CLK', 'clkn', 'VDD', 'VSS'], {'WN' : 750e-9, 'WP' : 1120e-9})
    inv_clki = inv_par("inv_clki", ['clkn', 'clki', 'VDD', 'VSS'], {'WN' : 550e-9, 'WP' : 830e-9})
    # Master latch
    invz_in = invz_par("invz_in", ['D', 'clkn', 'clki', 'dn', 'VDD', 'VSS'], {'WN' : 400e-9, 'WP' : 600e-9})
    inv_ml = inv_par("inv_ml", ['dn', 'di', 'VDD', 'VSS'], {'WN' : 650e-9, 'WP' : 980e-9})
    invz_mfb = invz_par("invz_mfb", ['di', 'clki', 'clkn', 'dn', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 230e-9, 'WEAK' : 1})
    # Slave latch
    invz_ms = invz_par("invz_ms", ['di', 'clki', 'clkn', 'qin', 'VDD', 'VSS'], {'WN' : 2000e-9, 'WP' : 3000e-9, 'NGN' : 2, 'NGP' : 2})
    inv_sl = inv_par("inv_sl", ['qin', 'qi', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 300e-9})
    invz_sfb = invz_par("invz_sfb", ['qi', 'clkn', 'clki', 'qin', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 150e-9})

    inv_Q = inv_par("inv_Q", ['qin', 'Q', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp, 'NGN' : ng, 'NGP' : ng})

    DFQ_D4.addElement([inv_clkn, inv_clki, invz_in, inv_ml, invz_mfb, invz_ms, inv_sl, invz_sfb, inv_Q])

    # Flatten the circuit
    if genFlat:
        DFQ_D4_flat = DFQ_D4.flat()
    if anonimize:
        DFQ_D4_flat.anonimize()

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
    spec = { 'D' : 'D', 'Q' : 'Q', 'CLK' : 'CLK' }
    res = sim.dffCheck(spec)

    if verbose:
        # Plot waveforms
        wave = sim.filterResults( ['D', 'CLK', 'Q'] )
        print("Simulation waveform")
        sres = sim.plotResults(wave)
        for name in sres.keys():
            print(sres[name])
    return res

