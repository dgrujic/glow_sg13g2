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
Netlist class is a basic SPICE netlist reader that can be used to read an extracted circuit netlist.
It provides methods to calculate gate and diffusion areas connected to a node, which is used when generating LEF abstracts.
"""

from glow_utils.symtech import SymTech
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS

import re
import random
import string

class Netlist:
    def __init__(self, fileName, verbose=True):
        """
        Read-in LVS (no parasitic) extracted SPICE netlist
        """
        self.verbose = {}
        self.subcircuits = {}
        self.readSPICE(fileName, self.verbose)

    @staticmethod
    def eng2sci(text):
        """
        Convert engineering prefix to scientific for number conversion
        """
        prefix_map = {
            'y': 'e-24', # yocto
            'z': 'e-21', # zepto
            'a': 'e-18', # atto
            'f': 'e-15', # femto
            'p': 'e-12', # pico
            'n': 'e-9',  # nano
            'u': 'e-6',  # micro
            'm': 'e-3',  # milli
            'c': 'e-2',  # centi
            'd': 'e-1',  # deci
            'k': 'e3',   # kilo
            'M': 'e6',   # Mega
            'G': 'e9',   # Giga
            'T': 'e12',  # Tera
            'P': 'e15',  # Peta
            'E': 'e18',  # Exa
            'Z': 'e21',  # Zetta
            'Y': 'e24'   # Yotta
        }

        # Regex to capture a number followed immediately by one of the engineering prefixes
        pattern = rf'(-?\d*\.?\d+)([{re.escape("".join(prefix_map.keys()))}])'

        def replace_func(match):
            number, prefix = match.groups()
            # Combine the number with the scientific exponent and clean up trailing zeroes
            val = float(f"{number}{prefix_map[prefix]}")
            return f"{val:e}".rstrip('0').rstrip('.') if 'e' in f"{val:e}" else f"{val:e}"

        # Substitute matches in the text
        return re.sub(pattern, replace_func, text)

    def readSPICE(self, fileName : str, verbose=True):
        """
        Basic SPICE netlist reader to input extracted netlists
        Only transistors are supported
        """
        subcircuit = {}
        devices = None
        device = None
        with open(fileName, 'r') as file:
            for line in file:
                line = line.strip()
                if (line == ""):
                    # Empty line, skip
                    continue
                elif (line[0] == '*'):
                    # Comment, skip
                    continue
                elif (line[0]) == '+':
                    # Line continuation, continue adding parameters to the current device
                    if device is not None:
                        tmp = line[1:].strip().split()
                        for i in range(len(tmp)):
                            name, val = tmp[i].split('=')
                            val = self.eng2sci(val)
                            device.update( {name : val} )
                elif (line[0] == 'M'):
                    # MOSFET, create new device and add it
                    if device is not None:
                        # Save previous device
                        devices.update( {device['name'] : device} )
                    device = {}
                    tmp = line.split()
                    device.update( {'name' : tmp[0]})
                    nodes = [tmp[1], tmp[2], tmp[3], tmp[4]]
                    device.update( {'nodes' : nodes} )
                    device.update( {'model' : tmp[5]} )
                    for i in range(6, len(tmp)):
                        name, val = tmp[i].split('=')
                        val = self.eng2sci(val)
                        device.update( {name : val} )
                elif (".SUBCKT" in line):
                    # Subcircuit
                    tmp = line.split()
                    if subcircuit != {}:
                        self.subcircuits.update( { subcircuit['__name__'] : subcircuit } )
                        subcircuit = {}
                    subcircuit.update({ 'name' : tmp[1] })
                    devices = {}
                    subcircuit.update({'devices' : devices})
                    nodes = []
                    for i in range(2, len(tmp)):
                        if '=' not in tmp[i]:
                            # This is a node name
                            nodes.append(tmp[i])
                    subcircuit.update( {'nodes' : nodes} )
                elif (".ENDS" in line):
                    if device is not None:
                        # Save previous device
                        devices.update( {device['name'] : device} )
                    if subcircuit != {}:
                        self.subcircuits.update( { subcircuit['name'] : subcircuit } )
                else:
                    # Unknown line, skip and issue warning
                    if verbose:
                        print("Netlist::WARNING : Skipping line\n","\t", line)

        if device is not None:
            # Save previous device
            devices.update( {device['name'] : device} )
        if subcircuit != {}:
            self.subcircuits.update( { subcircuit['name'] : subcircuit } )

    def getSubcircuitNames(self):
        return list(self.subcircuits.keys())

    def getSubcircuit(self, name):
        if name in self.subcircuits.keys():
            return self.subcircuits[name]
        else:
            return None

    def calcGateArea(self, circuitName, node):
        """
        Calculate the gate area connected to a given node name
        """
        circuit = self.subcircuits[circuitName]
        if circuit is None:
            if self.verbose:
                print("Netlist::WARNING : Circuit", circuitName, "not found, returning 0.")
                return 0
        devices = circuit['devices']
        deviceNames = list( devices.keys() )
        area = 0.0
        for name in deviceNames:
            device = devices[name]
            nodes = device['nodes']
            if nodes[1] == node:
                # Device gate is connected to a given node
                l = float(device['L'])
                w = float(device['W'])
                area += w * l
        strarea = "{:.4g}".format(area)
        return float(strarea)

    def calcDiffArea(self, circuitName, node):
        """
        Calculate the diffusion area connected to a given node name
        """
        circuit = self.subcircuits[circuitName]
        if circuit is None:
            if self.verbose:
                print("Netlist::WARNING : Circuit", circuitName, "not found, returning 0.")
                return 0
        devices = circuit['devices']
        deviceNames = list( devices.keys() )
        area = 0.0
        for name in deviceNames:
            device = devices[name]
            nodes = device['nodes']
            if nodes[0] == node:
                # Device drain is connected to a given node
                area += float(device['AD'])
            elif nodes[2] == node:
                # Device source is connected to a given node
                area += float(device['AS'])
        strarea = "{:.4g}".format(area)
        return float(strarea)

    def makeCircuit(self, circuitName):
        subcircuit = self.getSubcircuit(circuitName)
        if subcircuit is None:
            print("Subcircuit " + circuitName + " does not exist")
            return None
        nmos = SymTech.nmosModelName
        pmos = SymTech.pmosModelName
        # Make a random name for temproary circuit
        length = 8
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        terminals = subcircuit['nodes']
        circuit = Symsubcircuit(name, terminals)
        for elementName in list(subcircuit['devices'].keys()):
            element = subcircuit['devices'][elementName]
            w = element['W']
            l = element['L']
            areaS = element['AS']
            areaD = element['AD']
            periS = element['PS']
            periD = element['PD']
            name = element['name']
            nodes = element['nodes']
            model = element['model']
            if model == nmos:
                mos = SymNMOS(name, nodes, {'w' : w, 'l' : l, 'as' : areaS, 'ad' : areaD, 'ps' : periS, 'pd' : periD})
            elif model == pmos:
                mos = SymPMOS(name, nodes, {'w' : w, 'l' : l, 'as' : areaS, 'ad' : areaD, 'ps' : periS, 'pd' : periD})
            else:
                if self.verbose:
                    print("Netlist::WARNING : Model", model, "is unknown, skipping.")
                mos = None
            if mos is not None:
                circuit.addElement( mos )
        return circuit



