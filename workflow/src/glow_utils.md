# GLOW Utilities

Python package `glow_utils` provides utility functions used for design of digital standard cell library.
Package can be installed with
``` sh
pip install .
```
For development it is convenient to link the Python files to the package installation as
``` sh
pip install -e .
```
so that changes in Python files are immediately available without the need to reinstall the package.

## Quick start

GLOW utilities are designed to aid the development of circuits, specifically digital standard cells. They provide a programmatic way for development of parametrized hierarchical circuits, performing various checks, transformations and exporting to SPICE or CDL netlists.

Minium example of parametrized CMOS inverter is
``` Python
from glow_utils.symsubcircuit import Symsubcircuit
from glow_utils.symmosfet import SymNMOS, SymPMOS

inv_par = Symsubcircuit("inv_par", ['A', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})
n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})
inv_par.addElement([n, p])
print(inv_par.netlist_SPICE())
```
The output of this Python code is
```spice
.subckt inv_par A Y VDD VSS WN=3e-07 WP=4.5e-07 L=1.3e-07 NGN=1 NGP=1
MN0 Y A VSS VSS sg13g2_lvnmos w=WN l=L ad=WN*3.1e-07 as=WN*3.1e-07 pd=2*(WN+3.1e-07) ps=2*(WN+3.1e-07) ng=NGN 
MP0 Y A VDD VDD sg13g2_lvpmos w=WP l=L ad=WP*3.1e-07 as=WP*3.1e-07 pd=2*(WP+3.1e-07) ps=2*(WP+3.1e-07) ng=NGP 
.ends
```
A simple CMOS inverter testbench can be made by creating an instance of the inverter and defining transistor models - in this case a dummy `LEVEL 1` MOSFET model.
```spice
X1 in out vdd 0 inv_par
.model sg13g2_lvnmos NMOS (LEVEL=1 VTO=0.3 KP=50u)
.model sg13g2_lvpmos PMOS (LEVEL=1 VTO=-0.3 KP=20u)
```
What is left is to define voltage sources and simulations
```spice
Vdd vdd 0 1.2
Vin in 0 PULSE(0 1.2 0 1n 1n 10n 20n)
Cl out 0 10f
.tran 0.1n 100n
.control
run
plot v(in) v(out)
.endc
.end
```
Saving the file as `tb_inv.cir` and running a simulation with
```sh
ngspice tb_inv.cir
```
results in an error
```sh
  unknown parameter (ng) 
    Simulation interrupted due to error!
```
This error is a consequence of a chosen inadequate MOSFET model that does not support parameter `ng`, that is supported by target technology. Netlist can be corrected by deleting the extra parameter, and the whole corrected netlist is given in the listing below:
```spice
* CMOS Inverter Testbench
.subckt inv_par A Y VDD VSS WN=3e-07 WP=4.5e-07 L=1.3e-07
MN0 Y A VSS VSS sg13g2_lvnmos w=WN l=L ad=WN*3.1e-07 as=WN*3.1e-07 pd=2*(WN+3.1e-07) ps=2*(WN+3.1e-07)
MP0 Y A VDD VDD sg13g2_lvpmos w=WP l=L ad=WP*3.1e-07 as=WP*3.1e-07 pd=2*(WP+3.1e-07) ps=2*(WP+3.1e-07)
.ends

X1 in out vdd 0 inv_par
.model sg13g2_lvnmos NMOS (LEVEL=1 VTO=0.3 KP=50u)
.model sg13g2_lvpmos PMOS (LEVEL=1 VTO=-0.3 KP=20u)
Vdd vdd 0 1.2
Vin in 0 PULSE(0 1.2 0 1n 1n 10n 20n)
Cl out 0 10f
.tran 0.1n 100n
.control
run
plot v(in) v(out)
.endc
.end
```
This time the simulation runs successfully and the input and output waveforms are displayed.

This simple example shows how to use GLOW utils to design a CMOS inverter, but they can be used for much complex cases.

## Symtech class

## Symdict class

## Symparam class

## Symdevice class

### SymMOSFET class

### SymNMOS and SymPMOS

## Symsubcircuit class

## Symcheck class

