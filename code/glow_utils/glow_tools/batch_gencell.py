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
from glow_utils.manifest import Manifest

def printusage():
    print("*"*80)
    print("")
    print("batch_gencell runs the gencell on a batch of cells ")
    print("")
    print("Usage :")
    print("batch_gencell [options] manifest_file")
    print("")
    print("manifest_file is a YAML file containing information on cell groups and cells.")
    print("See the workflow/glow_utils documentation for manifest file structure.")
    print("Options:")
    print("\t", "-c, --cell", "\t", "Generate a single cell.")
    print("\t", "-g, --group", "\t", "Generate a cell group.")
    print("\t", "-t, --type", "\t", "Generate all cells of a given type.")
    print("\t", "-a, --all", "\t", "Generate all cells.")
    print("\t", "-p, --parallel", "\t", "Run jobs in parallel.")
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

def run_command(cmd):
    cell = cmd[1]
    result = subprocess.run(cmd, cwd="./"+cell, capture_output=True, text=True)
    return result, cell

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
    parser.add_argument('-p', '--parallel', type=int, default=1)
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('input_file')

    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    quiet = True if args.quiet else False

    manifest_file = args.input_file

    if args.parallel == 1:
        parallel = False
        nParallel = 1
    else:
        parallel = True
        if (args.parallel < 1) or (args.parallel > 256):
            nParallel = os.cpu_count()
        else:
            nParallel = args.parallel

    if not quiet:
        print("*"*80)
        print("Reading manifest file :", manifest_file)
    manifest = Manifest(manifest_file)

    cells = cells_from_manifest(manifest, args.cell, args.group, args.type, args.all)
    # Eliminate duplicate entries
    cells = list(set(cells))
    cells.sort()

    if not quiet:
        print("Running batch gencell on cells :")
        print(" ".join(cells))

    error_cells = []

    if not parallel:
        # Sequential run
        for cell in cells:
            cell_dir = "./" + cell
            cmd = ["gencell", cell]
            if quiet:
                cmd.append("--quiet")
            try:
                result = subprocess.run(cmd, cwd=cell_dir)
                if result.returncode != 0:
                    error_cells.append(cell)
            except:
                print("ERROR : ", cell)
                error_cells.append(cell)
    else:
        # Parallel run
        from concurrent.futures import ThreadPoolExecutor, as_completed
        if not quiet:
            print("Starting parallel execution with", nParallel, "processes...")

        # Make a list of commands
        cmdList = []
        for cell in cells:
            if quiet:
                cmdList.append( ["gencell", cell, "--quiet"] )
            else:
                cmdList.append( ["gencell", cell] )

        with ThreadPoolExecutor(max_workers=nParallel) as runner:
            jobs = {runner.submit(run_command, cmd): cmd for cmd in cmdList}
            for job in as_completed(jobs):
                result, cell = job.result()
                print(result.stdout.strip())
                if result.returncode != 0:
                    error_cells.append(cell)
    
    if len(error_cells) > 0:
        print("ERROR in cells : " + " ".join(error_cells))
        exit(1)
    else:
        print("ALL OK [" + str(len(cells)) + "]")
        exit(0)

if __name__ == "__main__":
    main()

