# AOI2N1

Inverted output AND-OR gate with two inverted AND inputs and one direct OR input. Eqivalent to OR-AND gate with inverted direct OR input.

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| A | Input A, inverted and connected to AND gate |
| B | Input B, inverted and connected to AND gate |
| C | Input C, direct input to OR gate |
| Y | Output |
| VDD | Power supply |
| VSS | Ground |


## Logic function and Truth table

### Logic function (Python)
<div align="center">
Y = ~((~A & ~B) | C)
</div>

### Logic function (Boolean)
\\[ Y = \overline{(\overline{A} \cdot \overline{B}) + C} \\]

### Truth Table for Y


| A | B | C | Y |
| :--- | :--- | :--- | :--- |
| 1 | - | 0 | 1 | 
| - | 1 | 0 | 1 | 
| - | - | 1 | 0 | 
| 0 | 0 | - | 0 | 


## Symbol

<div align="center">
<img src="figs/AOI2N1_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/AOI2N1_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [AOI2N1_DL](#aoi2n1_dl) | TBD | TBD |
| [AOI2N1_D1](#aoi2n1_d1) | TBD | TBD |
| [AOI2N1_D2](#aoi2n1_d2) | TBD | TBD |



### AOI2N1_DL

#### Hierarchical SPICE netlist
```spice
.subckt AOI2N1_DL A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad={1.5e-07*3.1e-07} as={1.5e-07*3.1e-07} pd={2*(1.5e-07+3.1e-07)} ps={2*(1.5e-07+3.1e-07)} 
XMN1 n0 B VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad={1.5e-07*3.1e-07} as={1.5e-07*3.1e-07} pd={2*(1.5e-07+3.1e-07)} ps={2*(1.5e-07+3.1e-07)} 
XMN2 Y n0 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad={3.2e-07*3.1e-07} as={3.2e-07*3.1e-07} pd={2*(3.2e-07+3.1e-07)} ps={2*(3.2e-07+3.1e-07)} 
XMN3 Y C VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad={3.2e-07*3.1e-07} as={3.2e-07*3.1e-07} pd={2*(3.2e-07+3.1e-07)} ps={2*(3.2e-07+3.1e-07)} 
XMP0 n1 A VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad={3e-07*3.1e-07} as={3e-07*3.1e-07} pd={2*(3e-07+3.1e-07)} ps={2*(3e-07+3.1e-07)} 
XMP1 n1 B n0 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad={3e-07*3.1e-07} as={3e-07*3.1e-07} pd={2*(3e-07+3.1e-07)} ps={2*(3e-07+3.1e-07)} 
XMP2 Y C n2 VDD sg13_lv_pmos w=6.4e-07 l=1.3e-07 ad={6.4e-07*3.1e-07} as={6.4e-07*3.1e-07} pd={2*(6.4e-07+3.1e-07)} ps={2*(6.4e-07+3.1e-07)} 
XMP3 n2 n0 VDD VDD sg13_lv_pmos w=6.4e-07 l=1.3e-07 ad={6.4e-07*3.1e-07} as={6.4e-07*3.1e-07} pd={2*(6.4e-07+3.1e-07)} ps={2*(6.4e-07+3.1e-07)} 
.ends
```

#### Flat SPICE netlist
```spice
.subckt AOI2N1_DL A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 
XMN1 n0 B VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 
XMN2 Y n0 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad=9.92e-14 as=9.92e-14 pd=1.26e-06 ps=1.26e-06 
XMN3 Y C VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad=9.92e-14 as=9.92e-14 pd=1.26e-06 ps=1.26e-06 
XMP0 n1 A VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 
XMP1 n1 B n0 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 
XMP2 Y C n2 VDD sg13_lv_pmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
XMP3 n2 n0 VDD VDD sg13_lv_pmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
.ends
```

#### CDL netlist
```cdl
.SUBCKT AOI2N1_DL A B C Y VDD VSS
*.PININFO C:I B:I A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 
MN1 n0 B VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 
MN2 Y n0 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 
MN3 Y C VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 
MP0 n1 A VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 
MP1 n1 B n0 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 
MP2 Y C n2 VDD sg13_lv_pmos w=6.4e-07 l=1.3e-07 
MP3 n2 n0 VDD VDD sg13_lv_pmos w=6.4e-07 l=1.3e-07 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### AOI2N1_D1

#### Hierarchical SPICE netlist
```spice
.subckt AOI2N1_D1 A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad={2.5e-07*3.1e-07} as={2.5e-07*3.1e-07} pd={2*(2.5e-07+3.1e-07)} ps={2*(2.5e-07+3.1e-07)} 
XMN1 n0 B VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad={2.5e-07*3.1e-07} as={2.5e-07*3.1e-07} pd={2*(2.5e-07+3.1e-07)} ps={2*(2.5e-07+3.1e-07)} 
XMN2 Y n0 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad={6.4e-07*3.1e-07} as={6.4e-07*3.1e-07} pd={2*(6.4e-07+3.1e-07)} ps={2*(6.4e-07+3.1e-07)} 
XMN3 Y C VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad={6.4e-07*3.1e-07} as={6.4e-07*3.1e-07} pd={2*(6.4e-07+3.1e-07)} ps={2*(6.4e-07+3.1e-07)} 
XMP0 n1 A VDD VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad={5e-07*3.1e-07} as={5e-07*3.1e-07} pd={2*(5e-07+3.1e-07)} ps={2*(5e-07+3.1e-07)} 
XMP1 n1 B n0 VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad={5e-07*3.1e-07} as={5e-07*3.1e-07} pd={2*(5e-07+3.1e-07)} ps={2*(5e-07+3.1e-07)} 
XMP2 Y C n2 VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad={1.28e-06*3.1e-07} as={1.28e-06*3.1e-07} pd={2*(1.28e-06+3.1e-07)} ps={2*(1.28e-06+3.1e-07)} 
XMP3 n2 n0 VDD VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad={1.28e-06*3.1e-07} as={1.28e-06*3.1e-07} pd={2*(1.28e-06+3.1e-07)} ps={2*(1.28e-06+3.1e-07)} 
.ends
```

#### Flat SPICE netlist
```spice
.subckt AOI2N1_D1 A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 
XMN1 n0 B VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 
XMN2 Y n0 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
XMN3 Y C VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
XMP0 n1 A VDD VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 
XMP1 n1 B n0 VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 
XMP2 Y C n2 VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad=3.968e-13 as=3.968e-13 pd=3.18e-06 ps=3.18e-06 
XMP3 n2 n0 VDD VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad=3.968e-13 as=3.968e-13 pd=3.18e-06 ps=3.18e-06 
.ends
```

#### CDL netlist
```cdl
.SUBCKT AOI2N1_D1 A B C Y VDD VSS
*.PININFO C:I B:I A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 
MN1 n0 B VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 
MN2 Y n0 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 
MN3 Y C VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 
MP0 n1 A VDD VDD sg13_lv_pmos w=5e-07 l=1.3e-07 
MP1 n1 B n0 VDD sg13_lv_pmos w=5e-07 l=1.3e-07 
MP2 Y C n2 VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 
MP3 n2 n0 VDD VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### AOI2N1_D2

#### Hierarchical SPICE netlist
```spice
.subckt AOI2N1_D2 A B C Y VDD VSS
XAOI2N1_1 A B C Y VDD VSS AOI2N1_D1 
XAOI2N1_2 A B C Y VDD VSS AOI2N1_D1 
.ends
```

#### Flat SPICE netlist
```spice
.subckt AOI2N1_D2 A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 
XMN1 n0 B VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 
XMN2 Y n0 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
XMN3 Y C VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
XMP0 n1 A VDD VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 
XMP1 n1 B n0 VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 
XMP2 Y C n2 VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad=3.968e-13 as=3.968e-13 pd=3.18e-06 ps=3.18e-06 
XMP3 n2 n0 VDD VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad=3.968e-13 as=3.968e-13 pd=3.18e-06 ps=3.18e-06 
XMN4 n3 A VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 
XMN5 n3 B VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 
XMN6 Y n3 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
XMN7 Y C VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 
XMP4 n4 A VDD VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 
XMP5 n4 B n3 VDD sg13_lv_pmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 
XMP6 Y C n5 VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad=3.968e-13 as=3.968e-13 pd=3.18e-06 ps=3.18e-06 
XMP7 n5 n3 VDD VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 ad=3.968e-13 as=3.968e-13 pd=3.18e-06 ps=3.18e-06 
.ends
```

#### CDL netlist
```cdl
.SUBCKT AOI2N1_D2 A B C Y VDD VSS
*.PININFO C:I B:I A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 
MN1 n0 B VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 
MN2 Y n0 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 
MN3 Y C VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 
MP0 n1 A VDD VDD sg13_lv_pmos w=5e-07 l=1.3e-07 
MP1 n1 B n0 VDD sg13_lv_pmos w=5e-07 l=1.3e-07 
MP2 Y C n2 VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 
MP3 n2 n0 VDD VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 
MN4 n3 A VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 
MN5 n3 B VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 
MN6 Y n3 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 
MN7 Y C VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 
MP4 n4 A VDD VDD sg13_lv_pmos w=5e-07 l=1.3e-07 
MP5 n4 B n3 VDD sg13_lv_pmos w=5e-07 l=1.3e-07 
MP6 Y C n5 VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 
MP7 n5 n3 VDD VDD sg13_lv_pmos w=1.28e-06 l=1.3e-07 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

## Pin capacitance
No pin capacitance data


## Static power
No static power data


## Dynamic power
No dynamic power data


## Delay
No delay data

