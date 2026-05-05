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
Symsubcircuit metaclass implements subcircuit functionality.
It can generate subcircuit classes with given names and nodes,
to which device instances can be added.
Generated classes can be instantiated hiearchicaly to build complex circuits.
"""

from copy import deepcopy
from copy import copy
import textwrap
from glow_utils.symdict import Symdict
from glow_utils.symparam import Symparam
from glow_utils.symdevice import Symdevice

class Symsubcircuit(object):
    """
    Symsubcircuit metaclass
    
    Symsubcircuit is a metaclass used for creating subcircuit classes.
    The main idea is to create a new class for each subcircuit.

    For example, an inverter subcircuit class named 'inv_par' with terminals 
    'A', 'Y', 'VDD' and 'VSS' and default parameter values WN = 200e-9, WP = 400e-9 and L = 130e-9
    can be created as:
    
    inv_par_cls = subcircuit( 'inv_par', ('A', 'Y', 'VDD', 'VSS'), {'WN':200e-9, 'WP':400e-9, 'L':130e-9} )
    
    The created subcircuit class, stored in inv_par_cls, can be populated with circuit elements or other subcircuits.

    Continuing the inverter example, transistors can be added to subcircuit as:
    n0 = SymNMOS('N0', ['Y', 'A', 'VSS', 'VSS'], {'w':'WN'}, {'l':'L'})
    p0 = SymNMOS('P0', ['Y', 'A', 'VDD', 'VDD'], {'w':'WP'}, {'l':'L'})
    inv_par_cls.addElement( [n0, p0] )
    
    addElement is a classmethod, so the elements are stored as class variables.
    This way, the subcircuit elements are shared amongst all instances of the
    same subcircuit. At this point the created subcircuit class has no instances.
    In order to use the subcircuit, it needs to be instantiated:
    
    inv_par_inst = inv_par_cls('instanceName', ('in', 'out', 'VDD', 'VSS'), {'WN':300e-9, 'WP':600e-9})
    
    By creating a subcircuit instance, it is given a name, connected to given nodes and
    optionally default parameters are overridden.
    The subcircuit instance can then be added to a other subcircuit to form a hierarchy:
    
    subckt_cls.addElement( inv_par_inst )
 
    Function ipar can be used to fetch the value of instance parameter, 
    and ipar('parameter_name') evaluates to the value of instance parameter 'parameter_name'.
    For example, NMOS instance with parameters
    {'w': 'WN', 'l': 'L', 
     'as': "ipar('w')*310e-9", 'ad': "ipar('w')*310e-9", 
     'ps': "2*(ipar('w')+310e-9)", 'pd': "2*(ipar('w')+310e-9)"}
    uses ipar function in expressions for as, ad, ps and pd.
    In this example, ipar('w') evaluates to the value of instance parameter 'w', so ipar('w') = 'WN'.
    Symbolic value 'WN' can further be evaluated to other expressions or a number, depending on the
    upper level subcircuit parameters.

    Function ppar can be used to fetch the value of instance parrent, which is usually a subcircuit.
    For example, a CMOS inverter

    inv_par = Symsubcircuit("inv_par", ['A', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})
    n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
    p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})
    inv_par.addElement([n, p])

    uses ppar to evaluate the value of 'WN', 'L' and 'NGN' for a given subcircuit instance.
    Continuing the example with two instances of inv_par that have different values of parameters:
    inv1 = inv_par("inv1", ['A', 'net1', 'VDD', 'VSS'], {'WN' : '1e-6', 'WP' : '2e-6', 'NGN' : 2, 'NGP' : 2, 'L' : 130e-9})
    inv2 = inv_par("inv2", ['net1', 'Y', 'VDD', 'VSS'], {'WN' : '1.5e-6', 'WP' : '3e-6', 'NGN' : 4, 'NGP' : 4, 'L' : 130e-9})
    we have that ppar evaluates to different values in different instances:
    inv1:  ppar("WN") = 1e-6
    inv2:  ppar("WN") = 2e-6
    Use of ppar enables creation of parametrized hierarchical circuits.

    """

    #
    # Class variables
    #
    subCkts = {}                    # Dictionary of all created subcircuit classes
    subCktClassName = None          # Subcircuit class name
    subCktTerminals = None          # List of subcircuit terminals
    subCktDefaultParameters = None  # Dictionary of default parameter values
    subCktDefaultFunctions = None   # Dictionary of default functions
    subCktElements = None           # List of subcircuit elements

    #************************
    # New class creation
    #************************    
    def __new__(cls, subCktClassName, subCktTerminals, subCktDefaultParameters={}, subCktDefaultFunctions={}, globalScope=False ):
        """
        This method creates a new subcircuit class.
        subCktClassName is a new subcircuit class name,
        subCktTerminals is a list of new subcircuit terminals and
        subCktDefaultParameters is a dictionary of default parameter values.
        subCktDefaultFunctions is a dictionary of default parameter values.        
        Each subcircuit class will be given its own class variables.
        """
        # Dictionary of new subcircuit class functions and variables
        newDict = { # Overload __new__ method so that newly created class doesn't create classes, but instances
                    '__new__' : cls.__new_instance__,   
                    # Give each subcircuit class a set of its own class variables
                    'subCktClassName' : subCktClassName,
                    'subCktTerminals' : subCktTerminals,
                    'subCktDefaultParameters' : Symdict({}, subCktDefaultParameters),
                    'subCktDefaultFunctions' : Symdict({}, subCktDefaultFunctions),
                    'subCktElements' : [],
                    'subCktElementNames' : set()
                   }

        newClass = type(subCktClassName, (Symsubcircuit,), newDict) # Return the newly created class
        if globalScope:
            globals()[subCktClassName]=newClass # Add class to global symbols
        # Add newly created subcircuit class to dictionary of available subcircuits
        cls.subCkts.update({subCktClassName : newClass})
        return newClass

    #************************
    # Class methods, common to all instances of the same subcircuit class
    #************************

    @classmethod
    def getSubckts(cls):
        return cls.subCkts

    @classmethod
    def getClassName(cls):
        return cls.subCktClassName

    @classmethod
    def getTerminals(cls):
        return cls.subCktTerminals
        
    @classmethod
    def getDefaultParameters(cls):
        return cls.subCktDefaultParameters

    @classmethod
    def getDefaultFunctions(cls):
        return cls.subCktDefaultFunctions
        
    @classmethod
    def getElements(cls):
        return cls.subCktElements

    @classmethod
    def isElementNameUnique(cls, name):
        if name in cls.subCktElementNames:
            return False
        else:
            cls.subCktElementNames.update(name)
            return True

    @classmethod
    def addElement(cls, newElement):
       if isinstance(newElement, list) or isinstance(newElement, tuple):
            for elem in newElement:
                if cls.isElementNameUnique(elem.name):
                    cls.subCktElements += [elem]
                else:
                    raise ValueError("Element name " + elem.name + " is not unique.")
       else:
            if cls.isElementNameUnique(newElement.name):
                cls.subCktElements += [newElement]
            else:
                raise ValueError("Element name " + newElement.name + " is not unique.")

    @classmethod
    def anonimize(cls, startIndex=0, netPrefix = "n"):
        """
        Anonimize renames instances and nodes to shorthen their names and
        to strip hieararchy information.
        For example, instances
        Minv1N0 net1 A VSS VSS
        Minv1P0 net1 A VDD VDD
        Minv2N0 Y net1 VSS VSS
        Minv2P0 Y net1 VDD VDD
        contain hierarchy information in their names, and they could be renamed to
        MN0 net1 A VSS VSS
        MP0 net1 A VDD VDD
        MN1 Y net1 VSS VSS
        MP1 Y net1 VDD VDD
        Similar reasoning could be applied to net names.
        """
        # Element counter is a dictionary that contains encountered Symdevices and their current count
        elementCounter = {}
        # Net translator is a dictionary that contains translation between original and short net names
        netTranslator = {}
        # Terminals are top level nets that should not be renamed
        terminals = cls.getTerminals()
        for elem in cls.subCktElements:
            if not isinstance(elem, Symdevice):
                raise ValueError("Anonimize works only with flat circuits.")
            elemType = elem.deviceType
            if elemType in elementCounter:
                # Already encountered such element
                n = elementCounter[elemType] + 1
                elementCounter.update({elemType : n})
            else:
                # New element, add it to elementCounter
                n = 0
                elementCounter.update({elemType : startIndex})
            newName = elem.modelPrefix + str(n)
            elem.name = newName
            elemNodes = elem.getNodes()
            newNodes = []
            for nodeName in elemNodes:
                if nodeName in terminals:
                    # Top level node, do not rename
                    newNodes.append(nodeName)
                else:
                    # Not a top level node, rename it
                    if nodeName not in netTranslator:
                        n = len(netTranslator)
                        newName = netPrefix + str(n)
                        netTranslator.update( {nodeName : newName} )
                        
                    newNodes.append( netTranslator[nodeName] )
            elem.nodes = newNodes

    #************************
    # Instance methods, for subcircuit instances
    #************************

    @staticmethod
    def __new_instance__(cls, instName, instNodes, instParams={}, instFns={}):
        return super(Symsubcircuit, cls).__new__(cls)
    
    def __init__(self, instName, instNodes, instParams={}, instFns={}):
        self.name = instName
        self.nodes = instNodes
        self.parameters = Symdict(self.getDefaultParameters(), localDict=instParams)
        localFns = {"ppar" : self.ppar}
        localFns.update(instFns)
        self.functions = Symdict(self.getDefaultFunctions(), localDict=localFns)

    def ppar(self, name):
        return self.parameters[name]

    @staticmethod
    def isNumber(x):
        try:
            float(x)
            return True
        except ValueError:
            return False 

    def getName(self):
        return self.name
        
    def getNodes(self):
        return self.nodes

    def flatten(self,  circuit = None):
        """
        Flatten subcircuit into a higher level circuit.
        Generic element flattening:
            1. Deep copy an element
            2. Give it a hierarchical name
            3. Rename nodes
            4. Assign parameter evaluator to the new element
            5. Execute custom flatten code
            6. Add the newly created element to the flat circuit
        Returns a list of flat circuit elements.
        """
        if circuit is None:
            # This is top level circuit
            self.hierarchyDelimiter = ""
            self.buildHierarchyName() # Build full hierarchical name
            upperLevelParamDict = Symdict({})
            upperLevelFnDict = Symdict({})
            flatCircuit = Symsubcircuit(self.name + "_flat", self.getTerminals(), self.parameters, self.functions, {})
            isTop = True
        else:
            self.hierarchyDelimiter = circuit.getHierarchyDelimiter() # Get the hierarchy delimiter from circuit
            self.buildHierarchyName(circuit) # Build full hierarchical name
            upperLevelParamDict = circuit.getParameterDict()
            upperLevelFnDict = circuit.getFunctionDict()
            flatCircuit = []
            isTop = False

        paramDict = Symdict(upperLevelParamDict, localDict = copy(self.getParameterDict()))
        pparEvaluator = Symparam(paramDict, upperLevelFnDict)
        pparEvaluator.substitute(paramDict)
        fnDict = Symdict(upperLevelFnDict, localDict = self.getFunctionDict())
        
        
        parameterEvaluator = Symparam(paramDict, fnDict)
        
        for element in  self.getElements():
            if isinstance(element, Symsubcircuit):
                # Another subcircuit. Flatten it into this one
                flat = element.flatten(self)
                for elem in flat:
                    elem.flatten(self)
                    if isTop:
                        flatCircuit.addElement( elem )
                    else:
                        flatCircuit.append( elem )
            else:
                # Circuit element
                hierPath = self.getHierarchyName() + self.getHierarchyDelimiter()
                newElement = deepcopy(element)
                newElement.name =  hierPath + newElement.name
                newNodeNames = []
                for i in range(0,len(newElement.getNodes())):
                    node = newElement.getNodes()[i]
                    if node in self.getTerminals():
                        terminalIndex = self.getTerminals().index(node)
                        pinName = self.nodes[terminalIndex]
                        if circuit is not None:
                            upperLevelPath = circuit.getHierarchyName()
                        else:
                            upperLevelPath = ""
                        if upperLevelPath != "":
                            pinName = upperLevelPath + self.getHierarchyDelimiter() + pinName
                        node = pinName
                    else:
                        node = hierPath + node
                    newNodeNames.append(node)
                newElement.putNodes(tuple(newNodeNames))
                newElement.setParameterEvaluator(parameterEvaluator)
                newElement.evaluateInstanceParameters()
                newElement.flatten(self)
                if isTop:
                    flatCircuit.addElement( newElement )
                else:
                    flatCircuit.append( newElement )
        return flatCircuit

    def buildHierarchyName(self, circuit = None):
        """
        Build hierarchical name
        """
        hierarchyDelimiter = self.getHierarchyDelimiter()
        if circuit is None:
            self.hierarchyName = ""
        else:
            self.hierarchyName = circuit.getHierarchyName() + hierarchyDelimiter + self.name            
                
    def getHierarchyName(self):
        """
        Returns a full hierarchical name
        """
        return self.hierarchyName
        
    def getHierarchyDelimiter(self):
        """
        Returns a hierarchy delimiter obtained from upper level circuit.
        """
        return self.hierarchyDelimiter

    #************************
    # Subcircuit functions
    #************************

    def getFunction(self, fnName):
        if fnName in self.functions:
            return self.functions[fnName]
        else:
            raise ValueError("Function "+fnName+" does not exist")
    
    def addFunction(self, fnName, fn):
        if fnName in self.functions:
            raise ValueError("Function "+fnName+" already exists")
        self.functions.update( {fnName : fn} )
        
    def getFunctionDict(self):
        return self.functions         

    def setFunctionDict(self, fnDict):
        self.functions = fnDict

    #************************
    # Subcircuit parameters
    #************************

    def getParameter(self, paramName):
        if paramName in self.parameters:
            return self.parameters[paramName]
        else:
            raise ValueError("Parameter "+paramName+" does not exist")

    def addParameter(self, paramName, paramValue):
        if paramName in self.parameters:
            raise ValueError("Parameter "+paramName+" already exists")
        self.parameters.update( {paramName : paramValue} )

    def getParameterDict(self):
        return self.parameters            

    def setParameterDict(self, parameterDict):
        self.parameters = parameterDict

    #************************
    # Info methods
    #************************

    @classmethod
    def info(cls):
        ret =  "Subcircuit name : " + cls.getClassName() + "\n"
        ret += "Pins            : " + " ".join(cls.getTerminals()) + "\n"
        ret += "Default params  : " + str(cls.getDefaultParameters().__repr__()) + "\n"
        ret += "Elements        : \n"
        for elem in cls.getElements():
            ret += textwrap.indent(str(elem), '\t') + "\n"
        return ret

    def __str__(self):
        terminals = self.getTerminals()
        nodes = self.getNodes()
        ret =  "Subcircuit      : " + self.getClassName() + "\n"
        ret += "Instance name   : " + self.name + "\n"
        ret += "Pins            : " + " ".join(terminals) + "\n"
        ret += "Connectivity    : " + " ".join(f"{t}->{n}" for t, n in zip(terminals, nodes)) + "\n"
        ret += "Parameters      : " + str(self.parameters.__repr__()) + "\n"
        ret += "Elements        : \n"
        for elem in self.getElements():
            ret += textwrap.indent(str(elem), '\t') + "\n"
        return ret
    
    @classmethod
    def netlist_SPICE(cls):
        res = ".subckt " + cls.subCktClassName + " "
        res += " ".join(cls.subCktTerminals)
        params = cls.getDefaultParameters()
        fns = cls.getDefaultFunctions()

        paramDict = Symdict({}, localDict = params)
        fnDict = Symdict({"ppar" : lambda x:x}, localDict = fns)
        parameterEvaluator = Symparam(paramDict, fnDict)

        for param in params.keys():
            paramVal = parameterEvaluator.substitute(params[param])
            res += " " + param + "=" + str(paramVal)
        res += "\n"
        for elem in cls.getElements():
            if isinstance(elem, Symsubcircuit):
                res += elem.to_SPICE(True, parameterEvaluator)
            else:
                res += elem.to_SPICE()
        res += ".ends\n"
        return res

    @classmethod
    def netlist_CDL(cls, printParams=False):
        from glow_utils.symcheck import Symcheck
        res = ".SUBCKT " + cls.subCktClassName + " "
        res += " ".join(cls.subCktTerminals)
        params = cls.getDefaultParameters()
        fns = cls.getDefaultFunctions()

        paramDict = Symdict({}, localDict = params)
        fnDict = Symdict({"ppar" : lambda x:x}, localDict = fns)
        parameterEvaluator = Symparam(paramDict, fnDict)

        for param in params.keys():
            if printParams:
                paramVal = parameterEvaluator.substitute(params[param])
            res += " " + param + "=" + str(paramVal)
        res += "\n"
        # Add pin info as comment
        check = Symcheck(cls)
        id = check.identifyTerminals()
        inputs = id['I']
        outputs = id['O']
        pwr = id['P']
        gnd = id['G']
        res += "*.PININFO "
        res += ":I ".join(inputs + [""])
        res += ":O ".join(outputs + [""])
        res += ":B ".join(pwr + [""])
        res += ":B ".join(gnd + [""])
        res += "\n"
        for elem in cls.getElements():
            if isinstance(elem, Symsubcircuit):
                res += elem.to_CDL(True, parameterEvaluator)
            else:
                res += elem.to_CDL()
        res += ".ENDS\n"
        return res

    #************************
    # SPICE conversion
    #************************

    def to_SPICE(self, netlistInstance = True, parameterEvaluator = None):
        # If netlistInstance = True, only instantiate the subcircuit,
        # otherwise print the subcircuit definition
        if netlistInstance:
            res = "X" + self.name + " "
            res += " ".join(self.nodes) + " "
            res += self.subCktClassName + " "
            params = self.getParameterDict()
            for param in params.keys():
                if parameterEvaluator is None:
                    paramVal = str(params[param])
                else:
                    paramVal = str(parameterEvaluator.substitute(params[param]))
                if isinstance(paramVal, (int, float)) or self.isNumber(paramVal):
                    res += param + "=" + str(paramVal) + " "
                else:
                    # NGSPICE expression
                    res += param + "={" + str(paramVal) + "} "
            res += "\n"
        else:
            res = self.netlist_SPICE()
        return res

    #************************
    # CDL conversion
    #************************
    def to_CDL(self, netlistInstance = True, parameterEvaluator = None):
        raise ValueError("Hierarchical CDL netlisting is not supported. Use SPICE for hiearchical circuits.")