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

import json

class SymTech:
    technology = {
        "processName" : "sg13g2",
        "nmosModelName" : "sg13_lv_nmos",
        "pmosModelName" : "sg13_lv_pmos",
        "nmosAS" : "ipar('w')*310e-9",
        "nmosAD" : "ipar('w')*310e-9",
        "nmosPS" : "2*(ipar('w')+310e-9)",
        "nmosPD" : "2*(ipar('w')+310e-9)",
        "pmosAS" : "ipar('w')*310e-9",
        "pmosAD" : "ipar('w')*310e-9",
        "pmosPS" : "2*(ipar('w')+310e-9)",
        "pmosPD" : "2*(ipar('w')+310e-9)",
        # Cell sizing
        "invx1WN": 640e-9,
        "invx1WP": 980e-9
    }
    processName = technology["processName"]
    nmosModelName = technology["nmosModelName"]
    pmosModelName = technology["pmosModelName"]

    def nmosAS():
        return SymTech.technology["nmosAS"]
    def nmosAD():
        return SymTech.technology["nmosAD"]
    def nmosPS():
        return SymTech.technology["nmosPS"]
    def nmosPD():
        return SymTech.technology["nmosPD"]
    
    def pmosAS():
        return SymTech.technology["pmosAS"]
    def pmosAD():
        return SymTech.technology["pmosAD"]
    def pmosPS():
        return SymTech.technology["pmosPS"]
    def pmosPD():
        return SymTech.technology["pmosPD"]
    
    @classmethod
    def loadTech(cls, fileName):
        # Load technology information from JSON file
        with open(fileName, 'r') as file:
            cls.technology = json.load(file)


