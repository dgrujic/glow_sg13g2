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
import os
import datetime
import subprocess
from pathlib import Path
from glow_utils.manifest import Manifest
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symsim import Symsim
from glow_utils.symtech import SymTech
from jinja2 import Environment, FileSystemLoader

defaultTemplatePath = "$GLOW_ROOT/code/templates"
defaultReportPath = "$GLOW_ROOT/doc/glow_sg13g2/src"

def printusage():
    print("*"*80)
    print("")
    print("genreport generates a report for a cell group")
    print("")
    print("Reports are generated for specified cells in a given YAML manifest,")
    print("by rendering Jinja report templates located at $GLOW_ROOT/code/templates.")
    print("Reports are by default written in $GLOW_ROOT/doc/glow_sg13g2/src.")
    print("Template and report output directories can be changed by setting")
    print("environment variables $GLOW_TEMPLATES and $GLOW_REPORT.")
    print("")
    print("Usage :")
    print("genreport [options] manifest_file")
    print("")
    print("manifest_file is a YAML file containing information on cell groups and cells.")
    print("See the workflow/glow_utils documentation for manifest file structure.")
    print("Options:")
    print("\t", "-g, --group", "\t", "Generate a report for a cell group.")
    print("\t", "-t, --type", "\t", "Generate reports for a cell type.")
    print("\t", "-a, --all", "\t", "Generate reports for all cells.")
    print("\t", "-s, --summary", "\t", "Generate a top level page for generated reports.")
    print("\t", "\t", "\t", "Top level page will overwrite the SUMMARY.md file.")
    print("\t", "--quiet", "\t", "Print only essential information.")
    print("*"*80)

def printLogo():
    print("\t",r"                                             _   ")
    print("\t",r"   __ _  ___ _ __  _ __ ___ _ __   ___  _ __| |_ ")
    print("\t",r"  / _` |/ _ \ '_ \| '__/ _ \ '_ \ / _ \| '__| __|")
    print("\t",r" | (_| |  __/ | | | | |  __/ |_) | (_) | |  | |_ ")
    print("\t",r"  \__, |\___|_| |_|_|  \___| .__/ \___/|_|   \__|")
    print("\t",r"  |___/                    |_|                   ")


def groups_from_manifest(manifest, cell_group, cell_types, cell_all):
    """
    Generate a list of groups from manifest and list of cell_groups, cell_types, or all cells
    """
    if cell_all:
        # Return all cells
        groups = manifest.getCellGroups()
        return groups
    # Add individual groups
    groups = []
    # Add groups
    for group in cell_group:
        groups.append(group)
    # Add cells by type
    for cell_type in cell_types:
        for group in manifest.getCellGroups(cell_type):
            groups.append(group)
    return groups

def getPins(cell):
    """
    Returns a dictionary with pin information
    """
    pins = {}
    for pin in cell['pins']:
        pins.update( { pin : cell['pins'][pin]['description']} )
    return pins

#
# Layout related
#

def hasLayout(cellName):
    cellPath = os.path.expandvars("$GLOW_ROOT/cells/" + cellName)
    cellLayoutFile = cellName + ".gds"
    # Check if cell layout exists
    if Path(cellPath + "/" + cellLayoutFile).is_file():
        return True
    else:
        return False

def layoutArea(cellName):
    if not hasLayout(cellName):
        return {}
    else:
        # Calculate cell width in unit sites and area
        result = {}
        tech = SymTech.technology
        siteWidth, siteHeight = num1, num2 = [float(x) for x in tech["LEF_siteSize"].split()]
        prBoundary = int(tech["LEF_prBoundary"])
        cellPath = os.path.expandvars("$GLOW_ROOT/cells/" + cellName)
        cellLayoutFile = cellName + ".gds"
        cmd = "gdsinfo " + cellPath + "/" + cellLayoutFile + " --area " + str(prBoundary) + ",0"
        res = subprocess.run(cmd, cwd=cellPath, shell=True, capture_output=True, text=True)
        outLines = res.stdout.split('\n')
        for line in outLines:
            x = line.strip().split()
            if len(x) == 4:
                if x[0] == cellName:
                    w = float(x[1])
                    a = float(x[3])
                    result.update({'width' : round(w / siteWidth) })
                    result.update({'area' : a })
                    return result
        return result

def gdsToSVG(manifest, groupName, quiet, reportFigPath):
    """
    Generate SVG of group cell layouts
    """
    cells = manifest.getCellGroupCells(groupName)
    for cellName in cells:
        cellPath = os.path.expandvars("$GLOW_ROOT/cells/" + cellName)
        cellLayoutFile = cellName + ".gds"
        # Check if cell layout exists
        if not hasLayout(cellName):
            # Cell layout does not exist
            continue
        else:
            cmd = "gds2svg " + cellLayoutFile + " -c " + cellName
            res = subprocess.run(cmd, cwd=cellPath, shell=True, capture_output=True, text=True)
            if res.returncode != 0:
                # Something went wrong
                if quiet:
                    print("\t", cellName, "GDS2SVG ERROR", end="")
                else:
                    print("INFO : Error while converting ", cellName, " GDSII to SVG")
                continue
            cmd = "cp " + cellName + ".svg " + reportFigPath
            res = subprocess.run(cmd, cwd=cellPath, shell=True, capture_output=True, text=True)
            if res.returncode != 0:
                # Something went wrong
                if quiet:
                    print("\t", cellName, "SVG COPY ERROR", end="")
                else:
                    print("INFO : Error while copying ", cellName, " SVG")
            else:
                print("\t", cellName, "SVG", end="")

