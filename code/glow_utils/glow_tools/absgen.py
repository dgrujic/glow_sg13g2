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

from glow_utils.netlist import Netlist
from glow_utils.symcheck import Symcheck
from glow_utils.symtech import SymTech
from glow_utils.lef import *

import gdstk
import argparse
from pathlib import Path
import subprocess

def printlogo():
    print("\t",r"        _                          ")
    print("\t",r"   __ _| |__  ___  __ _  ___ _ __  ")
    print("\t",r"  / _` | '_ \/ __|/ _` |/ _ \ '_ \ ")
    print("\t",r" | (_| | |_) \__ \ (_| |  __/ | | |")
    print("\t",r"  \__,_|_.__/|___/\__, |\___|_| |_|")
    print("\t",r"                  |___/            ")

def printusage():
    print("*"*80)
    printlogo()
    print("")
    print("absgen is an utility to generate LEF abstracts")
    print("Usage:")
    print("absgen cell_name [options]")
    print("Options:")
    print("--quiet          Print only essential info.")
    print("--keep_polygons  Don't convert polygons to rectangles")
    print("*"*80)

def dir_exists(dir_name):
    if Path(dir_name).is_dir():
        return True
    return False

def file_exists(file_name):
    if Path(file_name).is_file():
        return True
    return False

def cellSize(cell : gdstk.Cell, prBoundary):
    bb = None
    for poly in cell.polygons:
        if poly.layer == prBoundary:
            bb = poly.bounding_box()
    if bb is None:
        return None
    else:
        lr, tr = bb
        if lr != (0,0):
            print("WARNING : prBoundary origin is at ", lr)
        dx = tr[0] - lr[0]
        dy = tr[1] - lr[1]
    return (dx, dy)

def find_cell(name, lib):
    """
    Find a cell with given name in a list of given libraries.
    First occurence of a cell is returned, or None if not found.
    """
    for cell in lib.cells:
        if cell.name == name:
            return cell
    return None

