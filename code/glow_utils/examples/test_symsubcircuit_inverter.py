
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS

inv_par = Symsubcircuit("inv_par", ['A', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})

print("List of defined subcircuits :")
for name in Symsubcircuit.getSubckts().keys():
    print("\t", name)

n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'WN', 'l' : 'L', 'ng' : 'NGN'})
p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'WP', 'l' : 'L', 'ng' : 'NGP'})
inv_par.addElement([n, p])

print("*" * 40)
print(inv_par.info())
print("*" * 40)
print(inv_par.netlist_SPICE())
