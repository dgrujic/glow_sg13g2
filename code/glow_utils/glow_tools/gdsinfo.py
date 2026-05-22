
import gdstk
import argparse

def printusage():
    print("*"*80)
    print("\t",r"            _     _        __      ")
    print("\t",r"           | |   (_)      / _|     ")
    print("\t",r"   __ _  __| |___ _ _ __ | |_ ___  ")
    print("\t",r"  / _` |/ _` / __| | '_ \|  _/ _ \ ")
    print("\t",r" | (_| | (_| \__ \ | | | | || (_) |")
    print("\t",r"  \__, |\__,_|___/_|_| |_|_| \___/ ")
    print("\t",r"   __/ |                           ")
    print("\t",r"  |___/                            ")
    print("")
    print("gdsinfo is an utility to perform checks on GDSII files")
    print("Usage:")
    print("gdsinfo input_file.gds [commands]")
    print("Commands:")
    print("\t--printcells\tPrint names of all cells in a library")
    print("\t--cells\t\tSpecify cells to work on, default is all cells")
    print("\t--noref\t\tRaise error if a cell contans a reference (cell has hierarchy)")
    print("\t--errlay\tRaise error if a cell contains a layer/datatype")
    print("\t--uselay\tAllow layer/datatype in a cell")
    print("See examples for uses of errlay and uselay")
    print("")
    print("Examples:")
    print("")
    print("Print a list of all cells in a GDSII library")
    print("gdsinfo infile.gds --printcells")
    print("")
    print("By default checks are performed on all cells.")
    print("To perform checks only on cell1 and cell2 use")
    print("gdsinfo infile.gds --cels \"cell1 cell2\"")
    print("")
    print("Trigger an error if a cell contains references to other cells")
    print("gdsinfo infile.gds --noref")
    print("")
    print("Forbid all layer/datatypes and explicitly allow any layer with datatype 0")
    print("Result is that any layer with datatype 0 is allowed")
    print("gdsinfo infile.gds --errlay *,* --uselay *,0")
    print("")
    print("Forbid all layer/datatypes and explicitly allow any layer only datatype 0")
    print("Additionally, allow layer 10 with datatype 2")
    print("Result is that any layer with datatype=0 is allowed and layer 10 with datatype 2")
    print("gdsinfo infile.gds --errlay *,* --uselay *,0 --uselay 10,2")
    print("*"*80)

def is_layer_allowed(layer : int, datatype : int, args):
    # Determine if layer/datatype combination is allowed
    # Forbidden combinations are in args.errlay
    # Allowed combinations are in args.uselay
    # Allowed layers take precedence over forbidden layers,
    # so if errlay = ['1,*'], which forbids any datatype on layer 1
    # and uselay = ['1,0'], which allows the use of datatype 0 on layer 1,
    # this function will return True for datatype 0 on layer 1,
    # and False for any other datatype
    errlayers = args.errlay
    uselayers = args.uselay
    res = True
    for errlay in errlayers:
        snum, sdt = errlay.split(',')
        if (snum == '*'):
            # All layers are forbidden
            # Check if data type is specified
            if (sdt == '*'):
                # All data types are forbidden
                res = False
                break
            else:
                # Check if specific datatype is forbidden
                if int(sdt) == datatype:
                    res = False
                    break
        elif int(snum) == layer:
            # Specific layer is forbidden
            # Check if data type is specified
            if (sdt == '*'):
                # All data types are forbidden
                res = False
                break
            else:
                # Check if specific datatype is forbidden
                if int(sdt) == datatype:
                    res = False
                    break
    # Check if layer is explicitly allowed for use
    for uselay in uselayers:
        snum, sdt = uselay.split(',')
        if (snum == '*'):
            # All layers are allowed
            # Check if data type is specified
            if (sdt == '*'):
                # All data types are allowed
                res = True
                break
            else:
                # Check if specific datatype is allowed
                if int(sdt) == datatype:
                    res = True
                    break
        elif int(snum) == layer:
            # Specific layer is allowed
            # Check if data type is specified
            if (sdt == '*'):
                # All data types are allowed
                res = True
                break
            else:
                # Check if specific datatype is allowed
                if int(sdt) == datatype:
                    res = True
                    break
    return res

