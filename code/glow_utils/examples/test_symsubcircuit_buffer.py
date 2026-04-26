
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS

inv_par = Symsubcircuit("inv_par", ['A', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})

n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'WN', 'l' : 'L', 'ng' : 'NGN'})
p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'WP', 'l' : 'L', 'ng' : 'NGP'})
inv_par.addElement([n, p])

buff_par = Symsubcircuit("buff_par", ['A', 'Y', 'VDD', 'VSS', ], {'WN' : 1e-6, 'WP' : 2e-6, 'NGN' : 2, 'NGP' : 2})

inv1 = inv_par("inv1", ['A', 'net1', 'VDD', 'VSS'], {'WN' : 1e-6, 'WP' : 1.5e-6, 'NGN' : 2, 'NGP' : 2, 'L' : 130e-9})
inv2 = inv_par("inv2", ['net1', 'Y', 'VDD', 'VSS'], {'WN' : 2e-6, 'WP' : 3e-6, 'NGN' : 4, 'NGP' : 4, 'L' : 130e-9})
buff_par.addElement([inv1, inv2])

print("List of defined subcircuits :")
for name in Symsubcircuit.getSubckts().keys():
    print("\t", name)

print("*" * 40)
print(buff_par.info())
print("*" * 40)

buff1 = buff_par('buf1', ['in', 'out', 'vdd', 'vss'])
print(buff1.to_SPICE(False))

flat_buff1 = buff1.flatten()
print(flat_buff1.netlist_SPICE())
