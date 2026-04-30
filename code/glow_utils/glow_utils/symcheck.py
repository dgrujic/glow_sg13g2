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
Symcheck class implements various helper functions and checks for CMOS circuits.
Connectivity:
- Identify inputs, outputs and power pins.
- Check if circuit is flat.
Electrical rules checks:
- Check and raise error if gate is directly connected to power/gnd.
- Check and raise error if bulks are not connected to the same power/gnd.
- Check if there are floating gates.
"""

from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS

class Symcheck():
    def __init__(self, circuit):
        self.circuit = circuit
        if not self.isFlat():
            raise ValueError("Currently only flat circuits are supported.")

    def isFlat(self):
        """
        This method determines if a circuit is flat or hierarchical.
        Returns True if circuit is flat, False if it is hierarchical.
        """
        for elem in self.circuit.getElements():
            if isinstance(elem, Symsubcircuit):
                # This element is a subcircuit, so the circuit is hierarchical
                return False
        return True

    def getTerminalNode(self, element, terminal):
        """
        Returns the node name to which the terminal is connected of a single element.
        """
        tnum = element.getTerminalNumber(terminal)
        return element.getNodes()[tnum]

    def getTerminalNodes(self, terminal, restrictElementType=None):
        """
        This method goes through all circuit elements and returns a set of 
        node names that are connected to a given terminal.
        """
        res = set()
        for element in self.circuit.getElements():
            tnum = element.getTerminalNumber(terminal)
            if restrictElementType is not None:
                if not isinstance(element, restrictElementType):
                    # Skip this element because it is not of a given type
                    continue
            node = element.getNodes()[tnum]
            res.update( [node] )
        return res
    
    def getNodeTerminals(self, node, restrictElementType=None):
        """
        This method goes through all circuit elements and returns a set of 
        terminal names that are connected to a given node.
        """
        res = set()
        for element in self.circuit.getElements():
            if restrictElementType is not None:
                if not isinstance(element, restrictElementType):
                    # Skip this element because it is not of a given type
                    continue
            nodes = element.getNodes()
            if node in nodes:
                ind = nodes.index(node)
                res.update([element.getTerminalNumber(ind)])
        return res

    def identifyTerminals(self):
        """
        This method identifies which subcircuit terminals are inputs, outputs, power and ground.
        Returns a dictionary
        { 'I' : list[input terminal names],
          'O' : list[output terminal names],
          'P' : list[power terminal names],
          'G' : list[ground terminal names]}
        """
        powerNodes = self.getTerminalNodes('B', SymPMOS)
        groundNodes = self.getTerminalNodes('B', SymNMOS)
        gateNodes = self.getTerminalNodes('G')
        terminalNodes = set(self.circuit.getTerminals())
        inputNodes = gateNodes.intersection(terminalNodes)
        drainNodes = self.getTerminalNodes('D')
        sourceNodes = self.getTerminalNodes('S')
        allDS = drainNodes.union(sourceNodes)
        nonPowerDS = allDS.difference(powerNodes, groundNodes)
        outputNodes = nonPowerDS.intersection(terminalNodes)
        return {  'I' : list(inputNodes),
                  'O' : list(outputNodes),
                  'P' : list(powerNodes),
                  'G' : list(groundNodes)}

    def ERC(self):
        """
        This method performs Electrical Rules Check (ERC) on the circuit.
        Returns False if any of the checks fail.
        Checks that are performed:
        1. Check if there are multiple nodes connected to NMOS or PMOS bulks.
        2. Check if gate is directly connected to ground or power.
        3. Check if there are floating gates
        """
        res = True
        id_term = self.identifyTerminals()
        powerNodes = id_term['P']
        groundNodes = id_term['G']
        inputNodes = id_term['I']
        # Check if there are multiple nodes connected to NMOS or PMOS bulks
        if len(powerNodes) != 1:
            print("ERROR : Circuit ", self.circuit.getClassName(), "has multiple nets connected to PMOS bulk nodes :", " ".join(powerNodes) )
            res = False
        if len(groundNodes) != 1:
            print("ERROR : Circuit ", self.circuit.getClassName(), "has multiple nets connected to NMOS bulk nodes :", " ".join(groundNodes) )
            res = False
        # Check if there are gates directly connected to ground or power
        gateNodes = self.getTerminalNodes('G')
        if (len(set(powerNodes).intersection(gateNodes)) > 0):
            print("ERROR : Circuit ", self.circuit.getClassName(), "has gates directly connected to power net.")
            res = False
        if (len(set(groundNodes).intersection(gateNodes)) > 0):
            print("ERROR : Circuit ", self.circuit.getClassName(), "has gates directly connected to ground net.")
            res = False
        # Check if there are floating gates
        drainNodes = self.getTerminalNodes('D')
        sourceNodes = self.getTerminalNodes('S')
        allDS = drainNodes.union(sourceNodes)
        allDS = allDS.union(inputNodes) # gate is not floating if it is connected to input terminal
        floatingGates = gateNodes.difference(allDS)
        if len(floatingGates) > 0:
            print("ERROR : Circuit ", self.circuit.getClassName(), "has floating gates connected to nodes :", " ".join(floatingGates) )
            res = False
        return res        

