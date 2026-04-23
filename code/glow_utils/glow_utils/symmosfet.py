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

from symdevice import Symdevice
from symtech import SymTech

#
# MOSFET base class
#

class SymMOSFET(Symdevice):
    def initInstance(self):
        # Custom device initialization code
        # Check if w and l are given
        if not self.hasParameter('w'):
            raise ValueError("Device channel width not given.")
        if not self.hasParameter('l'):
            raise ValueError("Device channel length not given.")
        # If source/drain area/periphery are not given, assign default values
        # default* functions are defined in concrete MOSFET model
        if not self.hasParameter('as'):
            self.parameters.update({'as' : self.defaultAS() })
        if not self.hasParameter('ad'):
            self.parameters.update({'ad' : self.defaultAD() })
        if not self.hasParameter('ps'):
            self.parameters.update({'ps' : self.defaultPS() })
        if not self.hasParameter('pd'):
            self.parameters.update({'pd' : self.defaultPD() })

    def defaultAS(self):
        return 0.0 
    def defaultAD(self):
        return 0.0
    def defaultPS(self):
        return 0.0
    def defaultPD(self):
        return 0.0
    def to_SPICE(self):
        # Return string for SPICE netlist
        res = "M" + self.getName() + " "
        res += " ".join(self.getNodes()) + " "
        res += self.getModelName() + " "

        for param in ['m', 'w', 'l', 'ad', 'as', 'pd', 'ps', 'nrd', 'nrs']:
            if self.hasParameter(param):
                res += param + "=" + str(self.parameters.get(param)) + " "
        res += "\n"
        return res

#
# NMOS class
#
class SymNMOS(SymMOSFET, SymTech):
    modelName = SymTech.nmosModelName
    deviceType = "nmos"
    def initInstance(self):
        # Call base class init
        super().initInstance()
    def defaultAS(self):
        return SymTech.nmosAS()
    def defaultAD(self):
        return SymTech.nmosAD()
    def defaultPS(self):
        return SymTech.nmosPS()
    def defaultPD(self):
        return SymTech.nmosPD()
    def info(self):
        return "NMOS with 4 terminals"
    
#
# PMOS class
#
class SymPMOS(SymMOSFET, SymTech):
    modelName = SymTech.pmosModelName
    deviceType = "pmos"
    def initInstance(self):
        # Call base class init
        super().initInstance()
    def defaultAS(self):
        return SymTech.pmosAS()
    def defaultAD(self):
        return SymTech.pmosAD()
    def defaultPS(self):
        return SymTech.pmosPS()
    def defaultPD(self):
        return SymTech.pmosPD()
    def info(self):
        return "PMOS with 4 terminals"