from glow_utils.ngspice import Ngspice

libs = [ ('$PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib', 'mos_tt') ]
inc = []
conditions = { 'supplyVoltage' : 1.2, 'temperature' : 27.0 }

verbose = False
ng = Ngspice(libs, inc, conditions, verbose=verbose)

netlist = '$GLOW_ROOT/cells/NAND2_D1/NAND2_D1.sp'
circuit = 'NAND2_D1'

print("Reading netlist :", netlist)
print("Simulating      :", circuit)

inputs, inputVals, outputs, outputVals = ng.combSim(netlist, circuit)

print("Simulated truth table")
for name in inputs:
    print(f"{name:<4}", end="")
for name in outputs:
    print(f"{name:<4}", end="")
print("")
for i in range(len(inputVals)):
    row = inputVals[i]
    for val in row:
        print(f"{str(val):<4}", end="")
    row = outputVals[i]
    for val in row:
        print(f"{str(val):<4}", end="")
    print("")



