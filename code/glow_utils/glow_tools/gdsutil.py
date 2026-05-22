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

import gdstk
import argparse

sw_version = "1.0"

#
# Utility to manipulate GDSII files
# - Perform hierarchy flattening
# - Convert paths to polygons
# - Change layer and/or data type numbers of polygons, paths or labels
# - Merge polygons
# - Append cells to GDSII library
# 

def printusage():
    print("*"*80)
    print("\t",r"            _           _   _ _ ")
    print("\t",r"           | |         | | (_) |")
    print("\t",r"   __ _  __| |___ _   _| |_ _| |")
    print("\t",r"  / _` |/ _` / __| | | | __| | |")
    print("\t",r" | (_| | (_| \__ \ |_| | |_| | |")
    print("\t",r"  \__, |\__,_|___/\__,_|\__|_|_|")
    print("\t",r"   __/ |                        ")
    print("\t",r"  |___/                         ")
    print("")
    print("gdsutil is an utility to manipulate GDSII libraries")
    print("Usage:")
    print("gdsutil [commands]")
    print("Commands:")
    print("\t", "-i, --infile", "\t", "Input files. At least one input file is required.")
    print("\t", "-o, --outfile", "\t", "Output file. If exists, output file will be overwritten.")
    print("\t", "-a, --append", "\t", "Output file for append write.")
    print("\t", "-c, --cells", "\t", "Cells to work on. Single cells or a list of cell can be given")
    print("\t", "--warn_duplicate", "Only issue a warning if duplicate cells are found in different libraries.")
    print("\t", "--flatten", "\t", "Flatten the cells.")
    print("\t", "--to_polygons", "\t", "Convert paths to polygons.")
    print("\t", "-r, --remap", "\t", "Remap layers per given rules.")
    print("\t", "-m, --merge", "\t", "Merge shapes on specified layers. Shapes on the same layer and datatype are merged.")
    print("\t", "-d, --delete", "\t", "Delete shapes on specified layers.")
    print("\t", "-l, --label", "\t", "Rename labels per given rules")
    print("")
    print("Remap rules are specified as:")
    print("\t", "src_lay,src_dt dst_lay,dst_dt [polygon | path | label] ")
    print("\t", "src_lay and src_dt are source layer and datatype.")
    print("\t", "Asterisk * can be used to specify any layer or datatype")
    print("\t", "dst_lay, dst_dt are destination layer and datatype")
    print("\t", "Destination layer/datatype must be a concrete number.")
    print("")
    print("Remap rule examples:")
    print("\t", "1,* 1,0 polygon remaps polygons on layer 1 and any datatype")
    print("\t", "                to layer 1 and datatype 0")
    print("\t", "*,2 *,0 polygon remaps polygons on any layer and datatype 2")
    print("\t", "                to the same layer and datatype 0")
    print("")
    print("Merge rule examples:")
    print("\t", "*,* merges shapes on all layers and datatypes")
    print("\t", "5,* merges shapes on layer 5 and any datatype")
    print("")
    print("Delete rule example:")
    print("\t", "5,* deletes shapes on layer 5 and any datatype")
    print("")
    print("Rename label example:")
    print("\t", "vsup,vdd renames label text vsup with vdd")
    print("")
    print("Only selected operations are performed in the following order:")
    print("\tFlatten cell")
    print("\tConvert paths to polygons")
    print("\tDelete layers")
    print("\tRemap layers")
    print("\tMerge layers")
    print("\tRename labels")
    print("")
    print("Examples:")
    print("")
    print("Read in.gds, flatten cell1 and cell2 and write these cells to out.gds")
    print("gdsutil -i in.gds -o out.gds --flatten --cels \"cell1 cell2\"")
    print("")
    print("Read in.gds, flatten cell1 and cell2, merge shapes and write these cells to out.gds")
    print("gdsutil -i in.gds -o out.gds --merge *,* --flatten --cels \"cell1 cell2\"")
    print("")
    print("*"*80)

