
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS
from glow_utils.symsim import Symsim
from glow_utils.symieee1164 import IEEE1164
from sympy import bool_map, Nand, Nor
from sympy.abc import x, y

nand2_par = Symsubcircuit("nand2_par", ['A', 'B', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})

n0 = SymNMOS("N0", ['n0', 'A', 'VSS', 'VSS'], {'w' : '2*ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
n1 = SymNMOS("N1", ['Y', 'B', 'n0', 'VSS'], {'w' : '2*ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
p0 = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})
p1 = SymPMOS("P1", ['Y', 'B', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})

nand2_par.addElement([n0, n1, p0, p1])

sim = Symsim(nand2_par)

print("*"*40)
print("Determining gate logic function.")
logicExpr = sim.combFunc()
print("Gate logic function is", logicExpr[0])
if sim.error:
    print("ERROR : There is an error in circuit.")
else:
    print("Circuit is OK")

expectedFn = Nand(x, y)
mapping = bool_map(expectedFn, logicExpr[0])
if mapping is not None:
    print("Circuit function matches the expected Boolean function.")
else:
    print("Circuit function does not match the expected Boolean function.")

# Try to match the circuit function to the wrong Boolean function
wrongFn = Nor(x, y)
mapping = bool_map(wrongFn, logicExpr[0])
if mapping is not None:
    print("Circuit function matches the wrong Boolean function.")
else:
    print("Circuit function does not match the wrong Boolean function.")

