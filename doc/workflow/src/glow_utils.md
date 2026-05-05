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
MN0 Y A VSS VSS sg13g2_lvnmos w={WN} l={L} ad={WN*3.1e-07} as={WN*3.1e-07} pd={2*(WN+3.1e-07)} ps={2*(WN+3.1e-07)} ng={NGN}
MP0 Y A VDD VDD sg13g2_lvpmos w={WP} l={L} ad={WP*3.1e-07} as={WP*3.1e-07} pd={2*(WP+3.1e-07)} ps={2*(WP+3.1e-07)} ng={NGP}
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
MN0 Y A VSS VSS sg13g2_lvnmos w={WN} l={L} ad={WN*3.1e-07} as={WN*3.1e-07} pd={2*(WN+3.1e-07)} ps={2*(WN+3.1e-07)}
MP0 Y A VDD VDD sg13g2_lvpmos w={WP} l={L} ad={WP*3.1e-07} as={WP*3.1e-07} pd={2*(WP+3.1e-07)} ps={2*(WP+3.1e-07)}
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

Symtech class is intended to be a container of all relevant technology information, so that the rest of the `glow_utils` classes can be used with any technology.
Technology information is stored in a dictionary, that can be read from JSON file.
For example, JSON file for IHP SG13G2 technology is:
```json
{
    "processName" : "sg13g2",
    "nmosModelName" : "sg13g2_lvnmos",
    "pmosModelName" : "sg13g2_lvpmos",
    "nmosAS" : "ipar('w') * 310e-9",
    "nmosAD" : "ipar('w') * 310e-9",
    "nmosPS" : "2 * (ipar('w') + 310e-9)",
    "nmosPD" : "2 * (ipar('w') + 310e-9)",
    "pmosAS" : "ipar('w') * 310e-9",
    "pmosAD" : "ipar('w') * 310e-9",
    "pmosPS" : "2 * (ipar('w') + 310e-9)",
    "pmosPD" : "2 * (ipar('w') + 310e-9)"
}
```
Predefined key names are given in the following table.
|Key           | Description          |
|--------------|----------------------|
|processName   | Name of technology.  |
|nmosModelName | Name of NMOS transistor model.  |
|pmosModelName | Name of PMOS transistor model.  |
|nmosAS        | Expression to calculate NMOS source diffusion area. |
|nmosAD        | Expression to calculate NMOS drain diffusion area. |
|pmosAS        | Expression to calculate PMOS source diffusion area. |
|pmosAD        | Expression to calculate PMOS drain diffusion area. |
|nmosPS        | Expression to calculate NMOS source diffusion perimeter. |
|nmosPD        | Expression to calculate NMOS drain diffusion perimeter. |
|pmosPS        | Expression to calculate PMOS source diffusion perimeter. |
|pmosPD        | Expression to calculate PMOS drain diffusion perimeter. |