def parse_remap_rules(args):
    # Check if layer/dtype pairs and object types are valid
    remap_rules = {"path" : [], "polygon" : [], "label" : []}
    for rule in args.remap:
        lay_dt_1, lay_dt_2, objtype = rule
        if objtype not in ["path", "polygon", "label"]:
            print("Object type in layer remap rule", rule, "is not valid.")
            continue
        tmp = lay_dt_1.split(',')
        if not((tmp[0].isdecimal() or tmp[0]=='*') and (tmp[1].isdecimal() or tmp[1]=='*')):
            print("Layer/datatype", lay_dt_1, "in layer remap rule", rule, "is not valid.")
            continue
        else:
            if tmp[0] == '*':
                lay1 = '*'
            else:
                lay1 = int(tmp[0])
            if tmp[1] == '*':
                dt1 = '*'
            else:
                dt1 = int(tmp[1])
        tmp = lay_dt_2.split(',')
        if not((tmp[0].isdecimal() or tmp[0]=='*') and (tmp[1].isdecimal() or tmp[1]=='*')):
            print("Layer/datatype", lay_dt_2, "in layer remap rule", rule, "is not valid.")
            continue
        else:
            if tmp[0] == '*':
                lay2 = '*'
            else:
                lay2 = int(tmp[0])
            if tmp[1] == '*':
                dt2 = '*'
            else:
                dt2 = int(tmp[1])
        rules = remap_rules[objtype]
        rules.append(((lay1, dt1), (lay2, dt2)))
    return remap_rules

def apply_remap_rules(lay_dt, remap_rules):
    # Apply layer/datatype remap rules
    layer, datatype = lay_dt
    for rule in remap_rules:
        src, dst = rule
        src_lay, src_dt = src
        dst_lay, dst_dt = dst
        if (dst_lay == '*') or (dst_dt == '*'):
            # Match input layer/datatype
            if (dst_lay == '*') and (src_lay == '*'):
                # Match input layer
                res_lay, tmp = lay_dt
            elif (src_lay == '*') or (src_lay == layer):
                if (dst_lay != '*'):
                    res_lay = dst_lay
                else:
                    res_lay = layer
            if (dst_dt == '*') and (src_dt == '*'):
                # Match input datatype
                tmp, res_dt = lay_dt
                return (res_lay, res_dt)
            elif (src_dt == '*') or (src_dt == datatype):
                if (dst_dt != '*'):
                    res_dt = dst_dt
                else:
                    res_dt = datatype
                return (res_lay, res_dt)
        if (src_lay == '*') or (src_lay == layer):
            if (src_dt == '*') or (src_dt == datatype):
                return dst
    return lay_dt

def number_of_remap_rules(remap_rules):
    nrules = len(remap_rules['polygon'])
    nrules += len(remap_rules['path'])
    nrules += len(remap_rules['label'])
    return nrules

def print_remap_rules(remap_rules):
    polygon_rules = remap_rules['polygon']
    path_rules = remap_rules['path']
    label_rules = remap_rules['label']
    if len(polygon_rules) == 0:
        print("No polygon layer remap rules")
    else:
        print("Polygon layer remap rules:")
        for rule in polygon_rules:
            print("\t" + str(rule[0]) + " -> " + str(rule[1]))
    if len(path_rules) == 0:
        print("No path layer remap rules")
    else:
        print("Path layer remap rules:")
        for rule in path_rules:
            print("\t" + str(rule[0]) + " -> " + str(rule[1]))
    if len(label_rules) == 0:
        print("No label layer remap rules")
    else:
        print("Label layer remap rules:")
        for rule in path_rules:
            print("\t" + str(rule[0]) + " -> " + str(rule[1]))

def parse_merge_rules(args):
    # Check if layer/dtype pairs are valid
    merge_rules = []
    for rule in args.merge:
        tmp = rule.split(',')
        if not((tmp[0].isdecimal() or tmp[0]=='*') and (tmp[1].isdecimal() or tmp[1]=='*')):
            print("Layer/datatype in layer merge rule", rule, "is not valid.")
            continue
        else:
            if tmp[0] == '*':
                lay1 = '*'
            else:
                lay1 = int(tmp[0])
            if tmp[1] == '*':
                dt1 = '*'
            else:
                dt1 = int(tmp[1])
        merge_rules.append((lay1, dt1))
    return merge_rules