def get_reference_names(cell : gdstk.Cell):
    # Returns a tuple (number of references, list of referenced cell names)
    names = [ref.cell_name for ref in cell.references]
    nrefs = len(names)
    names = set(names)
    return (nrefs, list(names))

def get_layer_info(cell : gdstk.Cell):
    # Returns a set of tuples (layer number, data type) used in the cell
    fcell = cell.flatten()
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
        dt = label.datatype
        layer_set.add( (layer, dt) )
    return layer_set

def process_cell(cell : gdstk.Cell, args):
    # Perform checks on cells
    err = False
    print("Processing cell", cell.name)
    # Get cell references
    nrefs, refs = get_reference_names(cell)
    if nrefs > 0:
        if args.noref:
            print("ERROR : Cell contains references and noref flag is set.")
            err = True
        print("Number of references " + str(nrefs) + ". Referenced cell names:\n\t" , end="")
        print("\n\t".join(refs))
    else:
        print("-- NO REFERENCES --")
    # Get cell labels
    labels = cell.get_labels()
    
    if len(labels) == 0:
        print("-- NO LABELS --")
    else:
        print("Labels :")
        for l in labels:
            res = is_layer_allowed(l.layer, l.texttype, args)
            if res:
                print("\t" + l.text + " ("+str(l.layer) + "," + str(l.texttype) +")")
            else:
                print("\t" + l.text + " ("+str(l.layer) + "," + str(l.texttype) +")"+"   \tERROR : this layer/data type combination is not allowed")

    # Get used layer info
    layer_set = get_layer_info(cell)
    layer_list = sorted(list(layer_set))
    print("Used layers :")
    for layer in list(layer_list):
        lnum, dt = layer
        res = is_layer_allowed(lnum, dt, args)
        if res:
            print("\t" + str(layer))
        else:
            print("\t" + str(layer)+"   \tERROR : this layer/data type combination is not allowed")
            err = True
    return err
#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('-c', '--cells', default='*')
    parser.add_argument('--printcells', action='store_true')
    parser.add_argument('--noref', action='store_true')
    parser.add_argument('--errlay', action='append', default=[])
    parser.add_argument('--uselay', action='append', default=[])
    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    print(args)

    try:
        gds = gdstk.read_gds(args.infile)
    except:
        print('Input file not found.')
        exit(1)

    print("Reading file " + args.infile)
    ncells = len(gds.cells)
    print("Found " + str(ncells) + " cells.")
    cell_names = [cell.name for cell in gds.cells]
    if args.printcells:
        for s in cell_names:
            print(s, end=' ')
        print("")

    # Generate list of cells to process
    if args.cells == "*":
        print("Processing all cells")
        to_process = cell_names
    else:
        if ' ' in args.cells:
            # List of cell names is given
            to_process = args.cells.split()
            i = 0
            tmp = ""
            while i < len(to_process):
                if to_process[i] not in cell_names:
                    print("WARNING : Cell " + to_process[i] + " does not exist. Ignoring.")
                    del to_process[i]
                else:
                    tmp += to_process[i] + " "
                    i += 1
            print("Processing cells : ", tmp)
        else:
            # Single cell name is given
            to_process = [args.cells]    

    errors = 0
    err_cells = []
    for cell_name in to_process:
        print("*"*80)
        err = process_cell(gds[cell_name], args)
        if err:
            errors += 1
            err_cells.append(cell_name)
    print("*"*80)
    if errors == 0:
        print("All OK.")
        exit(0)
    else:
        print("ERROR in " + str(errors) + " cells :")
        print(" ".join(err_cells))
        exit(1)

if __name__ == "__main__":
    main()
