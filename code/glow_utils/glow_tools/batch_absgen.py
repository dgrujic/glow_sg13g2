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

def printusage():
    print("*"*80)
    print("")
    print("batch_absgen runs the absgen on a batch of cells ")
    print("")
    print("Usage :")
    print("batch_absgen -i file1 -i file2 ... [options]")
    print("Options:")
    print("--antenna    Prefix of antenna cells.")
    print("--spacer     Prefix of filler and decoupling cells.")
    print("")
    print("Input files contain list of cells to run in absgen.")
    print("Lines starting with # are considered as comments and ignored")
    print("Example of input file :")
    print("----------------------")
    print("# This is a comment")
    print("INV_D1")
    print("INV_D2")
    print("INV_D4")
    print("----------------------")
    print("This file runs absgen on cells INV_D1, INV_D2 and INV_D4")
    print("")
    print("To specify antenna and spacer cells")
    print("batch_absgen -i cell_list.txt --antenna ANTENNA --spacer FILL --spacer DCAP")
    print("This command treats cells named ANTENNA* as antenna cells, and FILL* and DCAP* as spacer cells.")
    print("*"*80)

def parse_string_names(str_arr):
    names = []
    for x in str_arr:
        if " " in x:
            tmp = x.split(" ")
            for name in tmp:
                names.append(name)
        else:
            names.append(x)
    return names

def read_input(file_name, cells):
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            if line[0] == "#":
                continue
            cells.append(line)

def is_prefix(cell_name, prefix_list):
    prefix_tuple = tuple(prefix_list)
    if cell_name.startswith(prefix_tuple):
        return True
    else:
        return False

#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    # Input file list
    parser.add_argument('-i', '--infile', action='append', default=[])
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--antenna', action='append', default=[])
    parser.add_argument('--spacer', action='append', default=[])
    
    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    quiet = True if args.quiet else False

    if (args.infile == []):
        printusage()
        exit(1)

    if not quiet:
        print("*"*80)
        print("Running batch absgen on cells :")

    antenna = args.antenna
    spacer = args.spacer

    input_files = parse_string_names(args.infile)
    cells = []
    for input_file in input_files:
        read_input(input_file, cells)

    if not quiet:
        print(" ".join(cells))

    error_cells = []

    glow_root = os.environ.get("GLOW_ROOT", default=None)
    if glow_root is None:
        glow_root = Path.cwd().parent
        if not quiet:
            print("WARNING : GLOW_ROOT is not set, using " + str(glow_root))

    for cell in cells:
        cell_dir = "./" + cell
        cmd = "absgen " + cell
        if is_prefix(cell, antenna):
            cmd += " --antenna"
        if is_prefix(cell, spacer):
            cmd += " --spacer"
        try:
            result = subprocess.run([cmd], cwd=cell_dir, env = os.environ | {'GLOW_ROOT' : glow_root}, shell=True)
            if result.returncode != 0:
                error_cells.append(cell)
        except:
            print("ERROR : ", cell)
            error_cells.append(cell)
    
    if len(error_cells) > 0:
        print("ERROR in [" +str(len(error_cells))+ "] cells : " + " ".join(error_cells))
        exit(1)
    else:
        if not quiet:
            print("ALL OK [" + str(len(cells)) + "]")
        exit(0)

if __name__ == "__main__":
    main()




