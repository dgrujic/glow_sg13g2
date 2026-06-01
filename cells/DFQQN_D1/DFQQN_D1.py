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
    cellInfo = { 'name' : 'DFQQN_D1',
                 'pinList' : ['D', 'CLK', 'Q', 'QN', 'VDD', 'VSS'],
                 'description' : 'D flip-flop with Q and QN outputs with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    wn = SymTech.technology["invx1WN"]
    wp = SymTech.technology["invx1WP"]

    DFQQN_D1 = Symsubcircuit("DFQQN_D1", ['D', 'CLK', 'Q', 'QN', 'VDD', 'VSS'])
    # Clock inverters
    inv_clkn = inv_par("inv_clkn", ['CLK', 'clkn', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9})
    inv_clki = inv_par("inv_clki", ['clkn', 'clki', 'VDD', 'VSS'], {'WN' : 200e-9, 'WP' : 300e-9})
    # Master latch
    invz_in = invz2_par("invz_in", ['D', 'clkn', 'clki', 'dn', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 230e-9})
    inv_ml = inv_par("inv_ml", ['dn', 'di', 'VDD', 'VSS'], {'WN' : 200e-9, 'WP' : 300e-9})
    invz_mfb = invz_par("invz_mfb", ['di', 'clki', 'clkn', 'dn', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 230e-9, 'WEAK' : 1})
    # Slave latch
    invz_ms = invz_par("invz_ms", ['di', 'clki', 'clkn', 'qin', 'VDD', 'VSS'], {'WN' : 500e-9, 'WP' : 750e-9})
    inv_sl = inv_par("inv_sl", ['qin', 'qi', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9})
    invz_sfb = invz_par("invz_sfb", ['qi', 'clkn', 'clki', 'qin', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 150e-9})

    inv_Q = inv_par("inv_Q", ['qin', 'Q', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
    inv_QN = inv_par("inv_QN", ['qi', 'QN', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})

    DFQQN_D1.addElement([inv_clkn, inv_clki, invz_in, inv_ml, invz_mfb, invz_ms, inv_sl, invz_sfb, inv_Q, inv_QN])

    # Flatten the circuit
    if genFlat:
        DFQQN_D1_flat = DFQQN_D1.flat()
    if anonimize:
        DFQQN_D1_flat.anonimize()

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
    spec = { 'D' : 'D', 'Q' : 'Q', 'QN' : 'QN', 'CLK' : 'CLK' }
    res = sim.dffCheck(spec)

    if verbose:
        # Plot waveforms
        wave = sim.filterResults( ['D', 'CLK', 'Q', 'QN'] )
        print("Simulation waveform")
        sres = sim.plotResults(wave)
        for name in sres.keys():
            print(sres[name])
    return res

