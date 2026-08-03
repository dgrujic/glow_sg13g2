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

# Parametrized NOR2 subcircuit
# Terminals:
#   A       input
#   B       input
#   Y       output
#   VDD     power supply
#   VSS     ground
# Parameters:
#   WN      total width of NMOS transistor channel, default 640nm
#   WP      total width of PMOS transistor channel, default 980 nm
#   L       channel length, default 130 nm
#   NGN     number of NMOS transistor gates, default 1
#   NGP     number of PMOS transistor gates, default 1

from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS
from glow_utils.symtech import SymTech

wn = SymTech.technology['invx1WN']
wp = SymTech.technology['invx1WP']
nor2_par = Symsubcircuit("nor2_par", ['A', 'B', 'Y', 'VDD', 'VSS'], {'WN' : wn, 'WP' : wp, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})
n0 = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
n1 = SymNMOS("N1", ['Y', 'B', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
p0 = SymPMOS("P0", ['n0', 'A', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})
p1 = SymPMOS("P1", ['Y', 'B', 'n0', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})
nor2_par.addElement([n0, n1, p0, p1])
