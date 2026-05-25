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

from glow_utils.symdevice import Symdevice
from glow_utils.symtech import SymTech
from glow_utils.symieee1164 import IEEE1164

#
# MOSFET base class
#

class SymMOSFET(Symdevice):
    # Device terminal names
    terminals = ['D', 'G', 'S', 'B']
    terminalNumbers = {name: index for index, name in enumerate(terminals)}

    ron = 1.0
    roff = 1e6
    rweak = 100.0

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

    def isWeak(self):
        if self.hasParameter('weak'):
            if self.parameters['weak'] == '0':
                # Strong MOSFET
                return False
            else:
                # Weak MOSFET
                return True
        else:
            return False

    def defaultAS(self):
        return 0.0 
    def defaultAD(self):
        return 0.0
    def defaultPS(self):
        return 0.0
    def defaultPD(self):
        return 0.0
    
    @staticmethod
    def isNumber(x):
        try:
            float(x)
            return True
        except ValueError:
            return False  

    def to_SPICE(self):
        # Return string for SPICE netlist
        res = "M" + self.getName() + " "
        res += " ".join(self.getNodes()) + " "
        res += self.getModelName() + " "
        for param in ['m', 'w', 'l', 'ad', 'as', 'pd', 'ps', 'nrd', 'nrs', 'ng']:
            if self.hasParameter(param):
                paramVal = self.evalInternalFns(self.parameters.get(param))
                if isinstance(paramVal, (int, float)) or self.isNumber(paramVal):
                    res += param + "=" + "{:.4g}".format(float(paramVal)) + " "
                else:
                    # NGSPICE expression
                    res += param + "={" + str(paramVal) + "} "
        res += "\n"
        return res

    def to_CDL(self):
        # Return string for CDL netlist
        res = "M" + self.getName() + " "
        res += " ".join(self.getNodes()) + " "
        res += self.getModelName() + " "
        for param in ['m', 'w', 'l', 'ng']:
            if self.hasParameter(param):
                paramVal = self.evalInternalFns(self.parameters.get(param))
                if isinstance(paramVal, (int, float)) or self.isNumber(paramVal):
                    res += param + "=" + "{:.4g}".format(float(paramVal)) + " "
                else:
                    res += param + "=" + str(paramVal) + " "
        res += "\n"
        return res

#
# NMOS class
#
class SymNMOS(SymMOSFET, SymTech):
    modelName = SymTech.nmosModelName
    deviceType = "nmos"
    modelPrefix = "N"
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

    def simR(self, nodeVals):
        """
        Simulate NMOS
        """
        d, g, s, b = nodeVals
        # Special case for diode connected NMOS
        nodes = self.getNodes()
        if (nodes[0] == nodes[1]):
            # Drain-gate connection
            if (s == IEEE1164.L) or (s == IEEE1164.ZERO):
                return self.ron
        elif (nodes[2] == nodes[1]):
            # Sorce-gate connection
            if (d == IEEE1164.L) or (d == IEEE1164.ZERO):
                return self.ron
        elif (g == IEEE1164.ONE) or (g == IEEE1164.H):
            # NMOS gate is high - device in ON
            if not self.isWeak():
                # Strong NMOS
                return self.ron
            else:
                return self.rweak
        return self.roff


#
# PMOS class
#
class SymPMOS(SymMOSFET, SymTech):
    modelName = SymTech.pmosModelName
    deviceType = "pmos"
    modelPrefix = "P"
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

    def simR(self, nodeVals):
        """
        Simulate PMOS
        """
        d, g, s, b = nodeVals
        # Special case for diode connected PMOS
        nodes = self.getNodes()
        if (nodes[0] == nodes[1]):
            # Drain-gate connection
            if (s == IEEE1164.H) or (s == IEEE1164.ONE):
                return self.ron
        elif (nodes[2] == nodes[1]):
            # Sorce-gate connection
            if (d == IEEE1164.H) or (d == IEEE1164.ONE):
                return self.ron
        elif (g == IEEE1164.ZERO) or (g == IEEE1164.L):
            # PMOS gate is low - device in ON
            if not self.isWeak():
                # Strong PMOS
                return self.ron
            else:
                return self.rweak
        return self.roff
