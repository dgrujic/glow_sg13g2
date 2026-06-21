from glow_utils.ngspice import Ngspice
from tabulate import tabulate


libs = [ ('$PDK_ROOT/$PDK/libs.tech/ngspice/models/cornerMOSlv.lib', 'mos_tt') ]
inc = []
conditions = { 'supplyVoltage' : 1.2, 'temperature' : 27.0 }

verbose = False
netlist = '$GLOW_ROOT/cells/DFQQN_D1/DFQQN_D1.sp'
circuit = 'DFQQN_D1'

ng = Ngspice(libs, inc, conditions, netlist, circuit, verbose=verbose)

print("Reading netlist :", netlist)
print("Simulating      :", circuit)

simSetup = {    'constantInputs' : [],
                'input' : ('D', 'positive'),
                'clk' : ('CLK', 'positive'),
                'output' : 'Q',
                'edge' : 'rising',
                "adjust_slew" :   False,
                "max_iter"    :   20,
                'dSlewList' : [100e-12, 1000e-12],
                'clkSlewList' : [100e-12, 1000e-12]
            }
print("Rising edge hold")
names, values =  ng.dffHold(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))

simSetup = {    'constantInputs' : [],
                'input' : ('D', 'positive'),
                'clk' : ('CLK', 'positive'),
                'output' : 'Q',
                'edge' : 'falling',
                "adjust_slew" :   False,
                'dSlewList' : [100e-12, 1000e-12],
                'clkSlewList' : [100e-12, 1000e-12]
            }
print("Falling edge hold")
names, values =  ng.dffHold(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))

simSetup = {    'constantInputs' : [],
                'input' : ('D', 'negative'),
                'clk' : ('CLK', 'positive'),
                'output' : 'QN',
                'edge' : 'rising',
                'dSlewList' : [100e-12, 1000e-12],
                'clkSlewList' : [100e-12, 1000e-12]
            }
print("Rising edge hold - QN")
names, values =  ng.dffHold(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))

simSetup = {    'constantInputs' : [],
                'input' : ('D', 'negative'),
                'clk' : ('CLK', 'positive'),
                'output' : 'QN',
                'edge' : 'falling',
                'dSlewList' : [100e-12, 1000e-12],
                'clkSlewList' : [100e-12, 1000e-12]
            }
print("Falling edge hold - QN")
names, values =  ng.dffHold(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))
