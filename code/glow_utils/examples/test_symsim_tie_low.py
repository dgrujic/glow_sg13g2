
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS
from glow_utils.symsim import Symsim
from glow_utils.symieee1164 import IEEE1164
from sympy import bool_map, Nand, Nor
from sympy.abc import x, y

tie_low_par = Symsubcircuit("tie_low_par", ['Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})

n0 = SymNMOS("N0", ['Y', 'n0', 'VSS', 'VSS'], {'w' : '2*ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
p0 = SymPMOS("P0", ['n0', 'n0', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})

tie_low_par.addElement([n0, p0])

sim = Symsim(tie_low_par)

print("*"*40)
print("Determining gate logic function.")
logicExpr = sim.combFunc()
print("Gate logic function is", logicExpr[0])
if sim.error:
    print("ERROR : There is an error in circuit.")
else:
    print("Circuit is OK")
