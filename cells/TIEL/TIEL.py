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
    cellInfo = { 'name' : 'TIEL',
                 'pinList' : ['Y', 'VDD', 'VSS'],
                 'description' : 'Tie low cell.'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    TIEL = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])
    lmin = SymTech.technology['Lmin']
    wn = SymTech.technology['invx1WN']
    wp = wn

    # NMOS
    n0 = SymNMOS("N0", ['Y', 'G', 'VSS', 'VSS'], {'w' : wn, 'l' : lmin })

    # PMOS
    p0 = SymPMOS("P0", ['G', 'G', 'VDD', 'VDD'], {'w' : wp, 'l' : lmin })

    TIEL.addElement([n0, p0])

    # Flatten the circuit
    if genFlat:
        TIEL_flat = TIEL.flat()
    if anonimize:
        TIEL_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ 0 ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)
