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

from glow_utils.symparam import Symparam
from glow_utils.symdict import Symdict

#///////////////////////////////////////////////////////////////////////////////////////
# Circuit element base class
#///////////////////////////////////////////////////////////////////////////////////////

class Symdevice(object):
    """
    Circuit element base class
    """
    deviceType = "unspecified"
    modelName = "symdevice"

    def __init__(self, name, nodes, parameters):
        """
        Calling Init() and avoiding overloading of __init__ is intentional to
        ensure that all elements have the same interface.
        """
        self.name = name
        self.nodes = nodes
        self.parameters = parameters
        self.parameterEvaluator = None  # Symparam instance
        self.functions = {"ipar" : self.ipar}
        self.initInstance()

    def ipar(self, name):
        """
        Returns instance parameter value with a given name
        """
        return self.parameters[name]

    def initInstance(self):
        """
        Custom initialization code called upon device creation
        """
        pass

    def finalizeElaboration(self, circuit):
        """
        Custom code called during elaboration phase, after the circuit has been assembled,
        node numbers assigned and all element parameters have been evaluated.
        This method can query the circuit to get the needed information.
        For example, mutual inductance component can query the circuit to find out the numbers
        of associated inductors and their inductance.
        """
        pass
        
    def assignNodes(self, nodeNumbers):
        """
        
        """
        if len(nodeNumbers)!=len(self.nodes):
            raise ValueError(self.name+" has "+str(len(self.nodes))+" nodes, but "+str(len(nodeNumbers))+" node numbers given")
        self.nodeNumbers = nodeNumbers

    def getParameterEvaluator(self):
        return self.parameterEvaluator
        
    def setParameterEvaluator(self, parameterEvaluator):
        self.parameterEvaluator = parameterEvaluator                

    def evaluateInstanceParameters(self):
        """
        Function to evaluate the instance parameters.
        The parameters are evaluated and inserted into instance dictionary.
        """
        for paramName in self.parameters:
            if self.isParameterEvaluated(paramName):
                paramExpr = self.parameters[paramName]
                paramValue = self.parameterEvaluator.evaluate(paramExpr, instanceFns = self.functions)
                self.parameters.update( {paramName : paramValue} )
        self.evaluateInstanceParametersCustom()

    def evaluateInstanceParametersCustom(self):
        """
        Custom code called after the instance parameters have been evaluated
        """
        pass

    def evalInternalFns(self, expr):
        """
        Perform symbolic substitution of device internal functions
        """
        parameterEvaluator = Symparam(self.parameters, self.functions)
        subsExpr = parameterEvaluator.substitute(expr, allowSymbols=True)
        return subsExpr

    def getNodes(self):
        """
        Return the component's nodes.
        """
        return self.nodes        

    def putNodes(self, nodes):
        """
        Put the component nodes.
        """
        if len(self.nodes) != len(nodes):
            raise ValueError("Component "+self.name+" has "+str(len(self.nodes))+" nodes, but "+str(len(nodes))+" nodes given")
        self.nodes = nodes

    def hasParameter(self, paramName):
        """
        Check if device has a parameter with name paramName
        """
        if paramName in self.parameters.keys():
            return True
        return False
    def isParameterEvaluated(self, paramName):
        """
        Function to indicate if parameter should be evaluated.
        """
        return True

    def getDeviceType(self):
        return self.deviceType

    def getParameters(self):
        """
        Return the component's parameters
        """
        return self.parameters
       
    def getName(self):
        """
        Return the component's name
        """
        return self.name        

    def getModelName(self):
        """
        Return the component's model name
        """
        return self.modelName

    def setModelName(self, modelName):
        """
        Set the component's model name
        """
        self.modelName = modelName

    def flatten(self, subcircuit):
        """
        Custom flatten code.
        """    
        pass    

    def info(self):
        """
        Returns a string with component description
        """
        return "Symdevice base class"
        
    def __str__(self):
        res =  "Circuit element : " +type(self).__name__ + "\n"
        res += "Device type     : " + self.getDeviceType() + "\n"
        res += "Instance name   : " + self.name + "\n"
        res += "Nodes           : " + " ".join(self.nodes) + "\n"
        res += "Parameters      : " + self.parameters.__repr__()
        res += "\n"
        return res
