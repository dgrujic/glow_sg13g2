
from symmosfet import SymNMOS, SymPMOS
from symparam import Symparam

n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'WN', 'l' : 'L'})
p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'WP', 'l' : 'L'})

print("NMOS info")
print(n)
print("PMOS info")
print(p)

paramValues = {'WN' : 400e-9, 'WP' : 600e-9, 'L' : 130e-9}
paramEvaluator = Symparam(paramValues, {})

n.setParameterEvaluator(paramEvaluator)
p.setParameterEvaluator(paramEvaluator)

n.evaluateInstanceParameters()
p.evaluateInstanceParameters()

print("NMOS info with evaluated parameters")
print(n)
print("PMOS info with evaluated parameters")
print(p)

print("NMOS SPICE line")
print(n.to_SPICE())
print("PMOS SPICE line")
print(p.to_SPICE())