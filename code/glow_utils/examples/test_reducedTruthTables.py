
from glow_utils.symsim import Symsim
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symieee1164 import IEEE1164

circuits = ["NAND4N2_D1", "MUX2_D1", "OAI221_D1"]

for circuit in circuits:
    print("*"*80)
    print('Circuit ' + circuit)
    Symsubcircuit.importCell(circuit)
    circuit = Symsubcircuit.getSubckts()[circuit + "_flat"]
    sim = Symsim(circuit, verbose=False)
    tbls = sim.reducedTruthTables()
    print(sim.formatReducedTruthTables(tbls)[0])
