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

# Parametrized inverter with tristate output subcircuit
# Terminals:
#   A       input
#   E       output enable
#   EN      output enable, inverted
#   Y       output
#   VDD     power supply
#   VSS     ground
# Parameters:
#   WN      total width of NMOS transistor channel, default 300 nm
#   WP      total width of PMOS transistor channel, default 450 nm
#   L       channel length, default 130 nm
#   NGN     number of NMOS transistor gates, default 1
#   NGP     number of PMOS transistor gates, default 1
#   WEAK    0 - normal drive, 1 - weak drive
#           Should be used where an inverter output is changed by other circuit, e.g. in a latch or a flip-flop

from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS

invz2_par = Symsubcircuit("invz2_par", ['A', 'EN', 'ENB', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1, 'WEAK' : 0})
n0 = SymNMOS("N0", ['Y', 'A', 'net0', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")', 'weak' : 'ppar("WEAK")'})
n1 = SymNMOS("N1", ['net0', 'EN', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")', 'weak' : 'ppar("WEAK")'})
p0 = SymPMOS("P0", ['Y', 'A', 'net1', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")', 'weak' : 'ppar("WEAK")'})
p1 = SymPMOS("P1", ['net1', 'ENB', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")', 'weak' : 'ppar("WEAK")'})
invz2_par.addElement([n0, n1, p0, p1])
