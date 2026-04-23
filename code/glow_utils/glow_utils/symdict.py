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


"""
Symdict class provides hierarchical dictionary feature.
This is useful for implementing scoped dictionary access,
when local parameter values override the global ones.
"""

class Symdict(dict):
    """
    Sub-class of Python dict class to allow hierarchical parameter evaluation.
    Dictionary keys and values are evaluated in hierarchical manner,
    where keys and values defined in localDict take precedence over upper levels.
    Example:
    topDict = { 'x':1, 'y':2}
    level1Dict = Symdict( topDict, localDict={'x':5 } )
    level1Dict['x'] evaluates to 5, since the local parameters take precedence over global ones.
    The same principle applies recursively.
    If the key in not defined in any dictionary, a KeyError exception is raised.
    """

    def __init__(self, parentDict, localDict = {}):
        """
        Init the Symdict with parentDict, which can be a dictionary or
        another instance of Symdict, and a local dictionary localDict.
        """
        self.parentDict = parentDict
        self.setLocalDict(localDict)
        
    def setLocalDict(self, localDict):
        """
        Set the provided dictionary as local dictionary.
        """
        self.clear()
        self.update(localDict)

    def getStructure(self):
        dictLen = super(type(self), self).__len__()
        res = "dict("+str(dictLen)+")"
        try:
            res += " -> " + self.parentDict.getStructure()
        except:
            if not (self.parentDict == None):
                res += " -> " + "dict("+str(len(self.parentDict))+")"    # The top level dictionary is not Symdict, but an ordinary dict
        return res    

    #---------------------------------------------------------------------------
    # Overloaded dict methods
    #---------------------------------------------------------------------------
        
    def __missing__(self, key):
        """
        The key is not present the in local dictionary, pass the request to parentDict
        to (possibly recursively) get the key value.
        """
        if self.parentDict == None:
            raise KeyError()
        else:        
            return self.parentDict[key]

    def __str__(self):
        """
        Prints dictionaries in hierarchical way.
        """
        res = super(type(self), self).__str__()     # get the string representation of local dictionary
        if not (self.parentDict == None):
            res += "\n"
            res += self.parentDict.__str__() # get the string representation of parent dictionary
        return res

    def __repr__(self):
        tmpDict = self.copy()
        return tmpDict.__repr__()

    def get(self, key, default=None):
        try:
            return self[key]
        except:
            return default

    def has_key(self, key):
        """
        Check if a flattened hierarchical dictionary has a key.
        First it checks if local dictionary has the specified key,
        and if not, traverses through other dictionaries.
        """
        #if super(type(self), self).has_key(key):
        if key in super(type(self), self).keys():
            return True     # Local dictionary has the key
        if self.parentDict == None:
            return False
        else:
            #return self.parentDict.has_key(key)
            return key in self.parentDict

    def copy(self):
        """
        Return a shallow copy of flattened dictionary
        """
        if self.parentDict == None:
            tmpDict = {}
        else:
            tmpDict = self.parentDict.copy()
        tmpDict.update(self)
        return tmpDict

    def items(self):
        """
        Returns items of flattened dictionary
        """
        tmpDict = self.copy()
        return tmpDict.items()

    def iteritems(self):
        """
        Returns iteritems of flattened dictionary
        """
        tmpDict = self.copy()
        return tmpDict.iteritems()

    def iterkeys(self):
        """
        Returns iterkeys of flattened dictionary
        """
        tmpDict = self.copy()
        return tmpDict.iterkeys()

    def itervalues(self):
        """
        Returns itervalues of flattened dictionary
        """
        tmpDict = self.copy()
        return tmpDict.itervalues()

    def __len__(self):
        """
        Returns the length of flattened dictionary
        """
        tmpDict = self.copy()
        return len(tmpDict)

    def __delitem__(self, key):
        """
        Overloaded low-level method for handling
        del SymdictInst[key]
        """
        raise RuntimeError("Deleting items is not supported in a hierarchical dictionary")

    def __contains__(self,key):
        """
        Overloaded low-level method for handling
        key in SymdictInst
        """
        return self.has_key(key)

