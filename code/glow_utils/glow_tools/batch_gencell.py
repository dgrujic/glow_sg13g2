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

def printusage():
    print("*"*80)
    print("")
    print("batch_gencell runs the gencell on a batch of cells ")
    print("")
    print("Usage :")
    print("batch_gencell -i file1 -i file2 ...")
    print("")
    print("Input files contain list of cells to run in gencell.")
    print("Lines starting with # are considered as comments and ignored")
    print("Example of input file :")
    print("----------------------")
    print("# This is a comment")
    print("INV_D1")
    print("INV_D2")
    print("INV_D4")
    print("----------------------")
    print("This file runs gencell on cells INV_D1, INV_D2 and INV_D4")
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
#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    # Input file list
    parser.add_argument('-i', '--infile', action='append', default=[])
    parser.add_argument('--quiet', action='store_true')

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
        print("Running batch gencell on cells :")

    input_files = parse_string_names(args.infile)
    cells = []
    for input_file in input_files:
        read_input(input_file, cells)

    if not quiet:
        print(" ".join(cells))

    error_cells = []

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
    
    if len(error_cells) > 0:
        print("ERROR in cells : " + " ".join(error_cells))
        exit(1)
    else:
        if not quiet:
            print("ALL OK [" + str(len(cells)) + "]")
        exit(0)

if __name__ == "__main__":
    main()