def print_merge_rules(merge_rules):
    if len(merge_rules) == 0:
        print("No layer merge rules")
    else:
        print("Layer merge rules:")
        for rule in merge_rules:
            print("\t" + str(rule[0]) + "," + str(rule[1]))

def is_merged(lay_dt, merge_rules):
    # Determine if layer is merged per merge rules
    layer, datatype = lay_dt
    for rule in merge_rules:
        lay, dt = rule
        if (lay == '*') or (lay == layer):
            if (dt == '*') or (dt == datatype):
                return True
    return False

def parse_delete_rules(args):
    # Check if layer/dtype pairs are valid
    delete_rules = []
    for rule in args.delete:
        tmp = rule.split(',')
        if not((tmp[0].isdecimal()) and (tmp[1].isdecimal() or tmp[1]=='*')):
            print("Layer/datatype in layer delete rule", rule, "is not valid.")
            continue
        else:
            lay = int(tmp[0])
            if tmp[1] == '*':
                dt = '*'
            else:
                dt = int(tmp[1])
        delete_rules.append((lay, dt))
    return delete_rules

def print_delete_rules(delete_rules):
    if len(delete_rules) == 0:
        print("No layer delete rules")
    else:
        print("Layer delete rules:")
        for rule in delete_rules:
            print("\t" + str(rule[0]) + "," + str(rule[1]))

def parse_label_rules(args):
    # Parse label renaming rules
    label_rules = []
    for rule in args.label:
        old_name, new_name = rule.split(',')
        label_rules.append((old_name, new_name))
    return label_rules

def print_label_rules(label_rules):
    if len(label_rules) == 0:
        print("No label renaming rules")
    else:
        print("Label renaming rules:")
        for rule in label_rules:
            print("\t" + str(rule[0]) + "->" + str(rule[1]))

def parse_string_names(str_arr):
    cells = []
    for x in str_arr:
        if " " in x:
            tmp = x.split(" ")
            for name in tmp:
                cells.append(name)
        else:
            cells.append(x)
    return cells

def find_cell(name, libs):
    """
    Find a cell with given name in a list of given libraries.
    First occurence of a cell is returned, or None if not found.
    """
    for lib in libs:
        for cell in lib.cells:
            if cell.name == name:
                return cell
    return None

def paths_to_polygons(cell):
    # Convert all paths in a cell to polygons
    for path in cell.paths:
        polygons = path.to_polygons()
        cell.remove(path)
        cell.add(*polygons)

def delete_layers(cell : gdstk.Cell, delete_rules):
    # Delete all paths, polygons and labels per given delete rules
    spec = []
    for rule in delete_rules:
        # Make layer specification for layer deletion
        lay, dt = rule
        if dt == '*':
            for i in range(0, 256):
                # Add all data types to spec
                spec.append( (lay, i) )
        else:
            spec.append( (lay, dt) )
    cell.filter( spec, remove=True)

def remap_layers(cell : gdstk.Cell, remap_rules):
    # Remap layers in a cell
    remap = remap_rules['polygon']
    if len(remap) > 0:
        for polygon in cell.polygons:
            lay = polygon.layer
            dt = polygon.datatype
            lay, dt = apply_remap_rules((lay, dt), remap)
            polygon.layer = lay
            polygon.datatype = dt
    
    remap = remap_rules['path']
    if len(remap) > 0:
        for path in cell.paths:
            lay = path.layers[0]
            dt = path.datatypes[0]
            lay, dt = apply_remap_rules((lay, dt), remap)
            path.set_layers( lay )
            path.set_datatypes( dt )
    
    remap = remap_rules['label']
    if len(remap) > 0:
        for label in cell.labels:
            lay = label.layer
            dt = label.texttype
            lay, dt = apply_remap_rules((lay, dt), remap)
            label.layer = lay
            label.texttype = dt

