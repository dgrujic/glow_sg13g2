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
Manifest class reads the cell manifest and provides functions to access the data.
"""

import yaml12
from enum import Enum

class Manifest:
    # Valid cell types
    cellTypes = Enum('cellTypes', [('COMB', 'combinatorial'),
                                   ('DFF', 'dff'),
                                   ('DL', 'dlatch'),
                                   ('CONST', 'constant'),
                                   ('ANT', 'antenna'),
                                   ('PHY', 'physical')])

    # Valid pin types
    pinTypes = Enum('pinTypes', [('IN', 'input'),
                                 ('OUT', 'output'),
                                 ('INOUT', 'inout'),
                                 ('POWER', 'power'),
                                 ('GND', 'ground')])

    # Mandatory fields for cell group
    mandatoryFields = set(['description', 'type', 'pins', 'function', 'cells'])
    pinFields = set(['type', 'description'])

    def __init__(self, fileName, verbose=False):
        self.verbose = verbose
        try:
            self.manifest = yaml12.read_yaml(fileName)
            if self.verbose:
                print("Read in YAML file", fileName)
            if not self.check():
                raise ValueError("Malformed manifest.")
        except FileNotFoundError:
            print("ERROR: File", fileName, "not found.")
            raise FileNotFoundError()
        except ValueError as err:
            print("ERROR: Syntax error in YAML :", err)
            raise ValueError("Syntax error")

    def check(self):
        """
        Perform checks on cell manifest to ensure that it is valid.
        """
        validCellTypes = set(x.value for x in self.cellTypes)
        validPinTypes = set(x.value for x in self.pinTypes)

        for cellGroupName in self.manifest:
            # Check if cellGroup has all of mandatory fields
            cellGroup = self.manifest[cellGroupName]
            fields = set(cellGroup.keys())
            if not self.mandatoryFields.issubset(fields):
                if self.verbose:
                    print("ERROR: Cell group", cellGroupName, "does not have all mandatory fields.")
                return False
            # Check cell type
            if cellGroup['type'] not in validCellTypes:
                if self.verbose:
                    print("ERROR: Cell group", cellGroupName, "type ",cellGroup['type'], " is invalid.")
                return False
            # Check pins
            if cellGroup['pins'] is not None:
                for pinName in cellGroup['pins']:
                    pin = cellGroup['pins'][pinName]
                    if not self.pinFields.issubset(set(pin)):
                        # Pin does not have all mandatory fields
                        print("ERROR: Cell group", cellGroupName, "pin", pinName, "does not have all mandatory fields.")
                        return False
                    if pin['type'] not in validPinTypes:
                        return False
            else:
                if self.verbose:
                    print("WARNING: Cell group", cellGroupName, " has no pins.")
            # Check if there is at least one cell
            if cellGroup['cells'] is None:
                if self.verbose:
                    print("ERROR: Cell group", cellGroupName, " has no cells.")
                return False
        return True                

    def getCellGroups(self, cellType = 'all'):
        """
        Returns a subset of cell groups with specified type
        """
        if cellType == 'all':
            return self.manifest
        else:
            validCellTypes = set(x.value for x in self.cellTypes)
            if cellType not in validCellTypes:
                if self.verbose:
                    print("WARNING: Invalid cell group type given", cellType, "returning empty list.")
                    return []
            cellGroups = {}
            for cellGroupName in self.manifest:
                cellGroup = self.manifest[cellGroupName]
                if cellGroup['type'] == cellType:
                    cellGroups.update( {cellGroupName : cellGroup} )
            return cellGroups

    def getCellGroupPins(self, cellGroup):
        """
        Returns a dictionary of cell group pins
        """
        return self.manifest[cellGroup]['pins']

    def getCellGroupCells(self, cellGroup):
        """
        Returns a list of cell group cells
        """
        return self.manifest[cellGroup]['cells']

    def getCellGroupType(self, cellGroup):
        """
        Returns a type of cell group
        """
        return self.manifest[cellGroup]['type']

    def getCellGroupFnSpec(self, cellGroup):
        """
        Returns a dictionary of cell group functions
        """
        return self.manifest[cellGroup]['function']

    def getCellType(self, cellName):
        """
        Returns a type of cell named cellName or None if not found
        """
        cellGroup = self.findCellGroup(cellName)
        if cellGroup is not None:
            return self.getCellGroupType(cellGroup)
        else:
            return None

    def getCellPins(self, cellName):
        """
        Returns a list of cell pins or None if not found
        """
        cellGroup = self.findCellGroup(cellName)
        if cellGroup is not None:
            pinDict = self.getCellGroupPins(cellGroup)
            return list(pinDict.keys())
        else:
            return None

    def getCellFnSpec(self, cellName):
        """
        Returns a dictionary of cell functions
        """
        cellGroup = self.findCellGroup(cellName)
        if cellGroup is not None:
            return self.getCellGroupFnSpec(cellGroup)
        else:
            return None
        
    def findCellGroup(self, cellName):
        """
        Returns a cell group name that contains a cell named cellName or None if not found
        """
        for cellGroup in self.manifest:
            if cellName in self.manifest[cellGroup]['cells']:
                return cellGroup
        return None

    def countCellGroups(self, cellType = 'all'):
        """
        Returns the number of cell groups of specified type
        """
        cellGroups = self.getCellGroups(cellType)
        return len(list(cellGroups))
    
    def countCells(self, cellType = 'all'):
        """
        Returns the number of cells of specified type
        """
        n = 0
        cellGroups = self.getCellGroups(cellType)
        for group in cellGroups:
            n += len(cellGroups[group]['cells'])
        return n

    def isType(self, cellName, argCellType):
        """
        Returns True if a cell is of given type, False if cell exists but is not of a given type, and None if cell does not exist
        """
        cellType = self.getCellType(cellName)
        if cellType is not None:
            if argCellType.value == cellType:
                return True
            else:
                return False
        else:
            return None

    def isCombinatorial(self, cellName):
        return self.isType(cellName, self.cellTypes['COMB'])

    def isDFF(self, cellName):
        return self.isType(cellName, self.cellTypes['DFF'])

    def isDLatch(self, cellName):
        return self.isType(cellName, self.cellTypes['DL'])

    def isConstant(self, cellName):
        return self.isType(cellName, self.cellTypes['CONST'])

    def isAntenna(self, cellName):
        return self.isType(cellName, self.cellTypes['ANT'])

    def isPhysical(self, cellName):
        return self.isType(cellName, self.cellTypes['PHY'])