Function `ipar` used in expressions is defined in the [Symdevice](#symdevice-class) class.

New keys can be added to JSON file and used to expand or add new functionalities.
Unused keys in JSON file will be ignored.

## Symdict class

Symdict is a sub-class of Python `dict` to allow hierarchical parameter evaluation. 
It is mainly used internally in other classes to build hierarchy of circuit parameters.
Dictionary keys and values are evaluated in a hierarchical manner,
where keys and values defined in local dictionary take precedence over upper levels.

For example:
```python
from glow_utils.symdict import Symdict
topDict = { 'x':1, 'y':2 }
level1Dict = Symdict( topDict, localDict={'x':5 } )
print(level1Dict['x'])
# 5
```
`level1Dict['x']` evaluates to 5 instead of 1, since the local parameter value of `x` takes precedence over the global value.
The same principle applies for any depth of dictionary hierarchy.
If the key in not defined in any dictionary, a KeyError exception is raised, as in a regular Python `dict`.

## Symparam class

Symparam class is used to evaluate symbolic parameter expressions.
Symbolic expressions can be expanded by substitution so that resulting expression contains only symbols that evaluate to numbers or are not defined. Alternatively, symbolic expressions can be evaluated to get a numeric value.
When `Symparam` is used with `Symdict`, it provides means for hierarchical evaluation of expressions, either to symbolic expression or numerical value, and is mainly used internally by other classes.

`Symparam` constructor takes two arguments, a dictionary of parameters `paramDict` and a dictionary of functions `fnDict`:
```python
evaluator = Symparam(paramDict, fnDict)
```
Instance `evaluator` of `Symparam` uses provided `paramDict` and `fnDict` to substitute or evaluate symbolic expressions.
Method `substitute` performs symbolic substitution on a given expression and results in a symbolic expression.
```python
def substitute(self, paramExpr, instanceFns = {}, allowSymbols = False):
```
Argument `paramExpr` is a string containing an expression to work on.
Optional argument `instanceFns` allows for additional, e.g. per-instance defined, functions that are not defined in `fnDict`.
Optional argument `allowSymbols` controls the behavior of symbolic substitution. If `allowSymbols = False` an exception is raised if a symbol is not defined - it does not expand to other symbols nor does it have a numerical value. If `allowSymbols = True` the substitution stops when a symbol is not defined, without raising an exception.

For example, substitution on expression `x + y` can be performed as:
```python
evaluator.substitute('x + y') # Result is a symbolic expression
```

Method `evaluate` performs symbolic substitution and evaluates a given expression to a number.
```python
def evaluate(self, paramExpr, instanceFns = {}):
```
Argument `paramExpr` is a string containing an expression to work on.
Optional argument `instanceFns` allows for additional, e.g. per-instance defined, functions that are not defined in `fnDict`.
Method `evaluate` tries to evaluate an expression to a number, and raises an exception if it can't be done - e.g. a symbol does not evaluate to number for available parameter and function dictionaries.

For example, evaluation of expression `x + y` can be performed as:
```python
evaluator.evaluate('x + y') # Result is a number
```

A complete example of `Symparam` basic use is given in the code below:
```python
from glow_utils.symparam import Symparam

values = {  'x' : 'a+b',
            'y' : 'c',
            'a' : 1,
            'b' : 2,
            'c' : 3}

params = Symparam(values, {})
expression = 'x * y'
print('Dictionary')
print(values)
print('Expression')
print(expression)
print('Expression after substitution')
print(params.substitute( expression ))
print('Expression numeric value')
print(params.evaluate( expression ))
```
The output of the previous Python code is
```
Dictionary
{'x': 'a+b', 'y': 'c', 'a': 1, 'b': 2, 'c': 3}
Expression
x * y
Expression after substitution
(a+b)*c
Expression numeric value
9
```

## Symdevice class

`Symdevice` is base class for devices, and it provides common functions that device should implement.
It should be used as a base class when implementing device models.

Excerpt from `Symdevice` code shows the minimum device constructor:
```python
class Symdevice(object):
    """
    Circuit element base class
    """
    deviceType = "unspecified"
    modelName = "symdevice"
    modelPrefix = "unspecified"
    terminals = []

    def __init__(self, name, nodes, parameters):
        self.name = name
        self.nodes = nodes
        self.parameters = parameters
        self.parameterEvaluator = None  # Symparam instance
        self.functions = {"ipar" : self.ipar}
        self.initInstance()
```
Class variables `deviceType`, `modelName`, `modelPrefix` and `terminals` are common for all instances of a given device class.

Class variable `deviceType` is a string indicating a device type - currently only `"nmos"` and `"pmos"` devices are implemented.

Class variable `modelName` contains a name of SPICE device model that is used as a model in SPICE and CDL netlists.

Class variable `modelPrefix` is a string that is used as a name prefix.

Class variable `terminals` is a list of device terminal names. The order of terminals in the list should match the order of terminals in SPICE models.

Device instance is created by making an instance of device class:
```python
dev_inst = dev_cls("inst_name", ['net1', 'net2', 'net3', 'net4'], {'w' : 400e-9, 'l' : 130e-9})
```
Instance `dev_inst` is given a name `inst_name`, and its terminals are connected to nodes `['net1', 'net2', 'net3', 'net4']`, and assigned parameter values `'w' = 400e-9` and `'l' = 130e-9`. Assigned parameter instance values override the default device parameters.

### SymMOSFET class

`SymMOSFET` is a base class for creating MOSFET devices. 
It defines terminal names, their order and SPICE/CDL output formatting, and is used to construct NMOS and PMOS device classes.

MOSFET terminals are assinged as `['D', 'G', 'S', 'B']`

`SymMOSFET` defines the following device parameters:
| Parameter | Description |
|-----------|-------------|
| m         | Device multiplier. |
| w         | MOSFET channel width. |
| l         | MOSFET channel length. |
| ad        | Drain diffusion area. |
| as        | Source diffusion area. |
| pd        | Drain diffusion perimeter. |
| ps        | Source diffusion perimeter. |
| nrd       | Drain diffusion equivalent number of squares. |
| nrs       | Source diffusion equivalent number of squares. |
| ng        | Number of gates (fingers). |

These parameters are common to many MOSFET models, and `SymMOSFET` can be used without modification with them.

### SymNMOS and SymPMOS

`SymNMOS` and `SymPMOS` extend the `SymMOSFET` class by assigning the device type, model name and model prefix.
They can be used to construct CMOS circuits with parametrized values.
Value parametrization is useful in at least two ways: it provides a way of using standard building blocks to construct complex circuits, and also to capture the design intent by explicitly stating transistor ratios.

NMOS and PMOS devices can be instantiated as
```python
n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'WN', 'l' : 'L'})
p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'WP', 'l' : 'L'})
```
In this example the NMOS and PMOS device have been instantiated with symbolic values for channel width and length. Parameters `ad`, `as`, `ps` and `pd` have the default values, that are taken from technology parameters retrieved from `Symtech`.

For example, default value for parameter `ad` is an expression
```python
"ipar('w') * 310e-9"
```
Function `ipar('w')` evaluates to the value of instance parameter `w`, that is `'WN'` in the previous example. This symbol can be further expanded by substitution and eventually evaluated at the circuit top level.

## Symsubcircuit class

Symsubcircuit is a meta-class used for creating subcircuit classes.
Instances of Symsubcircuit class are not objects, but new classes that represent a specific subcircuit which can be instantiated as objects.

For example, an inverter subcircuit class named `inv_par` with terminals 
`A`, `Y`, `VDD` and `VSS`, and default parameter values `WN = 200e-9`, `WP = 400e-9` and `L = 130e-9` can be created as:
```python
inv_par_cls = subcircuit( 'inv_par', ('A', 'Y', 'VDD', 'VSS'), {'WN':200e-9, 'WP':400e-9, 'L':130e-9} )
```

The newly created subcircuit class, stored in inv_par_cls, can be populated with circuit elements or other subcircuits.

Continuing the inverter example, transistors can be added to subcircuit as:
```python
n0 = SymNMOS('N0', ['Y', 'A', 'VSS', 'VSS'], {'w':'WN'}, {'l':'L'})
p0 = SymNMOS('P0', ['Y', 'A', 'VDD', 'VDD'], {'w':'WP'}, {'l':'L'})
inv_par_cls.addElement( [n0, p0] )
```

`addElement` is a classmethod, so the elements are stored as class variables.
This way, the subcircuit elements are shared amongst all instances of the same subcircuit. 
At this point the created subcircuit class has no instances.
In order to use the subcircuit, it needs to be instantiated:
```python
inv_par_inst = inv_par_cls('instanceName', ('in', 'out', 'VDD', 'VSS'), {'WN':300e-9, 'WP':600e-9})
```
By creating a subcircuit instance, it is given a name, connected to given nodes and optionally default parameters are overridden.
The subcircuit instance can then be added to a other subcircuit to form a hierarchy:
```python
subckt_cls.addElement( inv_par_inst )
```
Function `ipar` can be used to fetch the value of instance parameter, 
and `ipar('parameter_name')` evaluates to the value of instance parameter `'parameter_name'`.
For example, NMOS instance with parameters
```python
{'w': 'WN', 'l': 'L', 
  'as': "ipar('w')*310e-9", 'ad': "ipar('w')*310e-9", 
  'ps': "2*(ipar('w')+310e-9)", 'pd': "2*(ipar('w')+310e-9)"}
```
uses ipar function in expressions for `as`, `ad`, `ps` and `pd`.
In this example, `ipar('w')` evaluates to the value of instance parameter `'w'`, so `ipar('w') = 'WN'`.
Symbolic value `'WN'` can further be evaluated to other expressions or a number, depending on the upper level subcircuit parameters.

Function `ppar` can be used to fetch the value of instance parent, which is usually a subcircuit.
For example, a CMOS inverter
```python
inv_par = Symsubcircuit("inv_par", ['A', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'WP' : 450e-9, 'L' : 130e-9, 'NGN' : 1, 'NGP' : 1})
n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGN")'})
p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : 'ppar("WP")', 'l' : 'ppar("L")', 'ng' : 'ppar("NGP")'})
inv_par.addElement([n, p])
```
uses `ppar` to evaluate the value of `'WN'`, `'L'` and `'NGN'` for a given subcircuit instance.
Continuing the example with two instances of `inv_par` that have different values of parameters:
```python
inv1 = inv_par("inv1", ['A', 'net1', 'VDD', 'VSS'], {'WN' : '1e-6', 'WP' : '2e-6', 'NGN' : 2, 'NGP' : 2, 'L' : 130e-9})
inv2 = inv_par("inv2", ['net1', 'Y', 'VDD', 'VSS'], {'WN' : '1.5e-6', 'WP' : '3e-6', 'NGN' : 4, 'NGP' : 4, 'L' : 130e-9})
```
we have that ppar evaluates to different values in different instances:
```python
inv1:  ppar("WN") = 1e-6
inv2:  ppar("WN") = 2e-6
```
Use of `ppar` enables creation of parametrized hierarchical circuits.

Dictionary of all defined subcircuits can be obtained as
```python
subckt_cls_all = Symsubcircuit.getSubckts()
```
In this example the variable `subckt_cls_all` would be a dictionary with keys that are subcircuit names and values that are references to subcircuit classes that can be used for instance creation.

Subcircuit can be netlisted with `netlist_SPICE` or `netlist_CDL` methods. These methods netlist the subcircuit definition, not a particular instance. 

```python
from glow_utils import *
inv_par = Symsubcircuit("inv_par", ['A', 'Y', 'VDD', 'VSS'], {'WN' : 300e-9, 'L' : 130e-9})
n = SymNMOS("N0", ['Y', 'A', 'VSS', 'VSS'], {'w' : 'ppar("WN")', 'l' : 'ppar("L")'})
p = SymPMOS("P0", ['Y', 'A', 'VDD', 'VDD'], {'w' : '1.5*ppar("WN")', 'l' : 'ppar("L")'})
inv_par.addElement([n, p])

buff_par = Symsubcircuit("buff_par", ['in', 'out', 'VDD', 'VSS'], {'WN' : 1e-6})
inv1 = inv_par("inv1", ['in', 'net1', 'VDD', 'VSS'], {'WN' : 'ppar("WN")'})
inv2 = inv_par("inv2", ['net1', 'out', 'VDD', 'VSS'], {'WN' : '2*ppar("WN")'})
buff_par.addElement([inv1, inv2])
print(buff_par.netlist_SPICE())
```
The output of previous Python code is
```spice
.subckt buff_par in out VDD VSS WN=1e-06
Xinv1 in net1 VDD VSS inv_par WN={WN} 
Xinv2 net1 out VDD VSS inv_par WN={2*WN} 
.ends
```
Subcircuit can be flattened as
```python
flat = buff_par.flat()
print(flat.netlist_SPICE())
```
The flattened circuit netlist is
```spice
.subckt buff_par_flat in out VDD VSS WN=1e-06
Minv1N0 net1 in VSS VSS sg13g2_lvnmos w=1e-06 l=1.3e-07 ad=3.1e-13 as=3.1e-13 pd=2.62e-06 ps=2.62e-06 
Minv1P0 net1 in VDD VDD sg13g2_lvpmos w=1.5e-06 l=1.3e-07 ad=4.65e-13 as=4.65e-13 pd=3.62e-06 ps=3.62e-06 
Minv2N0 out net1 VSS VSS sg13g2_lvnmos w=2e-06 l=1.3e-07 ad=6.2e-13 as=6.2e-13 pd=4.62e-06 ps=4.62e-06 
Minv2P0 out net1 VDD VDD sg13g2_lvpmos w=3e-06 l=1.3e-07 ad=9.3e-13 as=9.3e-13 pd=6.62e-06 ps=6.62e-06 
.ends
```

Device and node names in a flat circuit are built as hierarchical names, concatenating the names of instance names at each level of hierarchy, and can be impractically long.
Subcircuit method `anonimize` can be used to assign short names to devices and nets by assigning them sequential integer names.
Only the nets connecting to subcircuit terminals are not renamed to preserve meaningfull names.
Continuing the buffer example, calling
```python
flat.anonimize()
print(flat.netlist_SPICE())
```
results in
```spice
.subckt buff_par_flat in out VDD VSS WN=1e-06
MN0 n0 in VSS VSS sg13g2_lvnmos w=1e-06 l=1.3e-07 ad=3.1e-13 as=3.1e-13 pd=2.62e-06 ps=2.62e-06 
MP0 n0 in VDD VDD sg13g2_lvpmos w=1.5e-06 l=1.3e-07 ad=4.65e-13 as=4.65e-13 pd=3.62e-06 ps=3.62e-06 
MN1 out n0 VSS VSS sg13g2_lvnmos w=2e-06 l=1.3e-07 ad=6.2e-13 as=6.2e-13 pd=4.62e-06 ps=4.62e-06 
MP1 out n0 VDD VDD sg13g2_lvpmos w=3e-06 l=1.3e-07 ad=9.3e-13 as=9.3e-13 pd=6.62e-06 ps=6.62e-06 
.ends
```

## Symcheck class

