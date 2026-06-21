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
                'adjust_slew' :   False,
                'tran_sim_step' :   10e-12,
                'coutList' : [1e-15, 20e-15, 40e-15, 100e-15],
                'clkSlewList' : [100e-12, 400e-12, 800e-12]
            }

print("Arc CLK -> Q\tRISE -> RISE")
names, values = ng.dffClkToOut(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))


simSetup = {    'constantInputs' : [],
                'input' : ('D', 'positive'),
                'clk' : ('CLK', 'positive'),
                'output' : 'Q',
                'edge' : 'falling',
                'adjust_slew' :   False,
                'tran_sim_step' :   10e-12,
                'coutList' : [1e-15, 20e-15, 40e-15, 100e-15],
                'clkSlewList' : [100e-12, 400e-12, 800e-12]
            }

print("Arc CLK -> Q\tRISE -> FALL")
names, values = ng.dffClkToOut(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))


simSetup = {    'constantInputs' : [],
                'input' : ('D', 'negative'),
                'clk' : ('CLK', 'positive'),
                'output' : 'QN',
                'edge' : 'rising',
                'adjust_slew' :   False,
                'tran_sim_step' :   10e-12,
                'coutList' : [1e-15, 20e-15, 40e-15, 100e-15],
                'clkSlewList' : [100e-12, 400e-12, 800e-12]
            }

print("Arc CLK -> QN\tRISE -> RISE")
names, values = ng.dffClkToOut(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))


simSetup = {    'constantInputs' : [],
                'input' : ('D', 'negative'),
                'clk' : ('CLK', 'positive'),
                'output' : 'QN',
                'edge' : 'falling',
                'adjust_slew' :   False,
                'tran_sim_step' :   10e-12,
                'coutList' : [1e-15, 20e-15, 40e-15, 100e-15],
                'clkSlewList' : [100e-12, 400e-12, 800e-12]
            }

print("Arc CLK -> QN\tRISE -> FALL")
names, values = ng.dffClkToOut(simSetup)
print(tabulate(values, headers=names, tablefmt='grid'))


