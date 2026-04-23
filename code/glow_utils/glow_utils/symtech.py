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

class SymTech:
    processName = "sg13g2"
    nmosModelName = "sg13s_lvnmos"
    pmosModelName = "sg13s_lvpmos"
    # Minumum MOSFET diffusion width, used to calculate source/drain area and periphery
    nmosDW = 310e-9
    pmosDW = 310e-9

    def nmosAS():
        return 'ipar("w")*' + str(SymTech.nmosDW)
    def nmosAD():
        return 'ipar("w")*' + str(SymTech.nmosDW) 
    def nmosPS():
        return '2*(ipar("w")+' + str(SymTech.nmosDW) + ')'
    def nmosPD():
        return '2*(ipar("w")+' + str(SymTech.nmosDW) + ')'
    
    def pmosAS():
        return 'ipar("w")*' + str(SymTech.pmosDW)
    def pmosAD():
        return 'ipar("w")*' + str(SymTech.pmosDW) 
    def pmosPS():
        return '2*(ipar("w")+' + str(SymTech.pmosDW) + ')'
    def pmosPD():
        return '2*(ipar("w")+' + str(SymTech.pmosDW) + ')'



