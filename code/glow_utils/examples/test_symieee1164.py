
from glow_utils.symieee1164 import IEEE1164
from itertools import combinations_with_replacement

values = [IEEE1164.DONT_CARE, IEEE1164.H, IEEE1164.L, 
          IEEE1164.ONE, IEEE1164.ZERO, IEEE1164.UNDEFINED, 
          IEEE1164.WEAK, IEEE1164.X, IEEE1164.Z]

inputs = list(combinations_with_replacement(values, 2))

for input in inputs:
    x, y = input
    res = IEEE1164.resolve(x, y)
    print(x.value, "|", y.value, "|", res.value)


