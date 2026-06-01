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
import numpy as np

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

        self.rinit = 1e4

        self.highThreshold = 0.9
        self.lowThreshold = 0.1

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
        self.inputs = sorted(id['I'])
        self.outputs = sorted(id['O'])
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
        self.msg("Symsim::Elaborate: Nodes   : " + " ".join(sorted(list(nodes))))
        self.nodes = dict.fromkeys(nodes, IEEE1164.UNDEFINED)
        self.msg("Symsim::Elaborate: Elaboration OK.")
    
    def printNodes(self):
        """
        Print node states
        """
        nodes = sorted(self.nodes.keys())
        for node in nodes:
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

    def iterNodes(self):
        nodes = self.nodes.copy()
        for node in nodes.keys():
            if (node not in self.inputs) and (node != self.power) and (node != self.ground):
                nodes[node] = IEEE1164.Z

    def setNode(self, node, value : IEEE1164):
        """
        Set the node to a given value.
        Does not allow to change the value of power and ground.
        Keeps track if node value has actually changed.
        """
        if (node != self.power) and (node != self.ground) and (node not in self.inputs):
            if (self.nodes[node] != value):
                self.nodeChanged = True
                #self.nodes[node] = value
                self.nodes[node] = IEEE1164.resolve(self.nodes[node], value)

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

    def getInputValues(self):
        """
        Get values of all inputs
        """
        res = []
        for node in self.inputs:
            res.append(self.nodes[node])
        return res

    def getOutputValues(self):
        """
        Get values of all outputs
        """
        res = []
        for node in self.outputs:
            res.append(self.nodes[node])
        return res

    def getOutputValue(self, node):
        """
        Get values of one output
        """
        return self.nodes[node]

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

    def filterResults(self, nodeNames):
        """
        Extract simulation results node values given in nodeNames.
        Convert to 1/0 if toLogic = True.
        """
        res = {}
        for node in nodeNames:
            res.update( { node : [] } )

        for step in self.results:
            for node in nodeNames:
                val = step[node]
                res[node].append( val )
        return res

    def plotResults(self, vals, start=None, end=None):
        """
        Text plot of results given in res.
        If given, start and end define staring and ending index
        """
        maxNameLen = max(map(len, vals))
        valLen = len(vals[list(vals.keys())[0]])
        res = {}
        for name in vals.keys():
            sname = name.ljust(maxNameLen + 2)
            res.update( {name : sname} )
        if start is not None:
            sInd = min(start, valLen)
        else:
            sInd = 0
        if end is not None:
            eInd = min(end, valLen)
        else:
            eInd = valLen
        
        for name in vals.keys():
            prev = vals[name][sInd].value
            sres = res[name]
            for i in range(sInd, eInd):
                cur = vals[name][i].value
                if prev == cur:
                    if cur == '1':
                        sres += "\u203e\u203e"
                    elif cur == '0':
                        sres += "__"
                    else:
                        sres = sres + cur + cur
                else:
                    if cur == '1':
                        sres += "|\u203e"
                    elif cur == '0':
                        sres += "|_"
                    else:
                        sres = sres + cur + cur
                prev = cur
            res[name] = sres
        return res

    #######################################
    # Combinatorial circuits
    #######################################

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

    #######################################
    # Sequential circuits
    #######################################

    def dffParse(self, spec):
        # Parse given FF specification

        # Parse specification and make a dictionary with the following keys
        # | Variable  | Description                                 |
        # |-----------|---------------------------------------------|
        # |   dPin    | Pin name for D input                        |
        # |   dInv    | Is data input inverted?                     |
        # |   qPin    | Pin name for Q output. None if not present. |
        # |   qnPin   | Pin name for QN output. None if not present.|
        # |  clkPin   | Pin name for CLK input.                     |
        # |  clkInv   | Is clock inverted?                          |
        # |  hasEn    | FF has an enable pin?                       |
        # |  enPin    | Pin name for enable.                        |
        # |  enInv    | Is enable inverted?                         |
        # | hasSCVAL  | Is value for simultaneous set/clear given?  |
        # |  SCVAL    | Output value for simultaneous set/clear.    |
        # | hasClr    | FF has CLR pin?                             |
        # | clrPin    | Pin name for CLR.                           |
        # | clrInv    | Is CLR inverted?                            |
        # | asyncClr  | Is CLR asynchronous?                        |
        # | hasSet    | FF has SET pin?                             |
        # | setPin    | Pin name for SET.                           |
        # | setInv    | Is SET inverted?                            |
        # | asyncSet  | Is SET asynchronous?                        |
        #
        # Based on these flags, active/inactive signal values are determined
        # | Variable  | Description                                 |
        # |-----------|---------------------------------------------|
        # |   dAct    | Active ('1') value for data input.          |
        # |   dIdle   | Idle ('0') value for data input.            |
        # |  clkAct   | Active value for clock input.               |
        # | clkIdle   | Idle value for clock input.                 |
        # |  enAct    | Active value for enable input.              |
        # |  enIdle   | Idle value for enable input.                |
        # |  clrAct   | Active value for clear input.               |
        # | clrIdle   | Idle value for clear input.                 |
        # |  setAct   | Active value for set input.                 |
        # | setIdle   | Idle value for set input.                   |

        # Make a dictionary containing all valid keys with value None to avoid errors from missing keys
        keys = ['D', 'DN', 'Q', 'QN', 'CLK', 'CLKN',
                'ACLR', 'ACLRN', 'CLR', 'CLRN',
                'ASET', 'ASETN', 'SET', 'SETN',
                'EN', 'ENB', 'SCVAL']
        ispec = dict.fromkeys(keys, None)
        # Update specification with given values
        ispec.update(spec)
        
        # Check if the specification is valid
        # Check D/DN
        d, dn = ispec['D'], ispec['DN']

        if (d is None) == (dn is None):
            error_msg = 'Input is not specified' if d is None else 'Both D and DN are given'
            self.msg(f'Symsim::ffCheck:ERROR: {error_msg}')
            return False

        dPin = dn if d is None else d
        dInv = d is None

        # Check Q/QN
        if ispec['Q'] is None and ispec['QN'] is None:
            self.msg('Symsim::ffCheck:ERROR: Output is not specified')
            return False

        qPin = ispec.get('Q')
        qnPin = ispec.get('QN')

        # Check CLK/CLKN
        clk = ispec['CLK']
        clkn = ispec['CLKN']

        if clk is None and clkn is None:
            self.msg('Symsim::ffCheck:ERROR: Clock is not specified')
            return False
        
        if clk is not None and clkn is not None:
            self.msg('Symsim::ffCheck:ERROR: Both CLK and CLKN are given')
            return False

        clkPin = clk if clk is not None else clkn
        clkInv = clk is None
        
        # Check EN/ENB
        if ispec['EN'] is not None and ispec['ENB'] is not None:
            self.msg('Symsim::ffCheck:ERROR: Both EN and ENB are given')
            return False

        hasEn = ispec['EN'] is not None or ispec['ENB'] is not None
        enPin = ispec['EN'] or ispec['ENB'] if hasEn else None
        enInv = False if ispec['EN'] is not None else (True if hasEn else None)
        
        # Check SCVAL
        SCVAL = ispec['SCVAL']
        hasSCVAL = SCVAL is not None

        # Check CLR
        # Check for mutually exclusive sets upfront
        has_sync_clr = (ispec['CLR'] is not None) and (ispec['CLRN'] is not None)
        has_async_clr = (ispec['ACLR'] is not None) and (ispec['ACLRN'] is not None)

        if has_sync_clr and has_async_clr:
            self.msg('Symsim::ffCheck:ERROR: Both synchronous and asynchronous CLR are given')
            return False

        # Extract the appropriate pins based on availability
        if has_sync_clr:
            hasClr, asyncClr = True, False
            clrPin = ispec['CLR'] if ispec['CLR'] is not None else ispec['CLRN']
            clrInv = False if ispec['CLR'] is not None else True
        elif has_async_clr:
            hasClr, asyncClr = True, True
            clrPin = ispec['ACLR'] if ispec['ACLR'] is not None else ispec['ACLRN']
            clrInv = False if ispec['ACLR'] is not None else True
        else:
            hasClr, asyncClr, clrPin, clrInv = False, None, None, None

        # Check SET
        # Check for mutually exclusive synchronous/asynchronous SET pins
        sync_set = (ispec['SET'] is not None, ispec['SETN'] is not None)
        async_set = (ispec['ASET'] is not None, ispec['ASETN'] is not None)

        if all(sync_set) and all(async_set):
            self.msg('Symsim::ffCheck:ERROR: Both synchronous and asynchronous SET are given')
            return False

        # Determine SET type and extract pin/inv states
        if all(sync_set):
            hasSet, asyncSet = True, False
            setPin = ispec['SET'] if ispec['SET'] is not None else ispec['SETN']
            setInv = (ispec['SET'] is None)
        elif all(async_set):
            hasSet, asyncSet = True, True
            setPin = ispec['ASET'] if ispec['ASET'] is not None else ispec['ASETN']
            setInv = (ispec['ASET'] is None)
        else:
            hasSet, asyncSet, setPin, setInv = False, None, None, None

        # Determine active/inactive signal values
        clkAct = IEEE1164.ZERO if clkInv else IEEE1164.ONE
        clkIdle = IEEE1164.ONE if clkInv else IEEE1164.ZERO
        
        dAct = IEEE1164.ZERO if dInv else IEEE1164.ONE
        dIdle = IEEE1164.ONE if dInv else IEEE1164.ZERO

        if hasEn:
            enAct = IEEE1164.ZERO if enInv else IEEE1164.ONE
            enIdle = IEEE1164.ONE if enInv else IEEE1164.ZERO
        else:
            enAct = None
            enIdle = None
            
        if hasClr:
            clrAct  = IEEE1164.ZERO if clrInv else IEEE1164.ONE
            clrIdle = IEEE1164.ONE  if clrInv else IEEE1164.ZERO
        else:
            clrAct = None
            clrIdle = None

        if hasSet:
            setAct = IEEE1164.ZERO if setInv else IEEE1164.ONE
            setIdle = IEEE1164.ONE if setInv else IEEE1164.ZERO
        else:
            setAct = None
            setIdle = None  
        
        res = { 'dPin' : d, 'dInv' : dInv, 'qPin' : qPin, 'qnPin' : qnPin,
                'clkPin' : clkPin, 'clkInv' : clkInv,
                'hasEn' : hasEn, 'enPin' : enPin, 'enInv' : enInv,
                'enAct' : enAct, 'enIdle' : enIdle,
                'hasSCVAL' : hasSCVAL, 'SCVAL' : SCVAL,
                'hasClr' : hasClr, 'clrPin' : clrPin , 'clrInv' : clrInv,
                'hasSet' : hasSet, 'setPin' : setPin , 'setInv' : setInv,
                'asyncClr' : asyncClr, 'asyncSet' : asyncSet,
                'dAct' : dAct, 'dIdle' : dIdle,
                'clkAct' : clkAct, 'clkIdle' : clkIdle,
                'clrAct' : clrAct, 'clrIdle' : clrIdle,
                'setAct' : setAct, 'setIdle' : setIdle}
        return res

    def dffCheck(self, spec):
        """
        Check a D flip-flop according to a given specification spec.
        spec is a dictionary containing a description of flip-flop
        Key     Description
        'D'     Name of data input pin or None
        'DN'    Name of inverted data input pin or None
        'Q'     Name of output or None
        'QN'    Name of inverted output or None
        'CLK'   Name of clock input or None
        'CLKN'  Name of inverted clock input or None
        'ACLR'  Name of asynchronous active high clear pin or None
        'ACLRN' Name of asynchronous active low clear pin or None
        'CLR'   Name of synchronous active high clear pin or None
        'CLRN'  Name of synchronous active low clear pin or None    
        'ASET'  Name of asynchronous active high set pin or None
        'ASETN' Name of asynchronous active low set pin or None
        'SET'   Name of synchronous active high set pin or None
        'SETN'  Name of synchronous active low set pin or None
        'EN'    Name of synchronous active high enable pin or None
        'ENB'   Name of synchronous active low enable pin or None
        'SCVAL' Value of output when both set and clear are active or None
        """

        self.initSim()

        self.pspec = self.dffParse(spec)

        self.msg("Symsim::dffCheck: Simulating D flip-flop with specification")
        self.msg("\n".join(f"\t{key} : {value}" for key, value in self.pspec.items()))

        # Set all inputs to inactive values
        self.dffInactive()
        # Set enable to active
        self.dffEN(True)
        self.simstep()

        for val in [False, True]:
            # Check if data writing works
            self.dffD(val)
            self.dffCLK(False)
            self.simstep()
            self.dffCLK(True)
            self.simstep()
            if not self.dffCheckQ(val):
                self.msg("Symsim::dffCheck: ERROR : Write value " + str(val) + "failed")
                return False
        self.msg("Symsim::dffCheck: Writing values to DFF works as expected. PASS.")

        # Check if changing the data with constant clock changes the output
        for val in [False, True]:
            # Check if data retention works
            self.dffD(val)
            self.dffCLK(False)
            self.simstep()
            self.dffCLK(True)
            self.simstep()
            for x in [False, True, False, True]:
                self.dffD(x)
                self.simstep()
                if not self.dffCheckQ(val):
                    self.msg("Symsim::dffCheck: ERROR :  Check on value " + str(val) + "failed")
                    return False
            self.dffCLK(False)                
            for x in [False, True, False, True]:
                self.dffD(x)
                self.simstep()
                if not self.dffCheckQ(val):
                    self.msg("Symsim::dffCheck: ERROR :  Check on value " + str(val) + "failed")
                    return False
        self.msg("Symsim::dffCheck: DFF retains value on input change. PASS.")
        
        # Check if EN works
        if self.pspec['hasEn']:
            self.dffEN(False)
            expected = self.dffGetQ()
            for val in [False, True]:
                # Check if data writing works
                self.dffD(val)
                self.dffCLK(False)
                self.simstep()
                self.dffCLK(True)
                self.simstep()
                if not self.dffCheckQ(expected):
                    self.msg("Symsim::dffCheck: ERROR : Enable check failed")
                    return False
            self.msg("Symsim::dffCheck: DFF enable works as expected. PASS.")
            self.dffEN(True)
        else:
            self.msg("Symsim::dffCheck: DFF does not have an EN input.")

        # Check if CLR works
        if self.pspec['hasClr']:
            # Set output to 1 so it can be cleared
            self.dffD(True)
            self.dffCLK(False)
            self.simstep()
            self.dffCLK(True)
            self.simstep()
            self.dffCLK(False)
            self.simstep()

            if self.pspec['asyncClr'] == True:
                self.dffCLR(True)
                self.simstep()
                if not self.dffCheckQ(False):
                    self.msg("Symsim::dffCheck: ERROR : Asynchronous clear is not working as expected.")
                    return False
                else:
                    self.msg("Symsim::dffCheck: Asynchronous clear is working as expected. PASS.")
            else:
                self.dffCLR(True)
                self.simstep()
                if not self.dffCheckQ(True):
                    self.msg("Symsim::dffCheck: ERROR : Synchronous clear is not working as expected.")
                    return False
                self.dffCLK(True)
                self.simstep()
                self.dffCLK(False)
                self.simstep()
                if not self.dffCheckQ(False):
                    self.msg("Symsim::dffCheck: ERROR : Synchronous clear is not working as expected.")
                    return False
                else:
                    self.msg("Symsim::dffCheck: Synchronous clear is working as expected. PASS.")
            self.dffCLR(False)
            self.simstep()
        else:
            self.msg("Symsim::dffCheck: DFF does not have a CLR input.")

        # Check if SET works
        if self.pspec['hasSet']:
            # Set output to 0 so it can be cleared
            self.dffD(False)
            self.dffCLK(False)
            self.simstep()
            self.dffCLK(True)
            self.simstep()
            self.dffCLK(False)
            self.simstep()

            if self.pspec['asyncSet'] == True:
                self.dffSET(True)
                self.simstep()
                if not self.dffCheckQ(True):
                    self.msg("Symsim::dffCheck: ERROR : Asynchronous set is not working as expected.")
                    return False
                else:
                    self.msg("Symsim::dffCheck: Asynchronous set is working as expected. PASS.")
            else:
                self.dffSET(True)
                self.simstep()
                if not self.dffCheckQ(False):
                    self.msg("Symsim::dffCheck: ERROR : Synchronous set is not working as expected.")
                    return False
                self.dffCLK(True)
                self.simstep()
                self.dffCLK(False)
                self.simstep()
                if not self.dffCheckQ(True):
                    self.msg("Symsim::dffCheck: ERROR : Synchronous set is not working as expected.")
                    return False
                else:
                    self.msg("Symsim::dffCheck: Synchronous clear is working as expected. PASS.")
            self.dffSET(False)
            self.simstep()
        else:
            self.msg("Symsim::dffCheck: DFF does not have a SET input.")

        # Check if simultaneous CLR and SET works as expected
        if self.pspec['hasSet'] and self.pspec['hasClr'] and (self.pspec['SCVAL'] is not None):
            self.dffSET(True)
            self.dffCLR(True)
            self.dffCLK(False)
            self.simstep()
            self.dffCLK(True)
            self.simstep()
            self.dffCLK(False)
            self.simstep()
            if not self.dffCheckQ(self.pspec['SCVAL']):
                self.msg("Symsim::dffCheck: ERROR : SCVAL is not working as expected.")
                return False
            else:
                self.msg("Symsim::dffCheck: ERROR : SCVAL is working as expected. PASS.")
        else:
            self.msg("Symsim::dffCheck: DFF does not have a SCVAL condition.")
        self.msg("Symsim::dffCheck: All checks passed.")
        return True

    def dffInactive(self):
        # Set all inputs to inactive values
        self.dffCLK(False)
        self.dffD(False)
        self.dffEN(False)
        self.dffCLR(False)
        self.dffSET(False)

    def dffCLK(self, val):
        # If val = True set FF clk to active value, otherwise to inactive value
        if val:
            self.setInput(self.pspec['clkPin'], self.pspec['clkAct'])
        else:
            self.setInput(self.pspec['clkPin'], self.pspec['clkIdle'])

    def dffD(self, val):
        # If val = True set FF data to active value, otherwise to inactive value
        if val:
            self.setInput(self.pspec['dPin'], self.pspec['dAct'])
        else:
            self.setInput(self.pspec['dPin'], self.pspec['dIdle'])

    def dffEN(self, val):
        # If val = True set FF enable to active value, otherwise to inactive value
        if self.pspec['hasEn']:
            if val:
                self.setInput(self.pspec['enPin'], self.pspec['enAct'])
            else:
                self.setInput(self.pspec['enPin'], self.pspec['enIdle'])

    def dffCLR(self, val):
        # If val = True set FF clear to active value, otherwise to inactive value
        if self.pspec['hasClr']:
            if val:
                self.setInput(self.pspec['clrPin'], self.pspec['clrAct'])
            else:
                self.setInput(self.pspec['clrPin'], self.pspec['clrIdle'])

    def dffSET(self, val):
        # If val = True set FF set to active value, otherwise to inactive value
        if self.pspec['hasSet']:
            if val:
                self.setInput(self.pspec['setPin'], self.pspec['setAct'])
            else:
                self.setInput(self.pspec['setPin'], self.pspec['setIdle'])

    def dffCheckQ(self, val):
        # Check if outputs have expected values.
        # If val = True => Q = IEEE1164.ONE and QN = IEEE1164.ZERO
        # If val = False => Q = IEEE1164.ZERO and QN = IEEE1164.ONE
        qPin = self.pspec['qPin']
        qnPin = self.pspec['qnPin']
        resOK = True
        if qPin is not None:
            if val:
                if self.getOutputValue(qPin) != IEEE1164.ONE:
                    resOK = False
            else:
                if self.getOutputValue(qPin) != IEEE1164.ZERO:
                    resOK = False
        if qnPin is not None:
            if val:
                if self.getOutputValue(qnPin) != IEEE1164.ZERO:
                    resOK = False
            else:
                if self.getOutputValue(qnPin) != IEEE1164.ONE:
                    resOK = False
        return resOK

    def dffGetQ(self):
        # Return Q value
        qPin = self.pspec['qPin']
        qnPin = self.pspec['qnPin']
        if qPin is not None:
            if self.getOutputValue(qPin) == IEEE1164.ONE:
                return True
            else:
                return False        
        if qnPin is not None:
            if self.getOutputValue(qnPin) == IEEE1164.ZERO:
                return True
            else:
                return False
        return None

    #######################################
    # Simulation methods
    #######################################

    def simstep(self, printDelta = False):
        """
        Simulation step. Update nodes until their values settle or 
        the maximum number of delta iterations has been reached.
        """
        ndelta = 0
        while ndelta < self.maxDelta:
            # Perform a delta simulation step
            newNodes = self.simMNA(self.nodes)
            ndelta += 1
            # Check if steady state has been reached
            if self.nodes == newNodes:
                # Steady state, save node values from this step and exit
                self.nodes = newNodes
                self.results.append( copy(self.nodes) )
                if not self.areNodeValuesValid():
                    print("Symsim::simstep: WARNING : Nodes contain invalid values.")
                return
            # Update node values and execute a new delta step
            self.nodes = newNodes
            if printDelta:
                self.msg("Delta step      : " + str(ndelta))
                self.printNodes()
        raise ValueError("Symsim::simstep: ERROR : Circuit didn't converge in " + str(self.maxDelta) +" delta steps.")

    def simMNA(self, initialState):
        """
        Construct MNA for this circuit and solve it.
        initialState is a dictionary of node names as keys and node values as values.
        initialState determines if node should be connected to ground or power
        through weak resistor to define the state of floating nodes.
        """
        allNodeNames = sorted(self.nodes.keys())
        # Internal nodes
        intNodes = []
        for node in allNodeNames:
            if (node not in self.inputs) and (node not in self.power) and (node not in self.ground):
                intNodes.append(node)
        numIntNodes = len(intNodes)
        indIntNodes = {item: index for index, item in enumerate(intNodes)}

        inputNodes = sorted(self.inputs)
        numInputs = len(self.inputs)    

        numPower = 1
        powerNode = self.power
        groundNode = self.ground
        
        mnaSize = numIntNodes + 2*numInputs + 2*numPower
        indPower = numIntNodes + numInputs
        
        baseInput = numIntNodes
        indInputs = {item: (baseInput+index) for index, item in enumerate(inputNodes)}

        # indNodes is a dictionary of node indexes in MNA
        indNodes = {}
        indNodes.update(indIntNodes)
        indNodes.update(indInputs)
        indNodes.update( {powerNode : indPower} )

        state = copy(initialState)
        for node in initialState.keys():
            if (initialState[node] == IEEE1164.H) or (initialState[node] == IEEE1164.ONE):
                state[node] = 1.0
            else:
                state[node] = 0.0

        # Fill MNA with weak pullup or pulldown resistors to match initial state 
        mna = np.zeros( (mnaSize, mnaSize) )
        # Fill mna with initial state
        for node in state.keys():
            #if (node not in self.inputs) and (node not in self.power) and (node not in self.ground):
            if (node not in self.ground):
                val = state[node]
                if (val > self.highThreshold):
                    # Add weak resistor from node to power supply
                    mna[ indNodes[node], indNodes[node] ] += 1.0/self.rinit
                    mna[ indNodes[powerNode], indNodes[powerNode] ] += 1.0/self.rinit
                    mna[ indNodes[node], indNodes[powerNode] ] += -1.0/self.rinit
                    mna[ indNodes[powerNode], indNodes[node] ] += -1.0/self.rinit
                else:
                    # Add weak resistor from node to ground
                    mna[ indNodes[node], indNodes[node] ] += 1.0/self.rinit

        # Fill MNA with transistor equivalents
        for elem in self.circuit.getElements():
            d, g, s, b = elem.getNodes()
            nodeVals = []
            nodes = elem.getNodes()
            for node in nodes:
                # Get current node values
                nodeVals.append( state[node] )
            rval = elem.simR(nodeVals)
            if d == groundNode:
                # Drain is grounded, add r from source to ground
                mna[ indNodes[s], indNodes[s] ] += 1.0/rval
            elif s == groundNode:
                # Source is grounded, add r from drain to ground
                mna[ indNodes[d], indNodes[d] ] += 1.0/rval
            else:
                # Floating element
                mna[ indNodes[s], indNodes[s] ] += 1.0/rval
                mna[ indNodes[d], indNodes[d] ] += 1.0/rval
                mna[ indNodes[s], indNodes[d] ] += -1.0/rval
                mna[ indNodes[d], indNodes[s] ] += -1.0/rval

        # Add entries for independent voltage sources
        nNodes = indPower + 1
        for node in inputNodes:
            ind = indNodes[node] # node index of input
            mna[ ind, nNodes + ind - baseInput ] = 1.0
            mna[ nNodes + ind - baseInput, ind ] = 1.0
        # Add entry for power
        mna[ indPower, nNodes + indPower - baseInput  ] = 1.0
        mna[ nNodes + indPower -baseInput, indPower ] = 1.0

        # Fill RHS with input values
        rhs = np.zeros( mnaSize )
        for node in inputNodes:
            if (initialState[node] == IEEE1164.ONE) or (initialState[node] == IEEE1164.H):
                inVal = 1.0
            else:
                inVal = 0.0
            rhs[ indNodes[node] - baseInput + nNodes ] = inVal
        # Add power
        rhs[ indNodes[powerNode] - baseInput + nNodes ] = 1.0

        try:
            sol = np.linalg.solve(mna, rhs)
        except:
            # Failed to solve the system, possibly a singular matrix
            self.msg("Symsim::simMNA:ERROR : MNA solving failed, possibly a singular matrix.")
            res = dict.fromkeys(initialState.keys(), IEEE1164.X)
            return res

        # Construct the output values
        res = {}
        for i in range(numIntNodes):
            x = sol[i]
            if x > self.highThreshold:
                val = IEEE1164.ONE
            elif x < self.lowThreshold:
                val = IEEE1164.ZERO
            else:
                val = IEEE1164.X
            res.update( {intNodes[i] : val} )
        for i in range(numInputs):
            node = inputNodes[i]
            res.update( {node : initialState[node]} )
        
        res.update( {powerNode : IEEE1164.ONE} )
        res.update( {groundNode : IEEE1164.ZERO} )
        return res
