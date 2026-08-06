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

from pathlib import Path
import importlib
import os
import sys

from glow_parcells import *
from glow_utils.symsim import Symsim
from glow_utils.symtech import SymTech
from glow_utils.symmosfet import SymNMOS, SymPMOS
from sympy import And, Or, Not
from sympy.abc import x, y, z

def file_exists(file_name):
    if Path(file_name).is_file():
        return True
    return False

def importCell(cell_name):
    if not file_exists("../" + cell_name + "/" + cell_name + ".py"):
        print("ERROR : File", cell_name+".py", "does not exist.")
        exit(1)

    # Dynamically load the cell
    path = os.getcwd() + "/../" + cell_name
    sys.path.insert(0, path)
    cell_module = importlib.import_module(cell_name)
    cell_module.generate()

def info():
    """
    Returns a dictionary with cell information
    Key         Value
    name        Cell name
    pinList     List of cell pins
    description Cell description
    """
    cellInfo = { 'name' : 'AOI2N1_D2',
                 'pinList' : ['A', 'B', 'C', 'Y', 'VDD', 'VSS'],
                 'description' : 'AOI2N1 with drive strength x1'
    }
    return cellInfo

def generate(genFlat = True, anonimize = True):
    """
    Generate the circuit structure.
    If genFlat = True generate a flat circuit with suffix _flat
    If anonimize = True anonimize devices and nodes in the generated flat circuit
    """
    cellInfo = info()

    AOI2N1_D2 = Symsubcircuit(cellInfo['name'], cellInfo['pinList'])

    cell_name = "AOI2N1_D1"
    importCell(cell_name)
    AOI2N1_cell = Symsubcircuit.getSubckts()[cell_name]
    AOI2N1_inst1 = AOI2N1_cell('AOI2N1_inst1', cellInfo['pinList'])
    AOI2N1_inst2 = AOI2N1_cell('AOI2N1_inst2', cellInfo['pinList'])

    AOI2N1_D2.addElement([AOI2N1_inst1, AOI2N1_inst2])

    # Flatten the circuit
    if genFlat:
        AOI2N1_D2_flat = AOI2N1_D2.flat()
    if anonimize:
        AOI2N1_D2_flat.anonimize()

def check(verbose = False):
    """
    Check if the circuit works as expected
    """
    expectedFns = [ And(Or(x, y), Not(z)) ]
    cellInfo = info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    sim = Symsim(circuit, verbose = verbose)
    return sim.combCheck(expectedFns)

