
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS

inv_par = Symsubcircuit("inv_par", ['Ai', 'Yi', 'VDDi', 'VSSi'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})

n = SymNMOS("N0", ['Yi', 'Ai', 'VSSi', 'VSSi'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
p = SymPMOS("P0", ['Yi', 'Ai', 'VDDi', 'VDDi'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})
nn = SymNMOS("Nx", ['Yib', 'Aib', 'VSSi', 'VSSi'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})

inv_par.addElement([n, p, nn])

buff_par = Symsubcircuit("buff_par", ['Ab', 'Yb', 'VDDb', 'VSSb', ], {'WN' : 1e-6, 'WP' : 2e-6, 'NGN' : 2, 'NGP' : 2})

inv1 = inv_par("inv1", ['Ab', 'ni1', 'VDDb', 'VSSb'], {'WN' : '1.5*ppar("WN")', 'WP' : '1.75*ppar("WP")', 'NGN' : 2, 'NGP' : 2, 'L' : 130e-9})
inv2 = inv_par("inv2", ['ni1', 'Yb', 'VDDb', 'VSSb'], {'WN' : '2*ppar("WN")', 'WP' : '2*ppar("WP")', 'NGN' : 4, 'NGP' : 4, 'L' : 130e-9})

buff_par.addElement([inv1, inv2])

buff1 = buff_par('buf1', ['Ax', 'nb1', 'VDDx', 'VSSx'], {'WN' : 1e-6, 'WP' : 2e-6, 'NGN' : 2, 'NGP' : 2})
buff2 = buff_par('buf2', ['nb1', 'Yx', 'VDDx', 'VSSx'], {'WN' : 10e-6, 'WP' : 20e-6, 'NGN' : 20, 'NGP' : 20})

topbuff_par = Symsubcircuit("topbuff_par", ['Ax', 'Yx', 'VDDx', 'VSSx', ], {'WN' : 4e-6, 'WP' : 6e-6, 'NGN' : 8, 'NGP' : 8})
topbuff_par.addElement([buff1, buff2])

topbuff1 = topbuff_par("topbuff1", ['in', 'out', 'vdd', 'vss'] )

print("*"*40)
print(buff1.netlist_SPICE())

print("*"*40)
print(topbuff1.netlist_SPICE())

topbuff1_flat = topbuff1.flatten()
print("*"*40)
print("SPICE netlist")
print(topbuff1_flat.netlist_SPICE())

print("Anonimize devices and nodes")
topbuff1_flat.anonimize()
print("*"*40)
print("Anonimized SPICE netlist")
print(topbuff1_flat.netlist_SPICE())
