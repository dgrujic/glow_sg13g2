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

import subprocess
from itertools import product
from glow_utils.netlist import Netlist
from glow_utils.symcheck import Symcheck

class Ngspice:
    def __init__(self, libraries, includes, conditions, verbose=True):
        defaultConditions = {   "supplyVoltage" : 1.2, 
                                "temperature" : 27.0,
                                "useGear" : True,
                                "tr" : 100e-12,
                                "tf" : 100e-12,
                                "tclk" : 100e-9,
                                "td" : 10e-9,
                                "tstepCombSim" : 1e-9}
        self.libraries = libraries
        self.includes = includes
        self.conditions = defaultConditions
        self.conditions.update( conditions )
        self.subcircuits = {}
        self.instances = {}
        self.dotcommands = []
        self.control = []
        self.verbose = verbose
        self.echoprefix = "!#!#"
        self.measGroups = {}

    def msg(self, message):
        if self.verbose:
            print("Ngspice::", message, "\n")

    def addInstance(self, name, nodes, model, parameters=None):
        # Add instance to circuit
        if name in self.instances.keys():
            self.msg("Instance name " + name + " already exists. Ignoring this instance.")
        else:
            self.instances.update( {name : {"nodes" : nodes, "model" : model, "parameters" : parameters} } )

    def addSubcircuit(self, name, subcircuit):
        if name in self.subcircuits.keys():
            print("ERROR : Subcircuit name " + name + " is already taken.")
            exit(1)
        self.subcircuits.update( { name : subcircuit } )

    def addControl(self, command : str) -> str:
        self.control.append(command)

    def echo(self, toEcho : str) -> str:
        return 'echo "' + self.echoprefix + toEcho + '"'
    
    def measAtTime(self, name : str, expr : str, time ) -> str:
        return 'meas tran ' + name + ' FIND '+ expr + ' AT='+str(time)

    def addMeasGroup(self, groupName : str, measurements):
        # Add a measurement group that can be used with measGroupAtTime
        # Measurement is a tuple (name, expression)
        self.measGroups.update( { groupName : measurements } )

    def alterGroup(self, alterVals):
        # Add a group of alter statements
        # alterVals is a list of tuples (name, value)
        res = ""
        for alter in alterVals:
            name, val = alter
            res += "\talter " + name + " = " + str(val) + "\n"
        return res

    def measGroupAtTime(self, groupName : str, t, addEcho=True):
        # Add measurements from groupName at time t
        # If addEcho = True add echo to netlist
        group = self.measGroups[groupName]
        res = ""
        if addEcho:
            echo = str(t)
        for meas in group:
            name, expr = meas
            name_t = name + "_" + str(t)
            res += " " + self.measAtTime(name_t, expr, t) + "\n"
            if addEcho:
                echo += " " + name + "=$&" + name_t
        res += self.echo(echo)
        return res

    def makeNetlist(self) -> str:
        # Make an ngspice netlist for a given circuit
        res  = "* ngspice testbench \n"
        temp = self.conditions["temperature"]
        for libcorner in self.libraries:
            lib, corner = libcorner
            res += ".lib " + lib + " " + corner + "\n"
        for include in self.includes:
            res += ".include " + include + "\n"
        res += ".temp " + str(temp) + "\n"
        # Add subcircuit definitions
        for name in self.subcircuits.keys():
            res += self.subcircuits[name]
        # Add subcircuit instances
        for name in self.instances.keys():
            nodes = self.instances[name]["nodes"]
            model = self.instances[name]["model"]
            parameters = self.instances[name]["parameters"]
            res += name + " " + " ".join(map(str, nodes))
            if model is not None:
                res += " " + model
            if parameters is not None:
                res += " " + " ".join(map(str, parameters))
            res += "\n"
        
        # Add dot commands
        for command in self.dotcommands:
            res += command + "\n"

        if self.conditions["useGear"]:
            res += ".option method=gear\n"
        
        # Add control
        if len(self.control) > 0:
            res += ".control\n"
            for command in self.control:
                res += "\t" + command + "\n"
            res += ".endc\n"

        res += ".end\n"
        return res

    def arbSource(self, name, waveform, vhigh, td, tr, tf, tclk):
        """
        Make an arbitrary signal source from several PULSE sources.

        """
        res  = ".subckt " + name + " out\n"
        ind = 0
        i = 0
        while i < len(waveform):
            if waveform[i] == 0:
                i += 1
            else:
                # Merge consecutive '1's
                istart = i
                while (i < len(waveform)):
                    if (waveform[i] == 0):
                        break
                    i += 1
                iend = i

                # For each '1' in waveform add one source that produces that pulse
                # Name the source vind, and connect to nodes ind and ind+1
                # Time when pulse starts
                tstart = td + istart * tclk
                tpw = (iend - istart) * tclk
                res += "v" + str(ind) + " " + str(ind+1) + " " + str(ind) + " "
                ind += 1
                res += "pulse(0 " + str(vhigh) + " " + str(tstart) + " " + str(tr) + " " + str(tf) + " " + str(tpw) + " 1 1)\n"
        # Add voltage source to connect the last voltage source to output
        res += "vout " + str(ind) + " out 0\n"
        res += ".ends\n"
        self.addSubcircuit(name, res)
        return td + len(waveform) * tclk

    def run(self, netlist=None, printNetlist=True):
        # Make a circuit netlist and run a simulation
        if netlist is None:
            netlist = self.makeNetlist()
        if printNetlist:
            self.msg(netlist)
        try:
            res = subprocess.run( ["ngspice", "-b"], input=netlist, text=True, capture_output=True, check=True)
        except subprocess.CalledProcessError as err:
            print("ngspice exited with " + str(err.returncode))
            print(err.stdout)
            print(err.stderr)
            exit(1)
        except FileNotFoundError:
            print("ngspice not found")
            exit(1)
        self.msg("*"*40)
        self.msg(res.stdout)
        self.msg("*"*40)

        filtered = []
        for line in res.stdout.split("\n"):
            line = line.strip()
            if line == "":
                continue
            if line.startswith(self.echoprefix):
                filtered.append(line[len(self.echoprefix):])
        return filtered

    def genCombSources(self, inputs):
        # Add arbitrary sources for combinatorial circuit that simulate all combinations of inputs
        # td, tclk, tr, tf and vdd are taken from conditions
        # Return the time duration of arb waveform and vectors
        nbits = len(inputs)
        td = self.conditions['td']
        tr = self.conditions['tr']
        tf = self.conditions['tf']
        tclk = self.conditions['tclk']
        vdd = self.conditions['supplyVoltage']
        allVectors = list(product([False, True], repeat=nbits))
        # Make lists to hold generated waveforms
        waveforms = [[] for _ in range(nbits)]
        for vector in allVectors:
            for i in range(len(vector)):
                if vector[i]:
                    waveforms[i].append(1)
                else:
                    waveforms[i].append(0)
        # Generate arb sources
        twave = 0
        # Assign ID to allow multiple combinatorial sources
        id = len(self.instances)
        for i in range(nbits):
            name = "ARB"+str(id)+"_"+str(i)
            twave = self.arbSource(name, waveforms[i], vdd, td, tr, tf, tclk)
            # Add source to netlist
            self.addInstance("X"+name, [inputs[i]], name, None)
        return (twave, allVectors)
    
    def combSim(self, netlistFile, circuitName, toLogic=True):
        # Read netlist, deduce inputs and outputs and run ngspice simulations over all input vectors.
        # Returns a tuple (inputs, outputs)
        # If toLogic = False returns simulated voltages
        # If toLogic = True returns logic values
        netlist = Netlist(netlistFile, self.verbose)
        circuit = netlist.makeCircuit(circuitName)
        check = Symcheck(circuit)
        id = check.identifyTerminals()
        inputs = sorted(id['I'])
        outputs = sorted(id['O'])
        power = id['P']
        if len(power) != 1:
            print("ERROR : Circuit should have exactly one power node, but found", str(len(power)), "nodes")
            exit(1)
        power = power[0]
        ground = id['G']
        if len(ground) != 1:
            print("ERROR : Circuit should have exactly one ground node, but found", str(len(ground)), "nodes")
            exit(1)
        ground = ground[0]

        # Add netlist file to include list
        self.includes.append(netlistFile)

        # Add circuit instance
        nodes = []
        nodes += inputs
        nodes += outputs
        nodes.append( power )
        nodes.append( '0' ) # ground
        self.addInstance("XDUT", nodes, circuitName, None)

        # Add supply voltage
        vddVal = self.conditions['supplyVoltage']
        self.addInstance('VSUP', [power, '0'], None, [str(vddVal)])

        tsim, allVectors = self.genCombSources(inputs)

        tstep = self.conditions["tstepCombSim"]
        self.addControl("tran " + str(tstep) + " " + str(tsim))

        measGroup = []
        for name in inputs:
            measGroup.append( (name, 'v('+name+')') )
        for name in outputs:
            measGroup.append( (name, 'v('+name+')') )
        
        self.addMeasGroup("signals", measGroup)
        td = self.conditions["td"]
        tclk = self.conditions["tclk"]
        t0 = td + 0.9 * tclk
        for i in range(len(allVectors)):
            self.addControl(self.measGroupAtTime("signals", t0 + i * tclk, True))
        
        inputVals = []
        outputVals = []
        res = self.run()
        for step in res:
            expr = step.split()
            inputRow = [1e9 for _ in range(len(inputs))]
            outputRow = [1e9 for _ in range(len(outputs))]
            for vals in expr[1:]:
                if ('=' in vals):
                    name, val  = vals.split('=')
                    if name in inputs:
                        ind = inputs.index(name)
                        inputRow[ind] = float(val)
                    if name in outputs:
                        ind = outputs.index(name)
                        outputRow[ind] = float(val)
            inputVals.append(inputRow)
            outputVals.append(outputRow)

        if not toLogic:
            return (inputs, inputVals, outputs, outputVals)
        else:
            vt = self.conditions['supplyVoltage']/2
            inputVals01 = [['1' if val > vt else '0' for val in row] for row in inputVals]
            outputVals01 = [['1' if val > vt else '0' for val in row] for row in outputVals]
            return (inputs, inputVals01, outputs, outputVals01)