#
# Summary generator
#

def generateSummary(groups, templatePath):
    """
    Generate SUMMARY.md
    """
    template_dir = os.path.expandvars(templatePath)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_summary.jinja")

    # Data for Jinja template
    data = {
        "cell_groups": groups,
    }

    return template.render(data)

#
# Combinatorial report generator
#

def combinatorialReport(manifest, groupName, templatePath):
    """
    Generate a report for combinatorial gate
    """
    groups = manifest.getCellGroups()

    group = groups[ groupName ]
    pins = getPins(group)
    logicEquations = group['function']
    optional = group['optional']

    # Import the first of a cell group to simulate the truth table
    cellName = group['cells'][0]
    Symsubcircuit.importCell(cellName)
    circuit = Symsubcircuit.getSubckts()[cellName + "_flat"]
    sim = Symsim(circuit, verbose=False)
    tbls = sim.reducedTruthTables()
    simInputs = sim.getInputNames()
    truthTable = {  "inputs" : simInputs}
    logicFunctions = {}

    for entry in tbls:
        name, values = entry
        logicFunctions.update( {name : values} )
    truthTable.update({"functions" : logicFunctions})

    # Process cell variants
    cellVariants = {}
    for cellName in group['cells']:
        Symsubcircuit.importCell(cellName)
        circuit = Symsubcircuit.getSubckts()[cellName]
        circuit_flat = Symsubcircuit.getSubckts()[cellName + "_flat"]
        cellInfo = {}
        cellInfo.update( {'spice' : circuit.netlist_SPICE().strip() } )
        cellInfo.update( {'spice_flat' : circuit_flat.netlist_SPICE().strip() } )
        cellInfo.update( {'cdl' : circuit_flat.netlist_CDL().strip() } )
        if hasLayout(cellName):
            cellInfo.update( {'layout' : cellName } )
            cellInfo.update( layoutArea(cellName) )
        cellVariants.update( {cellName : cellInfo})

    template_dir = os.path.expandvars(templatePath)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_combinatorial.jinja")

    # Data for Jinja template
    data = {
        "cell_group": groupName,
        "cell_group_description" : group['description'],
        "pins" : pins,
        "logicEquations" : logicEquations,
        "optional" : optional,
        "truthTable" : truthTable,
        "cellVariants" : cellVariants,
        "timestamp" : datetime.datetime.now().strftime(r"%d-%m-%Y %H:%M:%S")
    }

    return template.render(data)


#
# D flip-flop report generator
#

def dffReport(manifest, groupName, templatePath):
    """
    Generate a report for a D flip-flop
    """
    groups = manifest.getCellGroups()

    group = groups[ groupName ]
    pins = getPins(group)
    if 'optional' in group.keys():
        optional = group['optional']
    else:
        optional = {}

    # Import the first of a cell group to simulate the truth table
    cellName = group['cells'][0]
    Symsubcircuit.importCell(cellName)
    circuit = Symsubcircuit.getSubckts()[cellName + "_flat"]
    sim = Symsim(circuit, verbose=False)
    spec = group['function']
    spec = {value: key for key, value in spec.items()}
    tbl = sim.dffTable(spec)
    # Process cell variants
    cellVariants = {}
    for cellName in group['cells']:
        Symsubcircuit.importCell(cellName)
        circuit = Symsubcircuit.getSubckts()[cellName]
        circuit_flat = Symsubcircuit.getSubckts()[cellName + "_flat"]
        cellInfo = {}
        cellInfo.update( {'spice' : circuit.netlist_SPICE().strip() } )
        cellInfo.update( {'spice_flat' : circuit_flat.netlist_SPICE().strip() } )
        cellInfo.update( {'cdl' : circuit_flat.netlist_CDL().strip() } )
        if hasLayout(cellName):
            cellInfo.update( {'layout' : cellName } )
            cellInfo.update( layoutArea(cellName) )
        cellVariants.update( {cellName : cellInfo})

    template_dir = os.path.expandvars(templatePath)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_dff.jinja")

    # Data for Jinja template
    data = {
        "cell_group": groupName,
        "cell_group_description" : group['description'],
        "pins" : pins,
        "optional" : optional,
        "truthTable" : tbl,
        "cellVariants" : cellVariants,
        "timestamp" : datetime.datetime.now().strftime(r"%d-%m-%Y %H:%M:%S")
    }

    return template.render(data)

#
# D latch report generator
#

