from glow_utils.ngspice import Ngspice

libs = [ ('$PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib', 'mos_tt') ]
inc = []
conditions = { 'supplyVoltage' : 1.2, 'temperature' : 27.0 }

verbose = False
netlist = '$GLOW_ROOT/cells/NAND2_D1/NAND2_D1.sp'
circuit = 'NAND2_D1'

ng = Ngspice(libs, inc, conditions, netlist, circuit, verbose=verbose)

print("Reading netlist :", netlist)
print("Simulating      :", circuit)

inputs, inputVals, outputs, outputVals, pleak = ng.combSimLeakagePower()

print("Simulated leakage power")
for name in inputs:
    print(f"{name:<6}", end="")
for name in outputs:
    print(f"{name:<6}", end="")
print("P [W]")
for i in range(len(inputVals)):
    row = inputVals[i]
    for val in row:
        print(f"{str(round(val,2)):<6}", end="")
    row = outputVals[i]
    for val in row:
        print(f"{str(round(val,2)):<6}", end="")
    print(str(pleak[i]))