#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cell_name')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--keep_polygons', action='store_true')
    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    usePolygons = True if args.keep_polygons else False
    quiet = True if args.quiet else False

    if not quiet:
        print("*"*80)
        printlogo()
        print("")

    cell_name = args.cell_name
    if not quiet:
        print("Generating abstract view for cell",cell_name)
    else:
        print("ABSGEN",cell_name, "\t",end="")

    if not quiet:
        if usePolygons:
            print("INFO : Using polygons in LEF abstract")
        else:
            print("INFO : Converting polygons to rectangles in LEF abstract")

    gds_name = cell_name + ".gds"
    extracted_name = cell_name + "_extracted.cir"
    if file_exists( gds_name ):
        if not quiet:
            print("Using GDSII file " + gds_name )
    else:
        print("ERROR : GDSII file " + gds_name + " not found!")
        exit(1)

    # Check if extracted netlist already exists, and generate it if not
    if dir_exists("lvs") and file_exists( "lvs/" + extracted_name ):
        if not quiet:
            print("Using extracted netlist lvs/" + extracted_name)
    else:
        if not quiet:
            print("Extracted netlist not found, running check_cell...")
            res = subprocess.run(["$GLOW_ROOT/code/scripts/check_cell.sh " + gds_name + " " + cell_name], shell=True)
        else:
            res = subprocess.run(["$GLOW_ROOT/code/scripts/check_cell.sh " + gds_name + " " + cell_name + " > /dev/null"], shell=True)
        if res.returncode != 0:
            print("Cell checking failed, please run check_cell.sh to debug the issue")
            exit(1)
        if dir_exists("lvs") and file_exists( "lvs/" + extracted_name ):
            if not quiet:
                print("Using extracted netlist lvs/" + extracted_name)
        else:
            print("Extracted netlist not found!")
            exit(1)

    netlist = Netlist("lvs/" + extracted_name, verbose=False)
    if netlist.getSubcircuit( cell_name ) is None:
        print("Extracted circuit does not contain cell " + cell_name)
        exit(1)
    
    circuit = netlist.makeCircuit(cell_name)
    check = Symcheck(circuit)
    id = check.identifyTerminals()

    inputs = id['I']
    outputs = id['O']
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

    if not quiet:
        print("Cell summary :")
        print("\tTransistors      :", len(circuit.getElements()))
        print("\tInput terminals  :", " ".join(inputs))
        print("\tOutput terminals :", " ".join(outputs))
        print("\tPower terminal   :", power)
        print("\tGround terminal  :", ground)

    siteName = SymTech.technology['LEF_siteName']
    x, y = SymTech.technology['LEF_siteSize'].split()
    siteSize = (float(x), float(y))
    lef_site = LEF_site(siteName, siteSize)

    try:
        gds = gdstk.read_gds(gds_name)
    except:
        print('Input file not found.')
        exit(1)

    cell = find_cell(cell_name, gds)
    if cell is None:
        print("ERROR : Cell", cell_name, "not found in GDSII library.")
        exit(1)

    ref_names = [ref.cell_name for ref in cell.references]
    nrefs = len(ref_names)
    if nrefs > 0:
        print("ERROR : cell contains references ", " ".join(ref_names))
        exit(1)

    prBoundary = int(SymTech.technology['LEF_prBoundary'])
    pr_size = cellSize(cell, prBoundary)
    if pr_size is None:
        print("ERROR : prBoundary not found in cell", cell_name)
        exit(1)

    if not quiet:
        print("Cell size is", pr_size)

    macro = LEF_macro(cell_name, lef_site, pr_size, [])

    # Check if all labels are on the same layer
    labels = cell.labels
    lay_set = set()
    dt_set = set()
    for label in labels:
        lay_set.add(label.layer)
        dt_set.add(label.texttype)
    if len(lay_set) != 1 or len(dt_set) != 1:
        print("ERROR : Found labels on multiple layers/datatypes.")
        exit(1)
    lay = list(lay_set)[0]
    dt = list(dt_set)[0]

    # Find all polygons on lay,0
    polygons = []
    for poly in cell.polygons:
        if poly.layer == lay and poly.datatype == 0:
            polygons.append(poly)
    
    # Sort 
    obs_geom = LEF_pin_geom()
    obstructions = LEF_obs(obs_geom)
    for poly in polygons:
        geom = LEF_pin_geom()
        polygon = LEF_polygon(poly.points)
        if not usePolygons:
            shapes = polygon.to_rectangles()
        else:
            shapes = polygon
        geom.add_shape(shapes)
        for label in labels:
            if poly.contain(label.origin):
                # Label is inside a polygon, so it is a pin
                if label.text == power:
                    # Power pin
                    macro.geom.append( LEF_pin(label.text, LEF_PINTYPE.POWER, geom) )
                    geom = None
                    continue
                if label.text == ground:
                    # Ground pin
                    macro.geom.append( LEF_pin(label.text, LEF_PINTYPE.GROUND, geom) )
                    geom = None
                    continue
                if label.text in inputs:
                    # Ground pin
                    pin = LEF_pin(label.text, LEF_PINTYPE.IN, geom)
                    pin.antenna_gatearea = netlist.calcGateArea(cell_name, label.text)
                    macro.geom.append( pin )
                    geom = None
                    continue
                if label.text in outputs:
                    # Ground pin
                    pin = LEF_pin(label.text, LEF_PINTYPE.OUT, geom)
                    pin.antenna_diffarea = netlist.calcDiffArea(cell_name, label.text)
                    macro.geom.append( pin )
                    geom = None
                    continue
        # No label in polygon, this is an obstruction
        if geom is not None:
            for shape in geom.shapes:
                obs_geom.add_shape(shape)
    macro.geom.append(obs_geom)

    lef_filename = cell_name + ".lef"
    if not quiet:
        print("Writing LEF to file", lef_filename)
    else:
        print("DONE", end = "")
    macro.write_to_file(lef_filename)
    if not quiet:
        print("*"*80)

if __name__ == "__main__":
    main()
