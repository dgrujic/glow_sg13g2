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

# Parametrized NAND2 pull-down network subcircuit
# Terminals:
#   A       input
#   B       input
#   Y       output
#   VSS     ground
# Parameters:
#   WN      total width of NMOS transistor channel, default 300 nm
#   L       channel length, default 130 nm
#   NGN     number of NMOS transistor gates, default 1

from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS

nand2_pdn_par = Symsubcircuit("nand2_pdn_par", ['A', 'B', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'L' : 130e-9, 'NGN' : 1})
n0 = SymNMOS("N0", ['n0', 'B', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
n1 = SymNMOS("N1", ['Y', 'A', 'n0', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
nand2_pdn_par.addElement([n0, n1])

