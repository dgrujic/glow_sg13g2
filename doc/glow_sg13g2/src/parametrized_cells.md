# Parametrized cells

Most digital gates can be constructed from few elementary gates that are commonly occurring.
Constructing complex gates from elementary gates is a good practice because it reduces complexity, or equivalently improves readability, and perhaps more importantly captures the design intent.

Preserving design intent is important for understanding the circuit operation, transistor sizing, help with optimizing the layout.
Furthermore, porting to a different process is easier when a higher level description is available, and the role and design intent of each transistor is clear.

Commonly used cells are made as parametrized Python cells, called `parcells`,  and are collected in the module `glow_parcells`.
All parametrized cells can be imported with the following code:

```python
from glow_parcells import *
```
Parametrized cells can be instantiated with desired parameter values and used to construct complex gates.

## `inv_par`

Cell `inv_par` is a parametrized inverter.

Schematic of the `inv_par` cell is given in the following figure.

![inv_par schematic](figs/inv_par_sch.svg)

Symbol of the `inv_par` cell is given in the following figure.

![inv_par symbol](figs/inv_par_sym.svg)

Pins of the `inv_par` cell are listed in the following table.
| Pin | Description |
| :-------: | :--------- |
| `A`       | Inverter input. |
| `Y`       | Inverter output. |
| `VDD`     | Power supply. Not shown in the symbol. |
| `VSS`     | Ground. Not shown in the symbol. |

Parameters of the `inv_par` cell are given in the following table.

| Parameter | Description |
| :-------: | :--------- |
| `WN`      | Total width of NMOS transistor. Default 300 nm. |
| `NGN`     | Number of gates of NMOS transistor. Default 1. |
| `WP`      | Total width of PMOS transistor. Default 450 nm. |
| `NGP`     | Number of gates of PMOS transistor. Default 1. |
| `L`       | Channel length. Default 130 nm. |

SPICE netlist of the `inv_par` cell is:
```
.subckt inv_par A Y VDD VSS WN=3e-07 WP=4.5e-07 L=1.3e-07 NGN=1 NGP=1
XMN0 Y A VSS VSS sg13_lv_nmos w={WN} l={L} ad={WN*3.1e-07} as={WN*3.1e-07} pd={2*(WN+3.1e-07)} ps={2*(WN+3.1e-07)} ng={NGN}
XMP0 Y A VDD VDD sg13_lv_pmos w={WP} l={L} ad={WP*3.1e-07} as={WP*3.1e-07} pd={2*(WP+3.1e-07)} ps={2*(WP+3.1e-07)} ng={NGP}
.ends
```

## `invz_par` and `invz2_par`

Cell `invz_par` is a parametrized inverter with tri-state output.

Schematic of the `invz_par` cell is given in the following figure.

![invz_par schematic](figs/invz_par_sch.svg)

Symbol of the `invz_par` cell is given in the following figure.

![invz_par symbol](figs/invz_par_sym.svg)

Pins of the `invz_par` cell are listed in the following table.
| Pin | Description |
| :-------: | :--------- |
| `A`       | Inverter input. |
| `Y`       | Inverter output. |
| `EN`      | Output enable, active high. |
| `ENB`     | Output enable, active low. |
| `VDD`     | Power supply. Not shown in the symbol. |
| `VSS`     | Ground. Not shown in the symbol. |

Parameters of the `invz_par` cell are given in the following table.

| Parameter | Description |
| :-------: | :--------- |
| `WN`      | Total width of NMOS transistor. Default 300 nm. |
| `NGN`     | Number of gates of NMOS transistor. Default 1. |
| `WP`      | Total width of PMOS transistor. Default 450 nm. |
| `NGP`     | Number of gates of PMOS transistor. Default 1. |
| `L`       | Channel length. Default 130 nm. |
| `WEAK`    | Flag to indicate that output is weak and its output can be changed by other circuits. Used in memory elements. |

SPICE netlist of the `invz_par` cell is:
```
.subckt invz_par A EN ENB Y VDD VSS WN=3e-07 WP=4.5e-07 L=1.3e-07 NGN=1 NGP=1 WEAK=0
XMN0 Y EN net0 VSS sg13_lv_nmos w={WN} l={L} ad={WN*3.1e-07} as={WN*3.1e-07} pd={2*(WN+3.1e-07)} ps={2*(WN+3.1e-07)} ng={NGN} 
XMN1 net0 A VSS VSS sg13_lv_nmos w={WN} l={L} ad={WN*3.1e-07} as={WN*3.1e-07} pd={2*(WN+3.1e-07)} ps={2*(WN+3.1e-07)} ng={NGN} 
XMP0 Y ENB net1 VDD sg13_lv_pmos w={WP} l={L} ad={WP*3.1e-07} as={WP*3.1e-07} pd={2*(WP+3.1e-07)} ps={2*(WP+3.1e-07)} ng={NGP} 
XMP1 net1 A VDD VDD sg13_lv_pmos w={WP} l={L} ad={WP*3.1e-07} as={WP*3.1e-07} pd={2*(WP+3.1e-07)} ps={2*(WP+3.1e-07)} ng={NGP} 
.ends
```

Cell `invz2_par` is equivalent to `invz_par` but with inputs assigned to different series transistors. It is provided to allow for layout optimization while preserving equivalent logic function.

SPICE netlist of the `invz2_par` cell is:
```
.subckt invz2_par A EN ENB Y VDD VSS WN=3e-07 WP=4.5e-07 L=1.3e-07 NGN=1 NGP=1 WEAK=0
XMN0 Y A net0 VSS sg13_lv_nmos w={WN} l={L} ad={WN*3.1e-07} as={WN*3.1e-07} pd={2*(WN+3.1e-07)} ps={2*(WN+3.1e-07)} ng={NGN} 
XMN1 net0 EN VSS VSS sg13_lv_nmos w={WN} l={L} ad={WN*3.1e-07} as={WN*3.1e-07} pd={2*(WN+3.1e-07)} ps={2*(WN+3.1e-07)} ng={NGN} 
XMP0 Y A net1 VDD sg13_lv_pmos w={WP} l={L} ad={WP*3.1e-07} as={WP*3.1e-07} pd={2*(WP+3.1e-07)} ps={2*(WP+3.1e-07)} ng={NGP} 
XMP1 net1 ENB VDD VDD sg13_lv_pmos w={WP} l={L} ad={WP*3.1e-07} as={WP*3.1e-07} pd={2*(WP+3.1e-07)} ps={2*(WP+3.1e-07)} ng={NGP} 
.ends
```
