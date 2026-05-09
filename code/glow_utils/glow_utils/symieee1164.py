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

from enum import auto, Enum

class IEEE1164(Enum):
    # IEEE1164 types
    ONE = "1"
    ZERO = "0"
    H = "H"
    L = "L"
    WEAK = "W"
    UNDEFINED = "U"
    Z = "Z"
    X = "X"
    DONT_CARE = "-"

    @staticmethod
    def resolve(x, y):
        """
        Resolve a signal value when a net is driven by two drivers per IEEE1164
        """
        v = set([x, y])
        if ( IEEE1164.UNDEFINED in v ):
            return IEEE1164.UNDEFINED
        if ( IEEE1164.X in v ):
            return IEEE1164.X
        if ( IEEE1164.DONT_CARE in v ):
            return IEEE1164.X
        if ( IEEE1164.Z in v ):
            if ( x == IEEE1164.Z ):
                return y
            else:
                return x
        if ( IEEE1164.ZERO in v ):
            if IEEE1164.ONE in v:
                return IEEE1164.X
            else:
                return IEEE1164.ZERO
        if ( IEEE1164.ONE in v ):
            # Case (ZERO, ONE) already covered
            return IEEE1164.ONE
        if ( IEEE1164.WEAK in v ):
            return IEEE1164.WEAK
        if ( IEEE1164.L in v ):
            if IEEE1164.H in v:
                return IEEE1164.WEAK
            else:
                return IEEE1164.L
        if ( IEEE1164.H in v ):
            if IEEE1164.L in v:
                return IEEE1164.WEAK
            else:
                return IEEE1164.H

    @staticmethod
    def toStr(val):
        if isinstance(val, list) or isinstance(val, tuple):
            res = ""
            for x in val:
                res += str(x.value)
            return res
        else:
            return str(val.value)
        
    @staticmethod
    def toList(val):
        res = []
        if isinstance(val, list) or isinstance(val, tuple):
            valList = val
        else:
            valList = [val]
        for x in valList:
            if (x == IEEE1164.ONE) or (x == IEEE1164.H):
                res.append(1)
            else:
                res.append(0)
                if (x != IEEE1164.ZERO) and (x != IEEE1164.L):
                    print("WARNING : IEEE1164 value " + str(x.value) + " converted to 0.")
        return res
