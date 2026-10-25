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

netlistLicense = """
*
* Copyright Dr. Dušan Grujić (dusan.grujic@etf.bg.ac.rs)
* 
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* 
*    https://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
"""

import argparse
import os
from glow_utils.manifest import Manifest
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symsim import Symsim
import textwrap

defaultLibraryPath = "$GLOW_ROOT/library"
defaultNetlistFile = "glow_sg13g2"

def printusage():
    print("*"*80)
    print("")
    print("packnetlists collects individual CDL and SPICE netlists to a single file")
    print("")
    print("Usage :")
    print("packnetlists [options] manifest_file")
    print("")
    print("manifest_file is a YAML file containing information on cell groups and cells.")
    print("See the workflow/glow_utils documentation for manifest file structure.")
    print("Default library output directory can be changed by setting the")
    print("environment variable GLOW_LIBRARY.")
    print("Default netlist file name can be changed by setting the")
    print("environment variable GLOW_NETLIST_FILE.")
    print("Default values :")
    print("GLOW_LIBRARY =", defaultLibraryPath)
    print("GLOW_NETLIST_FILE =", defaultNetlistFile)
    print("")
    print("Options:")
    print("\t", "-c, --cell", "\t", "Generate a single cell.")
    print("\t", "-g, --group", "\t", "Generate a cell group.")
    print("\t", "-t, --type", "\t", "Generate all cells of a given type.")
    print("\t", "-a, --all", "\t", "Generate all cells.")
    print("\t", "--quiet", "\t", "Print only essential information.")
    print("*"*80)

def cells_from_manifest(manifest, cell_single, cell_group, cell_types, cell_all):
    """
    Generate a list of cells from manifest and list of single cells, cell_groups, cell_types, or all cells
    """
    cells = []
    if cell_all:
        # Return all cells
        groups = manifest.getCellGroups()
        for group in groups:
            cells += manifest.getCellGroupCells(group)
        return cells
    # Add individual cells
    cells += cell_single
    # Add cells from groups
    for group in cell_group:
        cells += manifest.getCellGroupCells(group)
    # Add cells by type
    for cell_type in cell_types:
        for group in manifest.getCellGroups(cell_type):
            cells += manifest.getCellGroupCells(group)
    return cells

#

def getFunction(manifest, cell):
    """
    Returns a string representation of a cell function
    """
    Symsubcircuit.importCell(cell)
    circuit = Symsubcircuit.getSubckts()[cell + "_flat"]
    sim = Symsim(circuit, verbose=False)

    if manifest.isCombinatorial(cell) or manifest.isConstant(cell):
        tbls = sim.reducedTruthTables()
        return sim.formatReducedTruthTables(tbls)
    elif manifest.isDFF(cell):
        group = manifest.findCellGroup(cell)
        spec = manifest.getCellGroupFnSpec(group)
        spec = {value: key for key, value in spec.items()}
        tbl = sim.dffTable(spec)
        # Replace up arrow with R to render correctly in monospace font
        return [sim.formatDffTable(tbl).replace("↑", "R")]
    elif manifest.isDLatch(cell):
        group = manifest.findCellGroup(cell)
        spec = manifest.getCellGroupFnSpec(group)
        spec = {value: key for key, value in spec.items()}
        tbl = sim.latchTable(spec)
        return [sim.formatDffTable(tbl)]
    else:
        return "No logic function"

#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    # Input file list
    parser.add_argument('-c', '--cell', action='append', default=[])
    parser.add_argument('-g', '--group', action='append', default=[])
    parser.add_argument('-t', '--type', action='append', default=[])
    parser.add_argument('-a', '--all',  action='store_true')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('input_file')

    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    # Check if user has set GLOW_LIBRARY or GLOW_NETLIST_FILE environment variables
    libraryPath = os.environ.get("GLOW_LIBRARY", default=defaultLibraryPath)
    netlistFile = os.environ.get("GLOW_NETLIST_FILE", default=defaultNetlistFile)

    quiet = True if args.quiet else False

    manifest_file = args.input_file

    if not quiet:
        print("*"*80)
        print("Reading manifest file :", manifest_file)
    manifest = Manifest(manifest_file)

    cells = cells_from_manifest(manifest, args.cell, args.group, args.type, args.all)
    # Eliminate duplicate entries
    cells = list(set(cells))
    cells.sort()

    if not quiet:
        print("Running packnetlists on cells :")
        print(" ".join(cells))

    error_cells = []

    cellCDL = []
    cellSPICE = []

    # Read-in cells
    for cell in cells:
        cell_dir = "./" + cell + "/"

        try:
            with open(cell_dir + cell + ".cdl", 'r') as f:
                cdl = f.read()
                cellCDL.append( (cell, cdl) )
            with open(cell_dir + cell + ".sp", 'r') as f:
                spice = f.read()
                cellSPICE.append( (cell, spice) )
        except:
            print("ERROR : ", cell)
            error_cells.append(cell)
    
    if len(error_cells) > 0:
        print("ERROR in cells : " + " ".join(error_cells))
        exit(1)

    print("Read in " + str(len(cells)) + " netlists")
    print("*"*80)
    # Write CDL netlist
    try:
        cdlFileName = libraryPath + "/cdl/" + netlistFile + ".cdl"
        print("Writing CDL netlists to", cdlFileName)
        cdlFileName = os.path.expandvars(cdlFileName)
        with open(cdlFileName, 'w') as f:
            f.write(netlistLicense)
            f.write("\n")
            for cell, cdl in cellCDL:
                print(cell, end=" ", flush=True)
                description = manifest.getCellDescription(cell)
                header = "*"*40  + "\n"
                header += "* Cell : " + cell + "\n"
                header += "* Description : " + description + "\n"
                fnStr = getFunction(manifest, cell)
                header += textwrap.indent("\n".join(fnStr), "* ") + "\n"
                header += "*"*40  + "\n"
                f.write(header)
                f.write(cdl)
                f.write("\n")
    except:
        print("ERROR : Could not write CDL output file.")
        exit(1)
    print("")
    print("*"*80)
    # Write SPICE netlist
    try:
        spiceFileName = libraryPath + "/spice/" + netlistFile + ".sp"
        print("Writing SPICE netlists to", spiceFileName)
        spiceFileName = os.path.expandvars(spiceFileName)
        with open(spiceFileName, 'w') as f:
            f.write(netlistLicense)
            f.write("\n")
            for cell, spice in cellSPICE:
                print(cell, end=" ", flush=True)
                description = manifest.getCellDescription(cell)
                header = "*"*40  + "\n"
                header += "* Cell : " + cell + "\n"
                header += "* Description : " + description + "\n"
                fnStr = getFunction(manifest, cell)
                header += textwrap.indent("\n".join(fnStr), "* ") + "\n"
                header += "*"*40  + "\n"
                f.write(header)
                f.write(spice)
                f.write("\n")
    except:
        print("ERROR : Could not write SPICE output file.")
        exit(1)
    print("")
    print("*"*80)
    print("ALL OK")
    exit(0)

if __name__ == "__main__":
    main()
