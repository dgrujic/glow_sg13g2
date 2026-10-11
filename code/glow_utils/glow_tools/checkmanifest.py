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

import argparse
import subprocess
import os
from pathlib import Path
from glow_utils.manifest import Manifest
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symsim import Symsim

def printusage():
    print("*"*80)
    print("")
    print("checkmanifest performs checks on a given manifest")
    print("")
    print("Checks performed:")
    print("\t- Check if a cell directory and Python code exists")
    print("\t- Check if a cell can be generated without errors")
    print("\t- Check if cell pins from manifest and cell info match")
    print("\t- Check if a cell's check() function returns True")
    print("\t- Check if running Symsim check passes with data from manifest in strict mode")
    print("")
    print("Usage :")
    print("checkmanifest [options] manifest_file")
    print("")
    print("manifest_file is a YAML file containing information on cell groups and cells.")
    print("See the workflow/glow_utils documentation for manifest file structure.")
    print("Options:")
    print("\t", "-c, --cell", "\t", "Check a single cell.")
    print("\t", "-g, --group", "\t", "Check a cell group.")
    print("\t", "-t, --type", "\t", "Check all cells of a given type.")
    print("\t", "-a, --all", "\t", "Check all cells.")
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

def check_cell(manifest, name, quiet):
    """
    Run a check on cell by using manifest specification
    """
    allCircuits = Symsubcircuit.getSubckts()
    circuit = allCircuits[ name + "_flat" ]
    
    if manifest.isCombinatorial(name):
        sim = Symsim(circuit, verbose = not(quiet))
        expectedFns = list(manifest.getCellFnSpec(name).values())
        return sim.combCheck(expectedFns, strict=True)
    elif manifest.isDFF(name):
        sim = Symsim(circuit, verbose = not(quiet))
        spec = manifest.getCellFnSpec(name)
        specPins = set(spec.keys())
        manifestPins = set(manifest.getCellPins(name))
        if not specPins.issubset(manifestPins):
            print("ERROR : Specification has extra pin[s] : ", specPins.difference(manifestPins))
            return False
        # Swap key/values
        spec = {value: key for key, value in spec.items()}
        return sim.dffCheck(spec)
    elif manifest.isDLatch(name):
        sim = Symsim(circuit, verbose = not(quiet))
        spec = manifest.getCellFnSpec(name)
        specPins = set(spec.keys())
        manifestPins = set(manifest.getCellPins(name))
        if not specPins.issubset(manifestPins):
            print("ERROR : Specification has extra pin[s] : ", specPins.difference(manifestPins))
            return False
        # Swap key/values
        spec = {value: key for key, value in spec.items()}
        return sim.latchCheck(spec)
    elif manifest.isConstant(name):
        sim = Symsim(circuit, verbose = not(quiet))
        expectedFns = list(manifest.getCellFnSpec(name).values())
        return sim.combCheck(expectedFns, strict=True)
    else:
        return True

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
        print("Running checks on cells :")
        print(" ".join(cells))

    error_cells = []

    glow_root = os.environ.get("GLOW_ROOT", default=None)
    if glow_root is None:
        glow_root = Path.cwd().parent
        if not quiet:
            print("WARNING : GLOW_ROOT is not set, using " + str(glow_root))

    for cell in cells:
        cellType = manifest.getCellType(cell)
        cell_dir = "./" + cell

        if not quiet:
            print("*" * 80)
            print("Checking cell", cell)
        else:
            print(cell, end="")

        # Check if cell Python code exists
        if not Symsubcircuit.cellExists(cell, view='python'):
            # Cell does not exist
            error_cells.append(cell)
            print("\tERROR : Python code does not exist.")
            continue
        else:
            try:
                Symsubcircuit.importCell(cell)
                if not quiet:
                    print("Succesfully imported and generated Python code.")
                else:
                    print("\tPython OK", end="")
            except:
                print("\tERROR : Failed to generate cell.")
                error_cells.append(cell)
                continue

        cellCls = None
        # Check if pins match
        try:
            cellCls = Symsubcircuit.getSubckts()[cell]
            # Get a set of cell pins
            cellPins = set(cellCls.getTerminals())
            # Get a set of cell pins from manifest
            manifestPins = set(manifest.getCellPins(cell))
            if cellPins == manifestPins:
                if not quiet:
                    print("Cell and manifest pins match.")
                else:
                    print("\tPINS OK", end="")
            else:
                print("\tERROR : Pins in cell and manifest do not match.")
                error_cells.append(cell)
                continue
        except:
            print("\tERROR : Failed to get cell subcircuit class.")
            error_cells.append(cell)
            continue

        # Check if subcircuit check function passes
        if cellCls.subCktCheck(not(quiet)):
            if not quiet:
                print("Cell check function OK")
            else:
                print("\tCELL_CHECK OK", end="")
        else:
            if not quiet:
                print("ERROR : Cell check function filed.")
            else:
                print("\tCELL_CHECK ERROR", end="")
            error_cells.append(cell)
            continue
           
        # Check manifest specification
        try:
            if check_cell(manifest, cell, quiet):
                if not quiet:
                    print("Cell check function from manifest specification OK")
                else:
                    print("\tCELL_CHECK_MANIFEST OK")
            else:
                if not quiet:
                    print("ERROR : Cell check function from manifest specification failed.")
                else:
                    print("\tCELL_CHECK_MANIFEST ERROR")                
                error_cells.append(cell)
                continue
        except:
            print("\tERROR : Failed to check cell from manifest specification.")
            error_cells.append(cell)
            continue
    
    if len(error_cells) > 0:
        print("ERROR in [" +str(len(error_cells))+ "] cells : " + " ".join(error_cells))
        exit(1)
    else:
        if not quiet:
            print("ALL OK [" + str(len(cells)) + "]")
        exit(0)

if __name__ == "__main__":
    main()

