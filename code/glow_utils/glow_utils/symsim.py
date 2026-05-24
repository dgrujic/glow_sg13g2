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

from glow_utils.symcheck import Symcheck
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symdevice import Symdevice
from glow_utils.symieee1164 import IEEE1164
from copy import copy
from itertools import product
from sympy import symbols
from sympy.logic import SOPform
from sympy.logic import simplify_logic
from sympy import bool_map

class Symsim:
    def __init__(self, circuit : Symsubcircuit, verbose = True):
        self.circuit = circuit
        self.verbose = verbose
        self.nodeChanged = False
        self.results = []
        # Maximum number of delta simulation steps
        self.maxDelta = 1000
        self.error = False
        self.elaborate()
        self.initSim()

    def msg(self, text):
        if self.verbose:
            print(text)

    def elaborate(self):
        """
        Elaborate a circuit
        1. Check if a circuit is flat
        2. Check if a circuit passes ERC
        3. Find inputs, outputs, power and ground
        4. Make a dictionary of all nodes
        """
        check = Symcheck(self.circuit)
        if not check.isFlat():
            raise ValueError("ERROR : Circuit is not flat.")
        self.msg("Symsim::Elaborate: Circuit is flat.")
        if not check.ERC():
            raise ValueError("ERROR : Circuit does not pass ERC.")
        self.msg("Symsim::Elaborate: Circuit passes ERC.")
        # Identify inputs, outputs, power and ground
        id = check.identifyTerminals()
        self.inputs = id['I']
        self.outputs = id['O']
        self.power = id['P'][0]
        self.ground = id['G'][0]
        self.msg("Symsim::Elaborate: Inputs  : " + " ".join(self.inputs))
        self.msg("Symsim::Elaborate: Outputs : " + " ".join(self.outputs))
        self.msg("Symsim::Elaborate: Power   : " + " ".join([self.power]))
        self.msg("Symsim::Elaborate: Ground  : " + " ".join([self.ground]))
        # Make a dictionary of all nodes
        nodes = set()
        for elem in self.circuit.getElements():
            elem : Symdevice
            for node in elem.getNodes():
                nodes.update([node])
        self.msg("Symsim::Elaborate: Nodes   : " + " ".join(list(nodes)))
        self.nodes = dict.fromkeys(nodes, IEEE1164.UNDEFINED)
        self.msg("Symsim::Elaborate: Elaboration OK.")
    
    def printNodes(self):
        """
        Print node states
        """
        for node in self.nodes.keys():
            print(f"{node:<15} : {self.nodes[node].value:<5}")

    def initSim(self):
        """
        Initialize the simulation:
        1. Erase previous results
        2. Initialize nodes
        """
        self.error = False
        self.results = []
        self.initNodes()

    def initNodes(self):
        """
        Initialize node values for simulation:
        1. Set all nodes nodes to 'Z'
        2. Set power node to '1', ground node to '0'
        """
        self.nodes = dict.fromkeys(self.nodes, IEEE1164.Z)
        self.nodes[self.power] = IEEE1164.ONE
        self.nodes[self.ground] = IEEE1164.ZERO

    def propagateNodes(self):
        """
        Propagate node values from previous simulation step.
        Node values are propagated by converting '1' to 'H'
        and '0' to 'L'. Inputs, power and ground are not changed.
        """
        for node in self.nodes.keys():
            if (node not in self.inputs) and (node != self.power) and (node != self.ground):
                val = self.nodes[node]
                if val == IEEE1164.ONE:
                    self.nodes[node] = IEEE1164.H
                elif val == IEEE1164.ZERO:
                    self.nodes[node] = IEEE1164.L

    def setNode(self, node, value : IEEE1164):
        """
        Set the node to a given value.
        Does not allow to change the value of power and ground.
        Keeps track if node value has actually changed.
        """
        if (node != self.power) and (node != self.ground) and (node not in self.inputs):
            if (self.nodes[node] != value):
                self.nodeChanged = True
                self.nodes[node] = value
    
    def setInput(self, node, value : IEEE1164):
        if node in self.inputs:
            self.nodes[node] = value

    def setInputs(self, values):
        """
        Set values of all inputs
        """
        for i in range(len(self.inputs)):
            node = self.inputs[i]
            self.nodes[node] = values[i]

    def getInputNames(self):
        """
        Returns list of input terminal names
        """
        return self.inputs

    def getInputSymbols(self):
        """
        Returns symbols for circuit inputs
        """
        if len(self.inputs) > 0:
            inputs = " ".join(self.inputs)
            res = symbols(inputs)
            # Ensure that return type is always a tuple, even if only one element is returned
            if not isinstance(res, tuple):
                return (res,)
            else:
                return res
        else:
            return None

    def getOutputValues(self):
        """
        Get values of all outputs
        """
        res = []
        for node in self.outputs:
            res.append(self.nodes[node])
        return res
    
    def getOutputNames(self):
        """
        Returns list of output terminal names
        """
        return self.outputs
    
    def areNodeValuesValid(self):
        """
        Check if all node values are valid.
        Node value is valid if it has value 1, 0, H, L or Z.
        """
        for node in self.nodes.keys():
            val = self.nodes[node]
            if val not in [IEEE1164.ONE, IEEE1164.ZERO, IEEE1164.H, IEEE1164.L, IEEE1164.Z]:
                self.error = True
                return False
        return True

    def minterms(self, inputValues, outputValues, outputName = None):
        """
        Returns a list of minterms - input values for which output evaluates to '1'
        """
        res = []
        if outputName is not None:
            # Position of requested output
            nout = self.outputs.index(outputName)
        else:
            nout = 0
        for i in range(len(inputValues)):
            outval = outputValues[i][nout]
            if (outval == IEEE1164.ONE) or (outval == IEEE1164.H):
                # Output evaluates to '1', add inputs to minterm list
                res.append( IEEE1164.toList(inputValues[i]) )
        return res

    def combSim(self):
        """
        Determine combinatorial circuit truth table by simulating it for all input values
        """
        nbits = len(self.inputs)
        allVectors = list(product([IEEE1164.ONE, IEEE1164.ZERO], repeat=nbits))
        self.initSim()
        self.msg("Symsim::combSim: Simulating circuit with " + str(nbits) + " inputs and "+str(len(self.outputs))+" outputs.")
        inputs = []
        outputs = []
        for vector in allVectors:
            self.setInputs(vector)
            self.simstep()
            inStr = IEEE1164.toStr(vector)
            res = self.getOutputValues()
            outStr = IEEE1164.toStr(res)
            self.msg("Symsim::combSim: | " + inStr + " | " + outStr)
            inputs.append(vector)
            outputs.append(res)
        return (inputs, outputs)

    def combFunc(self):
        """
        Return a list of Boolean expressions for outputs
        """
        # Simulate the circuit to get truth tables
        inputs, outputs = self.combSim()
        inputSymbols = self.getInputSymbols()
        res = []
        if inputSymbols is not None:
            for outputName in self.outputs:
                # Determine a Boolean expression for each output
                minterms = self.minterms(inputs, outputs, outputName)
                logicExpr = simplify_logic(SOPform(inputSymbols, minterms))
                res.append(logicExpr)
            return res
        else:
            return IEEE1164.toList(outputs[0])

    def combCheck(self, expectedFns):
        """
        Simulate the function of a combinatorial circuit and check if the output function(s)
        are equivalent to the expected functions.
        expectedFns is a list of expected logic functions of a circuit.
        Returns True if the circuit is sucessfully simulated and simulated logic functions
        are equivalent to Boolean functions given in expectedFns.
        """
        self.msg("*"*80)
        self.msg("Working on circuit : " + self.circuit.getClassName() + "\n")
        logicExpr = self.combFunc()
        self.msg("")
        if not self.error:
            self.msg("Gate logic functions :")
            for fn in logicExpr:
                self.msg("\t"+str(fn))
        else:
            self.msg("ERROR : Simulation error.")
            return False

        for i in range(len(expectedFns)):
            mapping = bool_map(expectedFns[i], logicExpr[i])
            if mapping is None:
                self.msg("ERROR : Circuit function #" + str(i) +" "+str(expectedFns[i])+" does not operate as expected.")
                return False
        return True

    def simstep(self, printDelta = False):
        """
        Simulation step. Update nodes until their values settle or 
        the maximum number of delta iterations has been reached.
        """
        self.propagateNodes()
        ndelta = 0
        while ndelta < self.maxDelta:
            # Perform a delta simulation step
            self.nodeChanged = False
            # Go through all devices and simulate their response
            for elem in self.circuit.getElements():
                elem : Symdevice
                nodeVals = []
                nodes = elem.getNodes()
                for node in nodes:
                    # Get current node values
                    nodeVals.append( self.nodes[node] )
                newNodeVals = elem.sim(nodeVals)
                for i in range(len(newNodeVals)):
                    self.setNode(nodes[i], newNodeVals[i])
            # Print delta step if requested
            if printDelta:
                self.msg("Delta step      : " + str(ndelta))
                self.msg("Node changed    : " + str(self.nodeChanged))
                self.printNodes()
            ndelta += 1
            # Check if steady state has been reached
            if not self.nodeChanged:
                # Steady state, save node values from this step and exit
                self.results.append( copy(self.nodes) )
                if not self.areNodeValuesValid():
                    print("Symsim::simstep: WARNING : Nodes contain invalid values.")
                return
        raise ValueError("Symsim::simstep: ERROR : Circuit didn't converge in " + str(self.maxDelta) +" delta steps.")
