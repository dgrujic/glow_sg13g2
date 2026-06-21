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
    def __init__(self, libraries, includes, conditions, netlistFile, circuitName, verbose=True):
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
        self.verbose = verbose
        self.echoprefix = "!#!#"
        self.clear()
        self.circuitName = circuitName
        self.netlistFile = netlistFile
        self.dutFromNetlist(netlistFile, circuitName)

    def clear(self):
        # Clear current state for new simulation
        self.parameters = []
        self.subcircuits = {}
        self.instances = {}
        self.dotcommands = []
        self.control = []
        self.measGroups = {}
        
    def msg(self, message):
        if self.verbose:
            print("Ngspice::", message, "\n")

    def addParameter(self, name, value):
        # Add parameter to circuit
        self.parameters.append( (name, value) )

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

    def clearControl(self):
        self.control = []

    def echo(self, toEcho : str) -> str:
        return 'echo "' + self.echoprefix + toEcho + '"'
    
    def measAtTime(self, name : str, expr : str, time ) -> str:
        return 'meas tran ' + name + ' FIND '+ expr + ' AT='+str(time)

    def makeMeasGroupV(self, names):
        # Make measurement group where name is the same as node name
        measGroup = []
        for name in names:
            measGroup.append( (name, 'v('+name+')') )
        return measGroup

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

    def addSets(self, setList):
        # Generate set commands from a list of set commands
        # setList is a list of tuples (name, value)
        res = ""
        for x in setList:
            name, val = x
            res += "\tset " + name + " = " + str(val) + "\n"
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
    
    def measGroupOP(self, groupName : str):
        group = self.measGroups[groupName]
        res = ""
        for meas in group:
            name, expr = meas
            res += " " + name + "=$&" + expr
        return self.echo(res)

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
        # Add subcircuit parameters to netlist
        for param in self.parameters:
            name, val = param
            res += ".param " + name + " " + str(val) + "\n"

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
        # Make an arbitrary signal source from several PULSE sources.
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
                    if (waveform[i] == 0) or (waveform[i] == '0') or (waveform[i] == False):
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

    def extractValues(self, names, results, missingVal = 1e9):
        # Extract values from measurement results
        # If results do not contain all names, missing values will be assigned the value missingVal
        outvals = []
        for step in results:
            expr = step.split()
            row = [missingVal for _ in range(len(names))]
            for vals in expr:
                if ('=' in vals):
                    name, val  = vals.split('=')
                    if name in names:
                        ind = names.index(name)
                        try:
                            row[ind] = float(val)
                        except:
                            row[ind] = val
            outvals.append(row)
        return outvals

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
    
    def dutFromNetlist(self, netlistFile, circuitName):
        # Read a DUT from a given netlistFile and circuitName and identify pins
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

        self.inputs = inputs
        self.outputs = outputs
        self.power = power
        self.ground = ground
        self.circuitTerminals = circuit.getTerminals()
    
    def combSim(self, toLogic=True):
        # Run ngspice simulations over all input vectors.
        # Returns a tuple (inputs, outputs)
        # If toLogic = False returns simulated voltages
        # If toLogic = True returns logic values

        self.clear()

        # Add DUT circuit instance
        self.addInstance("XDUT", self.circuitTerminals, self.circuitName, None)
        # Add ground -> 0 source for ground current measurement
        self.addInstance("VDUTGND", [self.ground, '0'], None, ['0'])

        # Add supply voltage
        vddVal = self.conditions['supplyVoltage']
        self.addInstance('VSUP', [self.power, '0'], None, [str(vddVal)])

        tsim, allVectors = self.genCombSources(self.inputs)

        tstep = self.conditions["tstepCombSim"]
        self.addControl("tran " + str(tstep) + " " + str(tsim))

        self.addMeasGroup("signals", self.makeMeasGroupV(self.inputs + self.outputs))

        td = self.conditions["td"]
        tclk = self.conditions["tclk"]
        t0 = td + 0.9 * tclk
        # Add measurements for each input combination
        for i in range(len(allVectors)):
            self.addControl(self.measGroupAtTime("signals", t0 + i * tclk, True))
        
        res = self.run()
        inputVals = self.extractValues(self.inputs, res)
        outputVals = self.extractValues(self.outputs, res)

        if not toLogic:
            return (self.inputs, inputVals, self.outputs, outputVals)
        else:
            vt = self.conditions['supplyVoltage']/2
            inputVals01 = [['1' if val > vt else '0' for val in row] for row in inputVals]
            outputVals01 = [['1' if val > vt else '0' for val in row] for row in outputVals]
            return (self.inputs, inputVals01, self.outputs, outputVals01)

    def combSimLeakagePower(self):
        # Simulate power leakage of combinatorial circuits for all input states
        
        self.clear()
        
        # Add DUT circuit instance
        self.addInstance("XDUT", self.circuitTerminals, self.circuitName, None)
        # Add ground -> 0 source for ground current measurement
        self.addInstance("VDUTGND", [self.ground, '0'], None, ['0'])

        inputSources = ['V'+x for x in self.inputs]

        # Add supply voltage
        vddVal = self.conditions['supplyVoltage']
        self.addInstance('VSUP', [self.power, '0'], None, [str(vddVal)])

        # Add input stimuli
        for name in self.inputs:
            self.addInstance('V'+name, [name, '0'], None, [0.0])

        mg = self.makeMeasGroupV(self.inputs + self.outputs)
        mg.append(('pleak', 'pleak'))
        self.addMeasGroup("signals", mg)
        
        nbits = len(self.inputs)
        allVectors = list(product([0.0, vddVal], repeat=nbits))

        self.addControl('set vdd='+str(vddVal))

        for vector in allVectors:
            ag = zip(inputSources, vector)
            self.addControl(self.alterGroup(ag))
            self.addControl("op")
            self.addControl("let pleak=-$vdd*i(VSUP)")
            self.addControl(self.measGroupOP("signals"))
        
        res = self.run()

        inputVals = self.extractValues(self.inputs, res)
        outputVals = self.extractValues(self.outputs, res)
        pleak = self.extractValues(['pleak'], res)
        # Flatten pleak results to one dimension
        pleak = [val for row in pleak for val in row]
        return (self.inputs, inputVals, self.outputs, outputVals, pleak)

    def combSimDelaySlewPowerCin(self, simSetup):
        # Simulate combinatorial circuit propagation delay and slew (rise/fall) time.
        # All but one input are at given constant values, and one input changes 0 -> 1 and 1 -> 0.
        # Measurements are performed for all combinations of given rise time and loading capacitance.
        # Only one output is considered at a time.
        # Simsetup is a dictionary that contains simulation setup
        # Key               Description
        # constantInputs    List of tuples (inputName, value) that are held at constant given values during simulations.
        #                   value is True for input held at VDD, or False for input held at 0.
        # input             Tuple (inputName, ["positive" | "negative"]). 
        #                   Values "positive" and "negative" define if input->output is positive or negative unate.
        # output            Name of output
        # capList           List of loading capacitance values.
        # slewList          List of slew times.
        # 
        # Optional arguments.
        #
        # input_threshold_pct_fall      Threshold for input signal falling edge, default 50.
        # input_threshold_pct_rise      Threshold for input signal rising edge, default 50.
        # output_threshold_pct_fall     Threshold for output signal falling edge, default 50.
        # output_threshold_pct_rise     Threshold for output signal rising edge, default 50
        # slew_lower_threshold_pct_fall Lower threshold for falling edge, default 20
        # slew_lower_threshold_pct_rise Lower threshold for rising edge, default 20
        # slew_upper_threshold_pct_fall High threshold for falling edge, default 80
        # slew_upper_threshold_pct_rise High threshold for rising edge, default 80
        # adjust_slew                   Adjust generator slew time so that given slew time is
        #                               between thresholds slew_*threshold_pct_*. Default True.
        #
        # Returns a list of results in a form of a tuple
        # (['rise', 'fall'], cout, slew, tp, ts, pint, cg )
        #

        self.clear()

        settings = {    "input_threshold_pct_fall"  :   50.0,
                        "input_threshold_pct_rise"  :   50.0,
                        "output_threshold_pct_fall" :   50.0,
                        "output_threshold_pct_rise" :   50.0,
                        "slew_lower_threshold_pct_fall" :   20.0,
                        "slew_lower_threshold_pct_rise" :   20.0,
                        "slew_upper_threshold_pct_fall" :   80.0,
                        "slew_upper_threshold_pct_rise" :   80.0,
                        "adjust_slew"                   :   False,
                        "tran_sim_step"                 :   10e-12,
                        "tran_sim_time"                 :   10e-9,
                        "tran_delay"                    :   1e-9
                    }

        settings.update( simSetup )

        # Add DUT circuit instance
        self.addInstance("XDUT", self.circuitTerminals, self.circuitName, None)
        # Add ground -> 0 source for ground current measurement
        self.addInstance("VDUTGND", [self.ground, '0'], None, ['0'])

        # Add voltage sources for constant inputs
        for cin in settings['constantInputs']:
            name, val = cin
            # Add constant input stimuli
            if val:
                vin = self.conditions['supplyVoltage']
            else:
                vin = 0.0
            self.addInstance('V'+name, [name, '0'], None, [str(vin)])
        
        # Add supply voltage
        vddVal = self.conditions['supplyVoltage']
        self.addInstance('VSUP', [self.power, '0'], None, [str(vddVal)])

        # Output load capacitor
        outNode = settings['output']
        self.addInstance("Cload", [outNode, '0'], None, ['1f'])

        inNode, unate = settings['input']

        # Add input stimulus
        spec = "pulse(0 1.2 1n 100p 100p 100n 1 1 )"
        self.addInstance("VIN", [inNode, '0'], None, [spec])

        tDelay = str(settings['tran_delay'])

        # Calculate threshold values
        itFall = float(vddVal) * settings["input_threshold_pct_fall"] / 100.0
        itRise = float(vddVal) * settings["input_threshold_pct_rise"] / 100.0
        otFall = float(vddVal) * settings["output_threshold_pct_fall"] / 100.0
        otRise = float(vddVal) * settings["output_threshold_pct_rise"] / 100.0
        slFall = float(vddVal) * settings["slew_lower_threshold_pct_fall"] / 100.0
        slRise = float(vddVal) * settings["slew_lower_threshold_pct_rise"] / 100.0
        suFall = float(vddVal) * settings["slew_upper_threshold_pct_fall"] / 100.0
        suRise = float(vddVal) * settings["slew_upper_threshold_pct_rise"] / 100.0

        if settings["adjust_slew"]:
            # Input rise time adjustment
            irAdj = 100.0 / (settings["slew_upper_threshold_pct_rise"] - settings["slew_lower_threshold_pct_rise"])
            # Input fall time adjustment
            ifAdj = 100.0 / (settings["slew_upper_threshold_pct_fall"] - settings["slew_lower_threshold_pct_fall"])
        else:
            # No input rise time adjustment
            irAdj = 1.0
            # No input fall time adjustment
            ifAdj = 1.0

        # Prepare commonly used commands
        if unate == 'positive':
            # Input rising -> output rising, input falling -> output falling
            # Delay on rising output
            mDelayRise = "meas tran tp_rise TRIG v(" + inNode + ") VAL="+str(itRise)+" RISE=1 TARG v(" + outNode + ") VAL=" + str(otRise) + " RISE=1"
            # Delay on falling output
            mDelayFall = "meas tran tp_fall TRIG v(" + inNode + ") VAL="+str(itFall)+" FALL=1 TARG v(" + outNode + ") VAL=" + str(otFall) + " FALL=1"
        elif unate == 'negative':
            # Input rising -> output falling, input falling -> output rising
            # Delay on rising output
            mDelayRise = "meas tran tp_rise TRIG v(" + inNode + ") VAL="+str(itFall)+" FALL=1 TARG v(" + outNode + ") VAL=" + str(otRise) + " RISE=1"
            # Delay on falling output
            mDelayFall = "meas tran tp_fall TRIG v(" + inNode + ") VAL="+str(itRise)+" RISE=1 TARG v(" + outNode + ") VAL=" + str(otFall) + " FALL=1"
        else:
            print("ERROR : Unate value must be either 'positive' or 'negative'")
            exit(1)

        # Output rise time
        mOutRise = "meas tran ts_rise TRIG v(" + outNode +") VAL=" + str(slRise) + " RISE=1 TARG v(" + outNode + ") VAL=" + str(suRise) + " RISE=1"
        # Output fall time
        mOutFall = "meas tran ts_fall TRIG v(" + outNode +") VAL=" + str(suFall) + " FALL=1 TARG v(" + outNode + ") VAL=" + str(slFall) + " FALL=1"

        # Internal power from VDD current
        expr_pVDD = "let pvdd = v(" + self.power + ") * i(vsup)"
        mVDD_pint = "meas tran pint INTEG pvdd FROM={} TO={}"
        # Internal power from VSS current
        expr_pVSS = "let pvss = -v(" + self.power + ") * i(vdutgnd)"
        mVSS_pint = "meas tran pint INTEG pvss FROM={} TO={}"

        # Gate charge falling input
        mQg = "meas tran qg INTEG i(vin) FROM={} TO={}"
        # Gage capacitance falling input
        expr_CgFall = "let cg = qg/{}"
        # Gate charge rising input
        expr_CgRise = "let cg = -qg/{}"

        tranCmd = "tran " + str(settings['tran_sim_step']) + ' ' + str(settings['tran_sim_time'])

        res_names = ['type', 'cout', 'slew', 'tp', 'ts', 'pint', 'cg']
        res_vals = []

        # Setup simulation
        coutList = settings['capList']
        slewList = settings['slewList']

        for cout in coutList:
            for slew in slewList:
                self.clearControl()
                self.addControl("alter Cload " + str(cout))
                rslew = irAdj * float(slew)
                fslew = ifAdj * float(slew)

                # Input rising
                vstart = str(0.0)
                vend = str(vddVal)
                self.addControl("alter @VIN[pulse]=[ " + vstart + " " + vend + " " + tDelay + " " + str(rslew) + " " + str(fslew) +" 1 1 ]")
                self.addControl(tranCmd)
                self.addControl(mQg.format(float(tDelay), float(tDelay)+float(rslew)))
                self.addControl(expr_CgRise.format(vddVal))
                if unate == 'positive':
                    # Output rising
                    self.addControl(mDelayRise)
                    self.addControl(mOutRise)
                    self.addControl(expr_pVSS)
                    self.addControl(mVSS_pint.format(float(tDelay), float(tDelay)+float(rslew)))
                    msg = "type=rise cout=" + str(cout) + " slew=" + str(slew) + " tp=$&tp_rise ts=$&ts_rise pint=$&pint cg=$&cg"
                else:
                    # Output falling
                    self.addControl(mDelayFall)
                    self.addControl(mOutFall)
                    self.addControl(expr_pVDD)
                    self.addControl(mVDD_pint.format(float(tDelay), float(tDelay)+float(rslew)))
                    msg = "type=fall cout=" + str(cout) + " slew=" + str(slew) + " tp=$&tp_fall ts=$&ts_fall pint=$&pint cg=$&cg"
                self.addControl(self.echo(msg))

                # Input falling
                vstart = str(vddVal)
                vend = str(0.0)
                self.addControl("alter @VIN[pulse]=[ " + vstart + " " + vend + " " + tDelay + " " + str(rslew) + " " + str(fslew) +" 1 1 ]")
                self.addControl(tranCmd)
                self.addControl(mQg.format(float(tDelay), float(tDelay)+float(fslew)))
                self.addControl(expr_CgFall.format(vddVal))
                if unate == 'negative':
                    # Output rising
                    self.addControl(mDelayRise)
                    self.addControl(mOutRise)
                    self.addControl(expr_pVSS)
                    self.addControl(mVSS_pint.format(float(tDelay), float(tDelay)+float(fslew)))
                    msg = "type=rise cout=" + str(cout) + " slew=" + str(slew) + " tp=$&tp_rise ts=$&ts_rise pint=$&pint cg=$&cg"
                else:
                    #Output falling
                    self.addControl(mDelayFall)
                    self.addControl(mOutFall)
                    self.addControl(expr_pVDD)
                    self.addControl(mVDD_pint.format(float(tDelay), float(tDelay)+float(fslew)))
                    msg = "type=fall cout=" + str(cout) + " slew=" + str(slew) + " tp=$&tp_fall ts=$&ts_fall pint=$&pint cg=$&cg"
                self.addControl(self.echo(msg))

                res = self.run()
            
                res_vals += self.extractValues(res_names, res)

        return (res_names, res_vals)

    def dffSetup(self, simSetup):
        # Simulate the D flip-flop setup time.
        # 
        # Simsetup is a dictionary that contains simulation setup
        # Key               Description
        # constantInputs    List of tuples (inputName, value) that are held at constant given values during simulations.
        #                   value is True for input held at VDD, or False for input held at 0.
        #                   Constant inputs should be set so that flip-flip operates normally, i.e. is not held in reset.
        # input             Tuple (inputName, ["positive" | "negative"]). 
        #                   Values "positive" and "negative" define if input->output is of  positive or negative polarity.
        # clk               Tuple (clkName, ["positive" | "negative"])
        # output            Name of the flip-flop output
        # dSlewList         List of input data slew times.
        # clkSlewList       List of clock slew times.

        # 
        # Optional arguments.
        #
        # max_tclkout_change            Setup violation occurs when t_clk_out > max_tclkout_change * t_clk_out_nom . Default 1.05.
        # cout                          Output loading capacitor. Default 1 fF.
        # input_threshold_pct_fall      Threshold for input signal falling edge, default 50.
        # input_threshold_pct_rise      Threshold for input signal rising edge, default 50.
        # output_threshold_pct_fall     Threshold for output signal falling edge, default 50.
        # output_threshold_pct_rise     Threshold for output signal rising edge, default 50
        # slew_lower_threshold_pct_fall Lower threshold for falling edge, default 20
        # slew_lower_threshold_pct_rise Lower threshold for rising edge, default 20
        # slew_upper_threshold_pct_fall High threshold for falling edge, default 80
        # slew_upper_threshold_pct_rise High threshold for rising edge, default 80
        # adjust_slew                   Adjust generator slew time so that given slew time is
        #                               between thresholds slew_*threshold_pct_*. Default True.
        # td_search                     Setup time search interval is td_search + dataSlew + clkSlew
        # Returns a list of results in a form of a tuple
        # [("dslew=data slew", "clkslew=clock slew", "t_setup=setup time", ... )
        #

        self.clear()

        settings = {    "max_tclkout_change"        :   1.05,
                        "cout"                      :   1e-15,
                        "input_threshold_pct_fall"  :   50.0,
                        "input_threshold_pct_rise"  :   50.0,
                        "output_threshold_pct_fall" :   50.0,
                        "output_threshold_pct_rise" :   50.0,
                        "slew_lower_threshold_pct_fall" :   20.0,
                        "slew_lower_threshold_pct_rise" :   20.0,
                        "slew_upper_threshold_pct_fall" :   80.0,
                        "slew_upper_threshold_pct_rise" :   80.0,
                        "adjust_slew"                   :   False,
                        "tran_sim_step"                 :   10e-12,
                        "tran_clk_pw"                   :   5e-9,
                        "tran_delay"                    :   1e-9,
                        "td_search"                     :   1e-9,
                        "td_tolerance"                  :   1e-12,
                        "max_iter"                      :   20,
                        "edge"                          :   "rising"
                    }

        settings.update( simSetup )

        # Add DUT circuit instance
        self.addInstance("XDUT", self.circuitTerminals, self.circuitName, None)
        # Add ground -> 0 source for ground current measurement
        self.addInstance("VDUTGND", [self.ground, '0'], None, ['0'])

        # Add voltage sources for constant inputs
        for cin in settings['constantInputs']:
            name, val = cin
            # Add constant input stimuli
            if val:
                vin = self.conditions['supplyVoltage']
            else:
                vin = 0.0
            self.addInstance('V'+name, [name, '0'], None, [str(vin)])
        
        # Add supply voltage
        vddVal = self.conditions['supplyVoltage']
        self.addInstance('VSUP', [self.power, '0'], None, [str(vddVal)])

        # Output load capacitor
        outNode = settings['output']
        self.addInstance("Cload", [outNode, '0'], None, [settings['cout']])

        if settings["adjust_slew"]:
            # Input rise time adjustment
            irAdj = 100.0 / (settings["slew_upper_threshold_pct_rise"] - settings["slew_lower_threshold_pct_rise"])
            # Input fall time adjustment
            ifAdj = 100.0 / (settings["slew_upper_threshold_pct_fall"] - settings["slew_lower_threshold_pct_fall"])
        else:
            # No input rise time adjustment
            irAdj = 1.0
            # No input fall time adjustment
            ifAdj = 1.0

        tran_delay = settings['tran_delay']
        tran_clk_pw = settings['tran_clk_pw']
        td_search = settings['td_search']

        edge = settings['edge']

        # Add default data pulse generator, parameters will be changed in the search loop
        inNode, inPolarity = settings['input']
        self.addInstance('VD', [ inNode, '0' ], None, ['pulse(0 1.2 9n 100p 100p 100n 1 )'])
        # Data polarity
        if edge not in ('rising', 'falling'):
            print("ERROR : setup edge must be 'rising' or 'falling'")
            exit(1)
        elif inPolarity not in ('positive', 'negative'):
            print("ERROR : data polarity property must be 'positive' or 'negative'")
            exit(1)
        else:
            # True if data and edge are of the same polarity
            edgeEquData = (edge == 'rising') == (inPolarity == 'positive')
            vd_start = 0.0 if edgeEquData else vddVal
            vd_end = vddVal if edgeEquData else 0.0

        # Add default clock pulse generator, parameters will be changed in the search loop
        clkNode, clkPolarity = settings['clk']
        self.addInstance('VCLK', [ clkNode, '0'], None, ['pulse(0 1.2 1n 200p 200p 5n 10n)'] )

        res_list = []
        # Loop goes here
        for dSlew in settings["dSlewList"]:
            for clkSlew in settings["clkSlewList"]:
                self.clearControl()

                # Data slew rate
                if vd_start < vddVal/2:
                    # Rising edge
                    dSlew_eff = dSlew * irAdj
                else:
                    # Falling edge
                    dSlew_eff = dSlew * ifAdj
                
                # Clock polarity
                if clkPolarity == 'positive':
                    clkSlew_eff = clkSlew * irAdj
                    vclk_zero = 0.0
                    vclk_one = vddVal
                else:
                    clkSlew_eff = clkSlew * ifAdj
                    vclk_zero = vddVal
                    vclk_one = 0.0

                td_window = td_search + dSlew_eff + clkSlew_eff
                td0 = 2*tran_clk_pw+2*clkSlew_eff+tran_delay+(clkSlew_eff-dSlew_eff)/2
                td_min = td0 - td_window
                td_max = td0 + td_window
                tran_out_start = 2*tran_clk_pw+2*clkSlew_eff+(clkSlew_eff-dSlew_eff)/2
                tran_sim_time = tran_delay + 2.5*tran_clk_pw + 2*clkSlew_eff

                tranCmd = "tran " + str(settings['tran_sim_step']) + ' ' + str(tran_sim_time) + ' ' + str(tran_out_start)

                setCmds = [ ("td0", td0), 
                            ("td_max", td_max), ("td_min", td_min), ("iter", 0), ("max_iter", settings["max_iter"]),
                            ("max_change", settings["max_tclkout_change"]), ("vd_start", vd_start), ("vd_end", vd_end),
                            ("vd_tr", dSlew_eff), ("vd_tf", dSlew_eff), ("vclk_tr", clkSlew_eff), ("vclk_tf", clkSlew_eff),
                            ("vclk_zero", vclk_zero), ("vclk_one", vclk_one), ("vclk_per", 2*tran_clk_pw+2*clkSlew_eff), ("vclk_pw", tran_clk_pw),
                            ("td_tolerance", settings["td_tolerance"]), ("tran_delay", tran_delay) ]
                self.addControl( self.addSets(setCmds) )
                
                self.addControl("let ltd_curr = $td0 - " + str(td_search))
                self.addControl("set td_curr = $&ltd_curr")
                
                self.addControl("alter @VD[pulse]=[ $vd_start $vd_end $td_curr $vd_tr $vd_tf 1 1 ]")

                self.addControl("alter @VCLK[pulse]=[ $vclk_zero $vclk_one $tran_delay $vclk_tr $vclk_tf $vclk_pw $vclk_per]")
                
                # Run baseline transient to measure nominal Clk->Q delay
                self.addControl(tranCmd)

                if inPolarity == "positive":
                    self.addControl("let vq_end = " + str(vd_end))
                else:
                    self.addControl("let vq_end = " + str(vddVal - vd_end))


                self.addControl('* Check if FF has captured the value')
                self.addControl('let vq_final = v(' + outNode + ')[length(v(' + outNode + '))-1]')
                self.addControl('print vq_final')
                self.addControl('if abs(vq_final - vq_end) ge ' + str(0.1 * vddVal))
                self.addControl('    echo "ERROR : Q was not captured during baseline run"')
                self.addControl('    quit 1')
                self.addControl('else')
                self.addControl('    echo "Q was captured during baseline run"')
                self.addControl('end')

                # Measure baseline clk->q delay
                meas = "meas tran nom_tclkq TRIG v(" + clkNode+ ") VAL=" + str(vddVal/2)
                if clkPolarity == "positive":
                    meas += " RISE=1 "
                else:
                    meas += " FALL=1 "
                meas += "TARG v(" + outNode + ") VAL="+ str(vddVal/2)
                if inPolarity == "positive":
                    if edge == "rising":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                else:
                    if edge == "rising":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                self.addControl(meas)
                # Store the raw text number safely across simulations
                self.addControl("set v_nom_tclkq = $&nom_tclkq")
                self.addControl('echo "Baseline Clock-to-Q delay is: $v_nom_tclkq"')

                self.addControl('set converged = 0')
                self.addControl('while $iter < $max_iter')
                self.addControl('    let tmp_delta = $td_max - $td_min')
                self.addControl('    if tmp_delta < $td_tolerance')
                self.addControl('        echo "Setup simulation has converged"')
                self.addControl('        set converged = 1')
                self.addControl('        break')
                self.addControl('    end')

                self.addControl('    let tmp_td = ($td_min + $td_max) / 2')
                self.addControl('    set td_current = $&tmp_td')
                    
                self.addControl('    let tmp_iter = $iter + 1')
                self.addControl('    set iter = $&tmp_iter')
                self.addControl('    echo "Iteration $iter, testing data delay td = $td_current"')

                self.addControl("alter @VD[pulse]=[ $vd_start $vd_end $td_current $vd_tr $vd_tf 1 1 ]")
                
                self.addControl(tranCmd)
                if inPolarity == "positive":
                    self.addControl("let vq_end = " + str(vd_end))
                else:
                    self.addControl("let vq_end = " + str(vddVal - vd_end))
                self.addControl("let vq_final = v(" + outNode + ")[length(v(" + outNode + "))-1]")

                self.addControl('    if abs(vq_final - vq_end) ge ' + str(0.1 * vddVal))
                self.addControl('        echo "Q was not captured"')
                self.addControl('        set td_max = $td_current')
                self.addControl('    else')
                self.addControl('        echo "Q was captured"')

                meas = "meas tran m_tclkq TRIG v(" + clkNode+ ") VAL=" + str(vddVal/2)
                if clkPolarity == "positive":
                    meas += " RISE=1 "
                else:
                    meas += " FALL=1 "
                meas += "TARG v(" + outNode + ") VAL="+ str(vddVal/2)
                if inPolarity == "positive":
                    if edge == "rising":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                else:
                    if edge == "rising":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                self.addControl(meas)
                # Convert current measurement to a local text variable
                self.addControl("set v_m_tclkq = $&m_tclkq")
                        
                # Calculate the maximum allowed degraded delay boundary
                self.addControl("let tmp_limit = $v_nom_tclkq * $max_change")
                self.addControl("set v_limit = $&tmp_limit")

                self.addControl('        if $v_limit > $v_m_tclkq')
                self.addControl('            echo "Setup is OK"')
                self.addControl('            set td_min = $td_current')
                self.addControl('        else')
                self.addControl('            echo "Setup is not OK (Clock-to-Q delay grew too large)"')
                self.addControl('            set td_max = $td_current')
                self.addControl('        end')
                self.addControl('    end')
                self.addControl('end')
                self.addControl('if $converged < 1')
                self.addControl('    echo "ERROR : Simulation has not converged!"')
                self.addControl('    quit 1')
                self.addControl('end')

                self.addControl("let tmp_td = ($td_min + $td_max) / 2")
                self.addControl("set td_current = $&tmp_td")
                self.addControl("alter @VD[pulse]=[ $vd_start $vd_end $td_current $vd_tr $vd_tf 1 1 ]")
                self.addControl(tranCmd)
                meas = "meas tran t_setup TRIG v(" + inNode+ ") VAL=" + str(vddVal/2)
                if inPolarity == "positive":
                    if edge == "rising":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                else:
                    if edge == "rising":
                        meas += " FALL=1 "
                    else:
                        meas += " RISE=1 "
                meas += "TARG v(" + clkNode + ") VAL="+ str(vddVal/2)
                if clkPolarity == "positive":
                    meas += " RISE=1 "
                else:
                    meas += " FALL=1 "
                self.addControl(meas)
                self.addControl(self.echo("t_setup=$&t_setup"))
                res = self.run()
                res_list.append( ("dslew="+str(dSlew), "clkslew="+str(clkSlew), res[0] ) )
        return res_list

    def dffHold(self, simSetup):
        # Simulate the D flip-flop hold time.
        # 
        # Simsetup is a dictionary that contains simulation setup
        # Key               Description
        # constantInputs    List of tuples (inputName, value) that are held at constant given values during simulations.
        #                   value is True for input held at VDD, or False for input held at 0.
        #                   Constant inputs should be set so that flip-flip operates normally, i.e. is not held in reset.
        # input             Tuple (inputName, ["positive" | "negative"]). 
        #                   Values "positive" and "negative" define if input->output is of positive or negative polarity.
        # clk               Tuple (clkName, ["positive" | "negative"])
        # output            Name of the flip-flop output
        # dSlewList         List of input data slew times.
        # clkSlewList       List of clock slew times.

        # 
        # Optional arguments.
        #
        # max_tclkout_change            Setup violation occurs when t_clk_out > max_tclkout_change * t_clk_out_nom . Default 1.05.
        # cout                          Output loading capacitor. Default 1 fF.
        # input_threshold_pct_fall      Threshold for input signal falling edge, default 50.
        # input_threshold_pct_rise      Threshold for input signal rising edge, default 50.
        # output_threshold_pct_fall     Threshold for output signal falling edge, default 50.
        # output_threshold_pct_rise     Threshold for output signal rising edge, default 50
        # slew_lower_threshold_pct_fall Lower threshold for falling edge, default 20
        # slew_lower_threshold_pct_rise Lower threshold for rising edge, default 20
        # slew_upper_threshold_pct_fall High threshold for falling edge, default 80
        # slew_upper_threshold_pct_rise High threshold for rising edge, default 80
        # adjust_slew                   Adjust generator slew time so that given slew time is
        #                               between thresholds slew_*threshold_pct_*. Default True.
        # td_search                     Setup time search interval is td_search + dataSlew + clkSlew
        # Returns a list of results in a form of a tuple
        # [("dslew=data slew", "clkslew=clock slew", "t_hold=hold time", ... )
        #

        self.clear()

        settings = {    "max_tclkout_change"        :   1.05,
                        "cout"                      :   1e-15,
                        "input_threshold_pct_fall"  :   50.0,
                        "input_threshold_pct_rise"  :   50.0,
                        "output_threshold_pct_fall" :   50.0,
                        "output_threshold_pct_rise" :   50.0,
                        "slew_lower_threshold_pct_fall" :   20.0,
                        "slew_lower_threshold_pct_rise" :   20.0,
                        "slew_upper_threshold_pct_fall" :   80.0,
                        "slew_upper_threshold_pct_rise" :   80.0,
                        "adjust_slew"                   :   False,
                        "tran_sim_step"                 :   10e-12,
                        "tran_clk_pw"                   :   5e-9,
                        "tran_delay"                    :   1e-9,
                        "td_search"                     :   1e-9,
                        "td_tolerance"                  :   1e-12,
                        "max_iter"                      :   20,
                        "edge"                          :   "rising"
                    }

        settings.update( simSetup )

        # Add DUT circuit instance
        self.addInstance("XDUT", self.circuitTerminals, self.circuitName, None)
        # Add ground -> 0 source for ground current measurement
        self.addInstance("VDUTGND", [self.ground, '0'], None, ['0'])

        # Add voltage sources for constant inputs
        for cin in settings['constantInputs']:
            name, val = cin
            # Add constant input stimuli
            if val:
                vin = self.conditions['supplyVoltage']
            else:
                vin = 0.0
            self.addInstance('V'+name, [name, '0'], None, [str(vin)])
        
        # Add supply voltage
        vddVal = self.conditions['supplyVoltage']
        self.addInstance('VSUP', [self.power, '0'], None, [str(vddVal)])

        # Output load capacitor
        outNode = settings['output']
        self.addInstance("Cload", [outNode, '0'], None, [settings['cout']])

        if settings["adjust_slew"]:
            # Input rise time adjustment
            irAdj = 100.0 / (settings["slew_upper_threshold_pct_rise"] - settings["slew_lower_threshold_pct_rise"])
            # Input fall time adjustment
            ifAdj = 100.0 / (settings["slew_upper_threshold_pct_fall"] - settings["slew_lower_threshold_pct_fall"])
        else:
            # No input rise time adjustment
            irAdj = 1.0
            # No input fall time adjustment
            ifAdj = 1.0

        tran_delay = settings['tran_delay']
        tran_clk_pw = settings['tran_clk_pw']

        td_search = settings['td_search']
        edge = settings['edge']

        # Add default data pulse generator, parameters will be changed in the search loop
        inNode, inPolarity = settings['input']
        self.addInstance('VD', [ inNode, '0' ], None, ['pulse(0 1.2 9n 100p 100p 100n 1 )'])
        # Data polarity
        if edge not in ('rising', 'falling'):
            print("ERROR : hold edge must be 'rising' or 'falling'")
            exit(1)
        elif inPolarity not in ('positive', 'negative'):
            print("ERROR : data polarity property must be 'positive' or 'negative'")
            exit(1)
        else:
            # For hold time measurement the reference edge is close to clock edge,
            # so the starting voltage is inverted compared to the setup case
            vd_start = 0.0 if edge == 'falling' else vddVal
            vd_end = vddVal if edge == 'falling' else 0.0

        # Add default clock pulse generator, parameters will be changed in the search loop
        clkNode, clkPolarity = settings['clk']
        self.addInstance('VCLK', [ clkNode, '0'], None, ['pulse(0 1.2 1n 200p 200p 5n 10n)'] )

        res_list = []

        for dSlew in settings["dSlewList"]:
            for clkSlew in settings["clkSlewList"]:
                self.clearControl()

                # Data slew rate
                if vd_start > vddVal/2:
                    # Rising edge
                    dSlew_eff = dSlew * irAdj
                else:
                    # Falling edge
                    dSlew_eff = dSlew * ifAdj
                
                # Clock polarity
                if clkPolarity == 'positive':
                    clkSlew_eff = clkSlew * irAdj
                    vclk_zero = 0.0
                    vclk_one = vddVal
                else:
                    clkSlew_eff = clkSlew * ifAdj
                    vclk_zero = vddVal
                    vclk_one = 0.0

                tc_pw = tran_clk_pw + dSlew_eff
                tc_per = 2*tc_pw + 2*clkSlew_eff
                td_del = tran_delay + tc_pw + clkSlew_eff - dSlew_eff/2 + clkSlew_eff/2
                td_pw = tc_pw - dSlew_eff + clkSlew_eff

                td_window = td_search + dSlew_eff + clkSlew_eff
                td_min = -td_window
                td_max = td_window
                tran_out_start = td_del
                tran_sim_time = tran_delay + 2.5*tc_pw + 2*clkSlew_eff

                tranCmd = "tran " + str(settings['tran_sim_step']) + ' ' + str(tran_sim_time) + ' ' + str(tran_out_start)

                setCmds = [ ("td_min", td_min), ("td_max", td_max), ("iter", 0), ("max_iter", settings["max_iter"]),
                            ("max_change", settings["max_tclkout_change"]), ("vd_start", vd_start), ("vd_end", vd_end),
                            ("vd_tr", dSlew_eff), ("vd_tf", dSlew_eff), ("vclk_tr", clkSlew_eff), ("vclk_tf", clkSlew_eff),
                            ("vclk_zero", vclk_zero), ("vclk_one", vclk_one), ("vclk_per", tc_per), ("vclk_pw", tc_pw),
                            ("td_tolerance", settings["td_tolerance"]), ("tran_delay", settings['tran_delay']), ("td_del", td_del), ("td_pw", td_pw) ]
                self.addControl( self.addSets(setCmds) )
                
                self.addControl("alter @VD[pulse]=[ $vd_start $vd_end $td_del $vd_tr $vd_tf 1 1 ]")
                self.addControl("alter @VCLK[pulse]=[ $vclk_zero $vclk_one $tran_delay $vclk_tr $vclk_tf $vclk_pw $vclk_per]")
                # Run baseline transient to measure nominal Clk->Q delay
                self.addControl(tranCmd)

                if inPolarity == "positive":
                    self.addControl("let vq_end = " + str(vd_end))
                else:
                    self.addControl("let vq_end = " + str(vddVal - vd_end))

                
                self.addControl("* Check if FF has captured the value")
                self.addControl('let vq_final = v(""" + outNode + """)[length(v(""" + outNode + """))-1]')
                self.addControl('print vq_final')
                self.addControl('if abs(vq_final - vq_end) ge ' + str(0.1 * vddVal))
                self.addControl('    echo "ERROR : Q was not captured during baseline run"')
                self.addControl('    quit 1')
                self.addControl('else')
                self.addControl('    echo "Q was captured during baseline run"')
                self.addControl('end')

                # Measure baseline clk->q delay
                meas = "meas tran nom_tclkq TRIG v(" + clkNode+ ") VAL=" + str(vddVal/2)
                if clkPolarity == "positive":
                    meas += " RISE=1 "
                else:
                    meas += " FALL=1 "
                meas += "TARG v(" + outNode + ") VAL="+ str(vddVal/2)
                if inPolarity == "positive":
                    if edge == "falling":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                else:
                    if edge == "rising":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                self.addControl(meas)
                # Store the raw text number safely across simulations
                self.addControl("set v_nom_tclkq = $&nom_tclkq")
                self.addControl('echo "Baseline Clock-to-Q delay is: $v_nom_tclkq"')

                self.addControl('set converged = 0')
                self.addControl('while $iter < $max_iter')
                self.addControl('    let tmp_delta = $td_max - $td_min')
                self.addControl('    if tmp_delta < $td_tolerance')
                self.addControl('        echo "Hold simulation has converged"')
                self.addControl('        set converged = 1')
                self.addControl('        break')
                self.addControl('    end')
                self.addControl('    let tmp_iter = $iter + 1')
                self.addControl('    set iter = $&tmp_iter')
                self.addControl('    let tpw_vector = $td_pw + ($td_min + $td_max) / 2')
                self.addControl('    set tpw = $&tpw_vector')
                self.addControl('    echo "Iteration $iter, testing data pulse width td_pw = $tpw"')

                self.addControl("alter @VD[pulse]=[ $vd_start $vd_end $td_del $vd_tr $vd_tf $tpw 1 ]")
                self.addControl(tranCmd)
                if inPolarity == "positive":
                    self.addControl("let vq_end = " + str(vd_end))
                else:
                    self.addControl("let vq_end = " + str(vddVal - vd_end))                
                self.addControl("let vq_final = v(" + outNode + ")[length(v(" + outNode + "))-1]")

                self.addControl('    if abs(vq_final - vq_end) ge ' + str(0.1 * vddVal))
                self.addControl('        echo "Q was not captured"')
                self.addControl('        let td_min_vec = $tpw - $td_pw')
                self.addControl('        set td_min = $&td_min_vec')
                self.addControl('    else')
                self.addControl('        echo "Q was captured"')

                meas = "meas tran m_tclkq TRIG v(" + clkNode+ ") VAL=" + str(vddVal/2)
                if clkPolarity == "positive":
                    meas += " RISE=1 "
                else:
                    meas += " FALL=1 "
                meas += "TARG v(" + outNode + ") VAL="+ str(vddVal/2)
                if inPolarity == "positive":
                    if edge == "falling":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                else:
                    if edge == "rising":
                        meas += " RISE=1 "
                    else:
                        meas += " FALL=1 "
                self.addControl(meas)
                # Convert current measurement to a local text variable
                self.addControl("set v_m_tclkq = $&m_tclkq")
                        
                # Calculate the maximum allowed degraded delay boundary
                self.addControl("let tmp_limit = $v_nom_tclkq * $max_change")
                self.addControl("set v_limit = $&tmp_limit")

                self.addControl('        if $v_limit > $v_m_tclkq')
                self.addControl('            echo "Hold is OK"')
                self.addControl('            let td_vec = $tpw - $td_pw')
                self.addControl('            set td_max = $&td_vec')
                self.addControl('        else')
                self.addControl('            echo "Hold is not OK (Clock-to-Q delay grew too large)"')
                self.addControl('            let td_vec = $tpw - $td_pw')
                self.addControl('            set td_min = $&td_vec')
                self.addControl('        end')
                self.addControl('    end')
                self.addControl('end')
                self.addControl('if $converged < 1')
                self.addControl('    echo "ERROR : Simulation has not converged!"')
                self.addControl('    quit 1')
                self.addControl('end')

                self.addControl('let tpw_vector = $td_pw + ($td_min + $td_max) / 2')
                self.addControl('set tpw = $&tpw_vector')
                
                self.addControl("alter @VD[pulse]=[ $vd_start $vd_end $td_del $vd_tr $vd_tf $tpw 1 ]")
                self.addControl(tranCmd)

                meas = "meas tran t_hold TRIG v(" + clkNode + ") VAL="+ str(vddVal/2)
                if clkPolarity == "positive":
                    meas += " RISE=1 "
                else:
                    meas += " FALL=1 "                                
                meas += "TARG v(" + inNode+ ") VAL=" + str(vddVal/2)
                if edge == "rising":
                    meas += " RISE=1 "
                else:
                    meas += " FALL=1 "

                self.addControl(meas)
                self.addControl(self.echo("t_hold=$&t_hold"))
                res = self.run()
                res_list.append( ("dslew="+str(dSlew), "clkslew="+str(clkSlew), res[0] ) )
        return res_list




    def dffClkToOut(self, simSetup):
        # Simulate the D flip-flop clock to output time.
        # 
        # Simsetup is a dictionary that contains simulation setup
        # Key               Description
        # constantInputs    List of tuples (inputName, value) that are held at constant given values during simulations.
        #                   value is True for input held at VDD, or False for input held at 0.
        #                   Constant inputs should be set so that flip-flip operates normally, i.e. is not held in reset.
        # input             Tuple (inputName, ["positive" | "negative"]). 
        #                   Values "positive" and "negative" define if input->output is of  positive or negative polarity.
        # clk               Tuple (clkName, ["positive" | "negative"])
        # output            Name of the flip-flop output
        # coutList          List of output loading capacitances.
        # clkSlewList       List of clock slew times.
        # edge              Output edge ['rising' | 'falling']

        # 
        # Optional arguments.
        #
        # input_threshold_pct_fall      Threshold for input signal falling edge, default 50.
        # input_threshold_pct_rise      Threshold for input signal rising edge, default 50.
        # output_threshold_pct_fall     Threshold for output signal falling edge, default 50.
        # output_threshold_pct_rise     Threshold for output signal rising edge, default 50
        # slew_lower_threshold_pct_fall Lower threshold for falling edge, default 20
        # slew_lower_threshold_pct_rise Lower threshold for rising edge, default 20
        # slew_upper_threshold_pct_fall High threshold for falling edge, default 80
        # slew_upper_threshold_pct_rise High threshold for rising edge, default 80
        # adjust_slew                   Adjust generator slew time so that given slew time is
        #                               between thresholds slew_*threshold_pct_*. Default True.
        # Returns a list of results in a form of a tuple
        # [("clkslew=clock slew", "cout=output capacitance", "t_clkout=clock->out time"), ... ]
        #

        self.clear()

        settings = {    "input_threshold_pct_fall"  :   50.0,
                        "input_threshold_pct_rise"  :   50.0,
                        "output_threshold_pct_fall" :   50.0,
                        "output_threshold_pct_rise" :   50.0,
                        "slew_lower_threshold_pct_fall" :   20.0,
                        "slew_lower_threshold_pct_rise" :   20.0,
                        "slew_upper_threshold_pct_fall" :   80.0,
                        "slew_upper_threshold_pct_rise" :   80.0,
                        "adjust_slew"                   :   False,
                        "dataSlew"                      :   100e-12,
                        "tran_sim_step"                 :   10e-12,
                        "tran_clk_pw"                   :   5e-9,
                        "tran_delay"                    :   1e-9,
                    }

        settings.update( simSetup )

        # Add DUT circuit instance
        self.addInstance("XDUT", self.circuitTerminals, self.circuitName, None)
        # Add ground -> 0 source for ground current measurement
        self.addInstance("VDUTGND", [self.ground, '0'], None, ['0'])

        # Add voltage sources for constant inputs
        for cin in settings['constantInputs']:
            name, val = cin
            # Add constant input stimuli
            if val:
                vin = self.conditions['supplyVoltage']
            else:
                vin = 0.0
            self.addInstance('V'+name, [name, '0'], None, [str(vin)])
        
        # Add supply voltage
        vddVal = self.conditions['supplyVoltage']
        self.addInstance('VSUP', [self.power, '0'], None, [str(vddVal)])

        # Output load capacitor of 1 fF, will be changed to specified values later
        outNode = settings['output']
        self.addInstance("Cload", [outNode, '0'], None, [1e-15])

        tran_delay = settings['tran_delay']
        tran_clk_pw = settings['tran_clk_pw']

        edge = settings['edge']

        # Add default data pulse generator, parameters will be changed in the search loop
        inNode, inPolarity = settings['input']
        self.addInstance('VD', [ inNode, '0' ], None, ['pulse(0 1.2 9n 100p 100p 100n 1 )'])
        # Data polarity
        if edge not in ('rising', 'falling'):
            print("ERROR : output edge must be 'rising' or 'falling'")
            exit(1)
        elif inPolarity not in ('positive', 'negative'):
            print("ERROR : data polarity property must be 'positive' or 'negative'")
            exit(1)
        else:
            # True if data and edge are of the same polarity
            edgeEquData = (edge == 'rising') == (inPolarity == 'positive')
            vd_start = 0.0 if edgeEquData else vddVal
            vd_end = vddVal if edgeEquData else 0.0

        # Add default clock pulse generator, parameters will be changed in the search loop
        clkNode, clkPolarity = settings['clk']
        self.addInstance('VCLK', [ clkNode, '0'], None, ['pulse(0 1.2 1n 200p 200p 5n 10n)'] )

        # Calculate threshold values
        itFall = float(vddVal) * settings["input_threshold_pct_fall"] / 100.0
        itRise = float(vddVal) * settings["input_threshold_pct_rise"] / 100.0
        otFall = float(vddVal) * settings["output_threshold_pct_fall"] / 100.0
        otRise = float(vddVal) * settings["output_threshold_pct_rise"] / 100.0
        slFall = float(vddVal) * settings["slew_lower_threshold_pct_fall"] / 100.0
        slRise = float(vddVal) * settings["slew_lower_threshold_pct_rise"] / 100.0
        suFall = float(vddVal) * settings["slew_upper_threshold_pct_fall"] / 100.0
        suRise = float(vddVal) * settings["slew_upper_threshold_pct_rise"] / 100.0

        if settings["adjust_slew"]:
            # Input rise time adjustment
            irAdj = 100.0 / (settings["slew_upper_threshold_pct_rise"] - settings["slew_lower_threshold_pct_rise"])
            # Input fall time adjustment
            ifAdj = 100.0 / (settings["slew_upper_threshold_pct_fall"] - settings["slew_lower_threshold_pct_fall"])
        else:
            # No input rise time adjustment
            irAdj = 1.0
            # No input fall time adjustment
            ifAdj = 1.0

        # Prepare commonly used commands
        if clkPolarity == 'positive':
            # Input rising -> output rising, input falling -> output falling
            # Delay on rising output
            mDelayRise = "meas tran tprop TRIG v(" + clkNode + ") VAL="+str(itRise)+" RISE=1 TARG v(" + outNode + ") VAL=" + str(otRise) + " RISE=1"
            # Delay on falling output
            mDelayFall = "meas tran tprop TRIG v(" + clkNode + ") VAL="+str(itRise)+" RISE=1 TARG v(" + outNode + ") VAL=" + str(otFall) + " FALL=1"
        elif clkPolarity == 'negative':
            # Input rising -> output falling, input falling -> output rising
            # Delay on rising output
            mDelayRise = "meas tran tprop TRIG v(" + clkNode + ") VAL="+str(itFall)+" FALL=1 TARG v(" + outNode + ") VAL=" + str(otRise) + " RISE=1"
            # Delay on falling output
            mDelayFall = "meas tran tprop TRIG v(" + clkNode + ") VAL="+str(itFall)+" FALL=1 TARG v(" + outNode + ") VAL=" + str(otFall) + " FALL=1"
        else:
            print("ERROR : clkPolarity value must be either 'positive' or 'negative'")
            exit(1)

        # Output rise time
        mOutRise = "meas tran tslew TRIG v(" + outNode +") VAL=" + str(slRise) + " RISE=1 TARG v(" + outNode + ") VAL=" + str(suRise) + " RISE=1"
        # Output fall time
        mOutFall = "meas tran tslew TRIG v(" + outNode +") VAL=" + str(suFall) + " FALL=1 TARG v(" + outNode + ") VAL=" + str(slFall) + " FALL=1"

        if edge == 'rising':
            mDelay = mDelayRise
            mSlew = mOutRise
        elif edge == 'falling':
            mDelay = mDelayFall
            mSlew = mOutFall
        else:
            print("ERROR : edge value must be either 'positive' or 'negative'")
            exit(1)

        res_names = ['cout', 'slew', 'tp', 'ts']
        res_vals = []
        for clkSlew in settings["clkSlewList"]:
            self.clearControl()

            # Data slew rate
            dSlew_eff = settings["dataSlew"]

            # Clock polarity
            if clkPolarity == 'positive':
                clkSlew_eff = clkSlew * irAdj
                vclk_zero = 0.0
                vclk_one = vddVal
            else:
                clkSlew_eff = clkSlew * ifAdj
                vclk_zero = vddVal
                vclk_one = 0.0

            tran_out_start = 2*tran_clk_pw+2*clkSlew_eff+(clkSlew_eff-dSlew_eff)/2
            tran_sim_time = tran_delay + 2.5*tran_clk_pw + 2*clkSlew_eff
            td_safe = tran_delay + clkSlew_eff + tran_clk_pw

            tranCmd = "tran " + str(settings['tran_sim_step']) + ' ' + str(tran_sim_time) + ' ' + str(tran_out_start)

            setCmds = [ ("tran_delay", tran_delay) ,
                        ("vd_start", vd_start), ("vd_end", vd_end),
                        ("vd_tr", dSlew_eff), ("vd_tf", dSlew_eff), ("vclk_tr", clkSlew_eff), ("vclk_tf", clkSlew_eff),
                        ("vclk_zero", vclk_zero), ("vclk_one", vclk_one), ("vclk_per", 2*tran_clk_pw+2*clkSlew_eff), ("vclk_pw", tran_clk_pw) ]
            self.addControl( self.addSets(setCmds) )
            
            self.addControl("set td_safe = " + str(td_safe))
            
            self.addControl("alter @VD[pulse]=[ $vd_start $vd_end $td_safe $vd_tr $vd_tf 1 1 ]")
            self.addControl("alter @VCLK[pulse]=[ $vclk_zero $vclk_one $tran_delay $vclk_tr $vclk_tf $vclk_pw $vclk_per]")

            for cout in settings['coutList']:
                # Change output capacitance
                self.addControl('alter Cload ' + str(cout))                            
                # Run transient to measure Clk->Q delay
                self.addControl(tranCmd)

                if inPolarity == "positive":
                    self.addControl("let vq_end = " + str(vd_end))
                else:
                    self.addControl("let vq_end = " + str(vddVal - vd_end))

                self.addControl('* Check if FF has captured the value')
                self.addControl('let vq_final = v(' + outNode + ')[length(v(' + outNode + '))-1]')
                self.addControl('print vq_final')
                self.addControl('if abs(vq_final - vq_end) ge ' + str(0.1 * vddVal))
                self.addControl('    echo "ERROR : Q was not captured"')
                self.addControl('    quit 1')
                self.addControl('else')
                self.addControl('    echo "Q was captured"')
                self.addControl('end')

                # Measure clk->q delay and slew
                self.addControl(mDelay)
                self.addControl(mSlew)
                msg = "cout=" + str(cout) + " slew=" + str(clkSlew) + " tp=$&tprop ts=$&tslew"
                self.addControl(self.echo(msg))

            res = self.run()
            res_vals += self.extractValues(res_names, res)
        return (res_names, res_vals)