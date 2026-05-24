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
from sympy import Not
from sympy.abc import x

wn = SymTech.technology["invx1WN"]
wp = SymTech.technology["invx1WP"]
expectedFns = [Not(x)]

INV_D1 = Symsubcircuit("INV_D1", ['A', 'Y', 'VDD', 'VSS'])
inv1 = inv_par("inv1", ['A', 'Y', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp})
INV_D1.addElement(inv1)

# Flatten the circuit
INV_D1_flat = INV_D1.flat()
INV_D1_flat.anonimize()

circuit = INV_D1_flat
circuitName = circuit.getClassName()

print("#"*80)
# Simulate the circuit to check the logic function
sim = Symsim(circuit)
if sim.combCheck(expectedFns):
    print("\nCircuit function OK")
else:
    print("\nERROR : Circuit does not work as expected.")
    exit(1)
print("*"*80)
circuit.write_SPICE(circuitName)
print("*"*80)
circuit.write_CDL(circuitName)
print("#"*80)
