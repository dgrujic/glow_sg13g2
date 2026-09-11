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

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'DFEQ_D2',
                 'pinList' : ['D', 'E', 'CLK', 'Q', 'VDD', 'VSS'],
                 'description' : 'D flip-flop with enable and Q output with drive strength x2'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):

    cellInfo = info()

    wnx1 = SymTech.technology["invx1WN"]
    wpx1 = SymTech.technology["invx1WP"]

    wn = SymTech.technology["invx2WN"]
    wp = SymTech.technology["invx2WP"]
    lmin = SymTech.technology['Lmin']

    wpdn = 250e-9
    wpun = 400e-9

    DFEQ_D2 = Symsubcircuit(cellInfo['name'], ['D', 'E', 'CLK', 'Q', 'VDD', 'VSS'])
    # Clock inverters
    inv_clkn = inv_par("inv_clkn", ['CLK', 'clkn', 'VDD', 'VSS'], {'WN' : wnx1, 'WP' : wpx1})
    inv_clki = inv_par("inv_clki", ['clkn', 'clki', 'VDD', 'VSS'], {'WN' : wnx1 / 2, 'WP' : wpx1 / 2})
    # Enable inverter
    inv_enb = inv_par("inv_enb", ['E', 'enb', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 250e-9})
    # Input enable network
    # Pull-down network
    n0 = SymNMOS("N0", ['nde', 'E', 'VSS', 'VSS'], {'w' : wpdn, 'l' : lmin })
    n1 = SymNMOS("N1", ['net_pdn', 'D', 'nde', 'VSS'], {'w' : wpdn, 'l' : lmin })
    n2 = SymNMOS("N2", ['nenbqi', 'enb', 'VSS', 'VSS'], {'w' : wpdn, 'l' : lmin })
    n3 = SymNMOS("N3", ['net_pdn', 'qi', 'nenbqi', 'VSS'], {'w' : wpdn, 'l' : lmin })
    n4 = SymNMOS("N4", ['dn', 'clkn', 'net_pdn', 'VSS'], {'w' : wpdn, 'l' : lmin })
    # Pull-up network
    p0 = SymPMOS("P0", ['neqi', 'E', 'VDD', 'VDD'], {'w' : wpun, 'l' : lmin })
    p1 = SymPMOS("P1", ['net_pun', 'qi', 'neqi', 'VDD'], {'w' : wpun, 'l' : lmin })
    p2 = SymPMOS("P2", ['nenbd', 'enb', 'VDD', 'VDD'], {'w' : wpun, 'l' : lmin })
    p3 = SymPMOS("P3", ['net_pun', 'D', 'nenbd', 'VDD'], {'w' : wpun, 'l' : lmin })
    p4 = SymPMOS("P4", ['dn', 'clki', 'net_pun', 'VDD'], {'w' : wpun, 'l' : lmin })
    # Master latch
    inv_ml = inv_par("inv_ml", ['dn', 'di', 'VDD', 'VSS'], {'WN' : 450e-9, 'WP' : 700e-9})
    invz_mfb = invz_par("invz_mfb", ['di', 'clki', 'clkn', 'dn', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 250e-9, 'WEAK' : 1})
    # Slave latch
    invz_ms1 = invz_par("invz_ms1", ['di', 'clki', 'clkn', 'qin', 'VDD', 'VSS'], {'WN' : 600e-9, 'WP' : 900e-9})
    invz_ms2 = invz_par("invz_ms2", ['di', 'clki', 'clkn', 'qin', 'VDD', 'VSS'], {'WN' : 600e-9, 'WP' : 900e-9})
    inv_sl = inv_par("inv_sl", ['qin', 'qi', 'VDD', 'VSS'], {'WN' : 650e-9, 'WP' : 900e-9})
    invz_sfb = invz_par("invz_sfb", ['qi', 'clkn', 'clki', 'qin', 'VDD', 'VSS'], {'WN' : 150e-9, 'WP' : 150e-9})
    # Output inverters
    inv_Q = inv_par("inv_Q", ['qin', 'Q', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})

    DFEQ_D2.addElement([inv_clkn, inv_clki, inv_enb,
                          n0, n1, n2, n3, n4,
                          p0, p1, p2, p3, p4,
                          inv_ml, invz_mfb, 
                          invz_ms1, invz_ms2, 
                          inv_sl, invz_sfb, inv_Q])

    # Flatten the circuit
    if genFlat:
        DFEQ_D2_flat = DFEQ_D2.flat()
    if anonimize:
        DFEQ_D2_flat.anonimize()

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
    spec = { 'D' : 'D', 'EN' : 'E', 'Q' : 'Q', 'CLK' : 'CLK' }
    res = sim.dffCheck(spec)

    if verbose:
        # Plot waveforms
        wave = sim.filterResults( ['D', 'E', 'CLK', 'Q'] )
        print("Simulation waveform")
        sres = sim.plotResults(wave)
        for name in sres.keys():
            print(sres[name])
    return res

