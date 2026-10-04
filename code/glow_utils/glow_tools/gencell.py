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

from glow_utils.symsubcircuit import Symsubcircuit

import argparse
from pathlib import Path

import importlib
import os
import sys

def printlogo():
    print("\t",r"                           _ _ ")
    print("\t",r"  __ _  ___ _ __   ___ ___| | |")
    print("\t",r" / _` |/ _ \ '_ \ / __/ _ \ | |")
    print("\t",r"| (_| |  __/ | | | (_|  __/ | |")
    print("\t",r" \__, |\___|_| |_|\___\___|_|_|")
    print("\t",r" |___/                         ")

def printusage():
    print("*"*80)
    printlogo()
    print("")
    print("gencell is an utility to generate cells from Python code")
    print("Usage:")
    print("gencell cell_name [options]")
    print("Options:")
    print("--quiet          Print only essential info.")
    print("--nospice        Don't write SPICE netlist.")
    print("--nocdl          Don't write CDL netlist.")
    print("--noflat         Don't flatten SPICE netlist.")
    print("*"*80)

def file_exists(file_name):
    if Path(file_name).is_file():
        return True
    return False

def writeNetlist(cell_module, flat = True, SPICE = True, CDL = True, verbose = False):
    """
    Write the circuit netlist
    """
    cellInfo = cell_module.info()
    name = cellInfo["name"]
    allCircuits = Symsubcircuit.getSubckts()
    circuit_flat = allCircuits[ name + "_flat" ]
    circuit_hier = allCircuits[ name ]
    if SPICE:
        if flat:
            circuit_flat.write_SPICE(name, printOutput = verbose)
        else:
            circuit_hier.write_SPICE(name, printOutput = verbose)
    if CDL:
        circuit_flat.write_CDL(name, printOutput = verbose)

#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cell_name')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--nospice', action='store_true')
    parser.add_argument('--nocdl', action='store_true')
    parser.add_argument('--noflat', action='store_true')
    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    quiet = True if args.quiet else False
    nospice = True if args.nospice else False
    nocdl = True if args.nocdl else False
    noflat = True if args.noflat else False

    if not quiet:
        print("*"*80)
        printlogo()
        print("")

    cell_name = args.cell_name
    if not quiet:
        print("Generating cell",cell_name)
    else:
        print("GENCELL",cell_name.ljust(10), "\t",end="")


    if not file_exists(cell_name + ".py"):
        print("ERROR : File", cell_name+".py", "does not exist.")
        exit(1)

    # Dynamically load the cell
    sys.path.insert(0, os.getcwd())
    cell_module = importlib.import_module(cell_name)

    try:
        info = cell_module.info()
        if not quiet:
            print("Cell info :")
            print("\tName        :", info['name'])
            print("\tTerminals   :", info['pinList'])
            print("\tDescription :", info['description'])
    except:
        print("ERROR : Unable to access cell", cell_name," info.")
        exit(1)

    try:
        cell_module.generate()
        if not quiet:
            print("INFO : Generated cell ", cell_name)
    except:
        print("ERROR : Unable to generate cell", cell_name)
        exit(1)
    
    try:
        res = cell_module.check(verbose=not(quiet))
        if res:
            if not quiet:
                print("INFO : Checks passed on cell", cell_name)
        else:
            print("ERROR : Checks failed on cell", cell_name)
            exit(1)
    except:
        print("ERROR : Unable to perform checks on cell", cell_name)
        exit(1)

    try:
        writeNetlist(cell_module, flat=not(noflat), SPICE=not(nospice), CDL=not(nocdl), verbose=not(quiet))
        if not nospice and not quiet:
            if noflat:
                print("INFO : Writing hierarchical SPICE netlist", cell_name + ".sp")
            else:
                print("INFO : Writing flat SPICE netlist", cell_name + ".sp")
        if not nocdl and not quiet:
            print("INFO : Writing CLD netlist", cell_name + ".cdl")
    except:
        print("ERROR : Unable to write netlist", cell_name)
        exit(1)

    if not quiet:
        print("All OK")
    else:
        print("OK")

    if not quiet:
        print("*"*80)


if __name__ == "__main__":
    main()