def merge_layers(cell : gdstk.Cell, merge_rules):
    # Merge specified layers in a cell
    lay_dt_set = get_layer_info(cell)
    # Make a dictonary of used layer/datatypes to group shapes
    lay_dict = {lay_dt: [] for lay_dt in lay_dt_set}
    # Separate polygons per layer
    for poly in cell.polygons:
        lay = poly.layer
        dt = poly.datatype
        lay_dt = (lay, dt)
        lay_dict[lay_dt].append(poly)    
    
    for lay_dt in lay_dict.keys():
        if is_merged(lay_dt, merge_rules):
            lay, dt = lay_dt
            polygons = lay_dict[lay_dt]
            merged = gdstk.boolean(polygons, [], "or", layer=lay, datatype=dt)
            cell.remove(*polygons)
            cell.add(*merged)

def rename_labels(cell : gdstk.Cell, label_rules):
    # Rename labels
    # Make a dictionary from label renaming rules
    label_dict = dict(label_rules)
    label_set = set(label_dict.keys())
    for label in cell.labels:
        if label.text in label_set:
            # Found label that matches the rule for replacement
            label.text = label_dict[label.text]

def get_layer_info(cell : gdstk.Cell):
    # Returns a set of tuples (layer number, data type) used in the cell
    fcell = cell.copy(cell.name + "_fcellcopy")
    fcell = fcell.flatten()
    layer_set = set()
    for polygon in fcell.polygons:
        layer = polygon.layer
        dt = polygon.datatype
        layer_set.add( (layer, dt) )
    for path in fcell.paths:
        polygons = path.to_polygons()
        for polygon in polygons:
            layer = polygon.layer
            dt = polygon.datatype
            layer_set.add( (layer, dt) )
    for label in fcell.labels:
        layer = label.layer
        dt = label.texttype
        layer_set.add( (layer, dt) )
    return layer_set

def get_reference_names(cell : gdstk.Cell):
    # Returns a tuple (number of references, list of referenced cell names)
    names = [ref.cell_name for ref in cell.references]
    nrefs = len(names)
    names = set(names)
    return (nrefs, list(names))

