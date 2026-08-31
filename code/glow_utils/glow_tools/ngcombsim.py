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

import os
import argparse
from sympy import symbols
from sympy.logic import SOPform
from sympy.logic import simplify_logic
from sympy import sympify
from sympy import bool_map
from glow_utils.ngspice import Ngspice

default_lib = ('$PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib', 'mos_tt')

def printusage():
    print("*"*80)
    print("\t",r"                                  _         _           ")
    print("\t",r"  _ __   __ _  ___ ___  _ __ ___ | |__  ___(_)_ __ ___  ")
    print("\t",r" | '_ \ / _` |/ __/ _ \| '_ ` _ \| '_ \/ __| | '_ ` _ \ ")
    print("\t",r" | | | | (_| | (_| (_) | | | | | | |_) \__ \ | | | | | |")
    print("\t",r" |_| |_|\__, |\___\___/|_| |_| |_|_.__/|___/_|_| |_| |_|")
    print("\t",r"        |___/                                           ")  
    print("")
    print("ngcombsim is an utility to simulate combinatorial circuit SPICE netlist in NGSPICE")
    print("")
    print("Usage:")
    print("ngcombsim input_file circuit [commands]")
    print("Commands:")
    print("\t--expected\tSpecify expected output Boolean functions")
    print("\t--strict\tEnforce strict checks")
    print("\t--lib   \tSpecify library model and corner")
    print("\t--cond  \tSpecify operating condition value")
    print("")
    print("Examples:")
    print("")
    print("Specify expected output function and check if the circuit function matches it.")
    print('ngcombsim NAND2_D1.sp NAND2_D1 --expected "Y = ~(A & B)"')
    print("")
    print("Specify SPICE library and corner.")
    print('ngcombsim NAND2_D1.sp NAND2_D1 --lib "$PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt"')
    print("")
    print("Specify operating condition.")
    print('ngcombsim NAND2_D1.sp NAND2_D1 --cond "supplyVoltage=1.3"')
    print("")

def getInputSymbols(inputNames):
    """
    Returns symbols from input names
    """
    if len(inputNames) > 0:
        inputs = " ".join(inputNames)
        res = symbols(inputs)
        # Ensure that return type is always a tuple, even if only one element is returned
        if not isinstance(res, tuple):
            return (res,)
        else:
            return res
    else:
        return None

def getFunctions(in_vals, out_vals, in_names, out_names ):
    """
    Returns a list of Boolean functions
    """
    in_syms = getInputSymbols( in_names )
    fns = []
    for nout in range(len(out_vals[0])):
        minterms = []
        for nin in range(len(in_vals)):
            if out_vals[nin][nout] == '1':
                minterms.append( [int(x) for x in in_vals[nin]] )
        logicExpr = simplify_logic(SOPform(in_syms, minterms))
        fns.append([out_names[nout], logicExpr])
    return fns

#
# Main code
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('circuit')
    parser.add_argument('--expected', action='append', default=[])
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--lib', action='append', default=[])
    parser.add_argument('--cond', action='append', default=[])

    try:
        args = parser.parse_args()
    except:
        printusage()
        exit(1)

    if "PDK_ROOT" not in os.environ:
        print("ERROR : PDK_ROOT is not set.")
        exit(1)

    infile = args.infile
    circuit_name = args.circuit
    print("Input file : " + infile)
    print("Circuit    : " + circuit_name)

    # Parse expected functions
    if args.expected == []:
        expected = None
    else:
        expected = {}
        for expr in args.expected:
            expr_name, expr_val = expr.split('=')
            expected.update( { expr_name.strip() : expr_val } )
        print("\nExpected Boolean expressions")
        for expr_name in expected:
            print(expr_name, '=', expected[expr_name])

    strict = args.strict

    print("")
    if args.lib == []:
        print("Using default library and corner.")
        libs = [ default_lib ]
    else:
        print("Using libraries")
        libs = []
        for lib in args.lib:
            print("\t", lib)
            libs.append( lib.split() )
    inc = []

    print("")
    conditions = { 'supplyVoltage' : 1.2, 'temperature' : 27.0 }
    if args.cond != []:
        for cond in args.cond:
            cond_name, cond_val = cond.split('=')
            try:
                conditions.update( {cond_name.strip() : float(cond_val)} )
                print("Setting condition :", cond)
            except:
                print("ERROR : Failed to parse", cond)
                exit(1)
    else:
        print("Using default conditions.")

    ng = Ngspice(libs, inc, conditions, infile, circuit_name, verbose=False)

    inputs, inputVals, outputs, outputVals = ng.combSim()
    print("")
    print("Inputs  : ", " ".join(inputs))
    print("Outputs : ", " ".join(outputs))
    print("")
    print("Simulated truth table")
    print("")
    nchars = 0
    for name in inputs:
        print(f"{name:<4}", end="")
        if len(name) < 4:
            nchars += 4
        else:
            nchars += len(name)
    for name in outputs:
        print(f"{name:<4}", end="")
        if len(name) < 4:
            nchars += 4
        else:
            nchars += len(name)
    print("")
    print("-" * nchars)

    for i in range(len(inputVals)):
        row = inputVals[i]
        for val in row:
            print(f"{str(val):<4}", end="")
        row = outputVals[i]
        for val in row:
            print(f"{str(val):<4}", end="")
        print("")

    print("-" * nchars)

    fns = getFunctions(inputVals, outputVals, inputs, outputs )

    print("")
    print("Circuit Boolean functions : ")
    for fn in fns:
        outName, fnExpr = fn
        print(outName, '=', fnExpr)

    if expected is not None:
        """
        Expected Boolean functions are given, try to match them to circuit function.
        """
        print("")
        print("Matching Boolean functions...")
        err = False

        # Parse expected functions
        expectedFns = {}
        for outName in expected:
            try:
                expectedFn = sympify(expected[outName], locals={'&': lambda x, y: x & y, '|': lambda x, y: x | y, '~': lambda x: ~x})
                expectedFns.update( { outName : expectedFn } )
            except:
                print("ERROR : Failed to parse expression", expected[outName])
                err = True

        # Check if a set of expected functions matches the circuit functions
        expectedSet = set(expectedFns.keys())
        circuitSet = set(dict(fns).keys())

        if expectedSet != circuitSet:
            if not strict:
                print("WARNING : Set of expected functions does not match the set of circuit outputs.")
            else:
                print("ERROR : Set of expected functions does not match the set of circuit outputs.")
                exit(1)

        for fn in fns:
            outName, fnExpr = fn
            # Try to match the function to expected functions
            if outName in expectedFns:
                mapping = bool_map(expectedFns[outName], fnExpr)
                if (mapping is None) or (mapping is False):
                    print(outName, "\tERROR")
                    err = True
                else:
                    print(outName, "\tMATCH")
            else:
                print("ERROR : No expected function is given for the output", outName)
                err = True
        if err:
            print("ERROR : Some Boolean functions were not matched.")
            exit(1)
        else:
            print("ALL OK")

