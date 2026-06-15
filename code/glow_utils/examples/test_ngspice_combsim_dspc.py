from glow_utils.ngspice import Ngspice

libs = [ ('$PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib', 'mos_tt') ]
inc = []
conditions = { 'supplyVoltage' : 1.2, 'temperature' : 27.0 }

verbose = True

netlist = '$GLOW_ROOT/cells/NAND2_D1/NAND2_D1.sp'
circuit = 'NAND2_D1'

ng = Ngspice(libs, inc, conditions, netlist, circuit, verbose=verbose)

print("Reading netlist :", netlist)
print("Simulating      :", circuit)

simSetup = {    'constantInputs' : [('B', True)],
                'input' : ('A', 'negative'),
                'output' : 'Y',
                'capList' : [1e-15, 10e-15, 50e-15, 100e-15, 500e-15, 1e-12],
                'slewList' : [50e-12, 100e-12, 200e-12, 500e-12, 800e-12, 1200e-12]
            }

print(ng.combSimDelaySlewPowerCin(simSetup))

# print("Simulated leakage power")
# for name in inputs:
#     print(f"{name:<6}", end="")
# for name in outputs:
#     print(f"{name:<6}", end="")
# print("P [W]")
# for i in range(len(inputVals)):
#     row = inputVals[i]
#     for val in row:
#         print(f"{str(round(val,2)):<6}", end="")
#     row = outputVals[i]
#     for val in row:
#         print(f"{str(round(val,2)):<6}", end="")
#     print(str(pleak[i]))