#
# Main code
#
def main():
    parser = argparse.ArgumentParser()

    # Input file list
    parser.add_argument('-i', '--infile', action='append', default=[])

    # Cells to work on
    parser.add_argument('-c', '--cells', action='append', default=[])

    # Flatten cells argument
    parser.add_argument('--flatten', action='store_true')

    # Convert paths to polygons
    parser.add_argument('--to_polygons', action='store_true')

    # Change layers
    parser.add_argument('-r', '--remap', nargs=3, action='append', default=[])

    # Merge shapes
    parser.add_argument('-m', '--merge', action='append', default=[])

    # Delete layer
    parser.add_argument('-d', '--delete', action='append', default=[])

    # Rename label
    parser.add_argument('-l', '--label', action='append', default=[])

    # Switch to warn on duplicate cell definitions
    parser.add_argument('--warn_duplicate', action='store_true')

    # Output file for write or append are mutually exclusive
    # Output file
    parser.add_argument('-o', '--outfile')
    # Output file for append operation
    parser.add_argument('-a', '--append')

    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    if (args.infile == []) or (args.outfile == None and args.appendfile == None):
        printusage()
        exit(1)

    print("*"*80)
    print((" "*30) + "GDSII Utility v" + sw_version)
    print("*"*80)
    input_files = parse_string_names(args.infile)
    print("Input files [" + str(len(input_files)) + "]")
    print(" ".join(input_files))
    print("")
    cells = parse_string_names(args.cells)
    print("Cells to work on [" + str(len(cells)) + "]")
    print(" ".join(cells))
    print("")
    warn_duplicate = args.warn_duplicate
    if warn_duplicate:
        print("Warn on duplicate cell names and ignore extra cells.")
    else:
        print("Duplicate cell names are not allowed.")
    print("")
    # Output file
    outfile = args.outfile
    appendfile = args.append
    if (outfile is None) and (appendfile is None):
        print("ERROR : Neither output or append file were given.")
        exit(1)
    elif (outfile is not None) and (appendfile is not None):
        print("ERROR : Both output and append file are given.")
        exit(1)
    if outfile is not None:
        print("Output will be WRITTEN to file", outfile)
    if appendfile is not None:
        print("Output will be APPENDED to file", appendfile)
    print("")
    # Parse layer remap rules
    remap_rules = parse_remap_rules(args)
    print_remap_rules(remap_rules)
    print("")
    # Parse layer merge rules
    merge_rules = parse_merge_rules(args)
    print_merge_rules(merge_rules)
    print("")
    # Parse layer delete rules
    delete_rules = parse_delete_rules(args)
    print_delete_rules(delete_rules)
    # Parse label renaming rules
    label_rules = parse_label_rules(args)
    print_label_rules(label_rules)
    print("*"*80)

    # Read input files
    total_cells = 0
    input_libs = []
    all_cell_names = set()
    for fname in input_files:
        print("Reading input file : " + fname + " ... ", end = "")
        try:
            gds = gdstk.read_gds(fname)
        except:
            print('Input file ' + fname + ' not found.')
            exit(1)
        total_cells += len(gds.cells)
        print("found " + str(len(gds.cells)) + " cells.")
        cell_names = [cell.name for cell in gds.cells]
        print("Cells : ")
        print(" ".join(cell_names))
        print("*"*80)
        duplicate_names = all_cell_names.intersection(set(cell_names))
        if len(duplicate_names) > 0:
            if warn_duplicate:
                print("WARNING : Found duplicate cells :", ", ".join(list(duplicate_names)))
            else:
                print("ERROR : Found duplicate cells :", ", ".join(list(duplicate_names)))
                exit(1)
        all_cell_names = all_cell_names.union(set(cell_names))

        input_libs.append(gds)

    print("Read in " + str(len(input_files)) + " GDSII libraries, with a total of " + str(total_cells) + " cells." )

    # Check if listed cells are in given libraries
    for cell in cells:
        if cell not in all_cell_names:
            print("ERROR : Cell", cell, "is not present in given libraries.")
            exit(1)

    if outfile is not None:
        output_lib = gdstk.Library()
    else:
        output_lib = gdstk.read_gds(appendfile)

    for cell_name in cells:
        print("*"*80)
        print("Working on cell", cell_name)
        cell = find_cell(cell_name, input_libs)
        if cell is None:
            print("ERROR : Cell ", cell_name, "not found.")
            exit(1)
        print("Cell info")
        print("\tLayers in cell", sorted(get_layer_info(cell)))
        nrefs, refs = get_reference_names(cell)
        print("\tReferences ["+str(nrefs)+"]", refs)
        print("\tPolygons",str(len(cell.polygons)))
        print("\tPaths",str(len(cell.paths)))
        print("\tLabels ["+str(len(cell.labels))+"]", " ".join(label.text for label in cell.labels))
        if args.flatten:
            print("Flattening cell..")
            cell.flatten()
        if args.to_polygons:
            print("Converting paths to polygons...")
            paths_to_polygons(cell)
        if len(delete_rules) > 0:
            print("Deleting layers :", delete_rules)
            delete_layers(cell, delete_rules)
        if number_of_remap_rules(remap_rules) > 0:
            print("Remapping layers...")
            remap_layers(cell, remap_rules)
        if len(merge_rules) > 0:
            print("Merging layers...")
            merge_layers(cell, merge_rules)
        if len(label_rules) > 0:
            print("Renaming labels...")
            rename_labels(cell, label_rules)
        output_lib.replace(cell)

    if outfile is not None:
        print("Writing GDSII", outfile)
        output_lib.write_gds(outfile)
    else:
        print("Appending GDSII", appendfile)
        output_lib.write_gds(appendfile)

if __name__ == "__main__":
    main()