def dlatchReport(manifest, groupName, templatePath):
    """
    Generate a report for a D latch
    """
    groups = manifest.getCellGroups()

    group = groups[ groupName ]
    pins = getPins(group)
    if 'optional' in group.keys():
        optional = group['optional']
    else:
        optional = {}

    # Import the first of a cell group to simulate the truth table
    cellName = group['cells'][0]
    Symsubcircuit.importCell(cellName)
    circuit = Symsubcircuit.getSubckts()[cellName + "_flat"]
    sim = Symsim(circuit, verbose=False)
    spec = group['function']
    spec = {value: key for key, value in spec.items()}
    tbl = sim.latchTable(spec)
    # Process cell variants
    cellVariants = {}
    for cellName in group['cells']:
        Symsubcircuit.importCell(cellName)
        circuit = Symsubcircuit.getSubckts()[cellName]
        circuit_flat = Symsubcircuit.getSubckts()[cellName + "_flat"]
        cellInfo = {}
        cellInfo.update( {'spice' : circuit.netlist_SPICE().strip() } )
        cellInfo.update( {'spice_flat' : circuit_flat.netlist_SPICE().strip() } )
        cellInfo.update( {'cdl' : circuit_flat.netlist_CDL().strip() } )
        if hasLayout(cellName):
            cellInfo.update( {'layout' : cellName } )
            cellInfo.update( layoutArea(cellName) )
        cellVariants.update( {cellName : cellInfo})

    template_dir = os.path.expandvars(templatePath)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_dff.jinja")

    # Data for Jinja template
    data = {
        "cell_group": groupName,
        "cell_group_description" : group['description'],
        "pins" : pins,
        "optional" : optional,
        "truthTable" : tbl,
        "cellVariants" : cellVariants,
        "timestamp" : datetime.datetime.now().strftime(r"%d-%m-%Y %H:%M:%S")
    }

    return template.render(data)

#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    # Input file list
    parser.add_argument('-g', '--group', action='append', default=[])
    parser.add_argument('-t', '--type', action='append', default=[])
    parser.add_argument('-a', '--all',  action='store_true')
    parser.add_argument('-s', '--summary',  action='store_true')
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('input_file')

    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    quiet = True if args.quiet else False

    # Check if user has set GLOW_TEMPLATE or GLOW_REPORT environment variables
    templatePath = os.environ.get("GLOW_TEMPLATE", default=defaultTemplatePath)
    reportPath = os.environ.get("GLOW_REPORT", default=defaultReportPath)

    if not quiet:
        printLogo()
        print("")
        print("Using template path :", templatePath)
        print("Using report path   :", reportPath)

    manifest_file = args.input_file

    if not quiet:
        print("*"*80)
        print("Reading manifest file :", manifest_file)
    manifest = Manifest(manifest_file)

    groups = groups_from_manifest(manifest, args.group, args.type, args.all)
    # Eliminate duplicate entries
    groups = list(set(groups))
    groups.sort()

    if not quiet:
        print("Generating reports for :")
        print(" ".join(groups))

    error_groups = []

    glow_root = os.environ.get("GLOW_ROOT", default=None)
    if glow_root is None:
        glow_root = Path.cwd().parent
        if not quiet:
            print("WARNING : GLOW_ROOT is not set, using " + str(glow_root))

    for group in groups:
        groupType = manifest.getCellGroupType(group)

        if not quiet:
            print("*" * 80)
            print("Generating report for group", group, end="")
        else:
            print(group, end="")

#        try:
        res = None
        if groupType == "combinatorial" or groupType == "constant":
            res = combinatorialReport(manifest, group, templatePath)
        elif groupType == "dff":
            res = dffReport(manifest, group, templatePath)
        elif groupType == "dlatch":
            res = dlatchReport(manifest, group, templatePath)
        if res is not None:
            # Write the report
            reportFilename = os.path.expandvars(reportPath)
            reportFilename += "/" + group + ".md"
            with open(reportFilename, "w") as file:
                file.write(res)
            # Generate layout SVG
            reportFigPath = os.path.expandvars(reportPath) + "/figs"
            gdsToSVG(manifest, group, quiet, reportFigPath)
            print("\tOK")
        else:
            print("\tWARNING : Unsupported group type", groupType, "SKIPPING")
        # except:
        #     print("\tERROR")
        #     error_groups.append(group)

    if args.summary:
        # Generate SUMMARY.md
        try:
            print("Generating summary...", end="")
            res = generateSummary(groups, templatePath)
            reportFilename = os.path.expandvars(reportPath)
            reportFilename += "/SUMMARY.md"
            with open(reportFilename, "w") as file:
                file.write(res)
            print("\tOK")
        except:
            print("\tERROR")

    if len(error_groups) > 0:
        print("ERROR in [" +str(len(error_groups))+ "] cells : " + " ".join(error_groups))
        exit(1)
    else:
        if not quiet:
            print("ALL OK [" + str(len(groups)) + "]")
        exit(0)

if __name__ == "__main__":
    main()

