# NAND4

Four input NAND gate

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| A | Input A |
| B | Input B |
| C | Input C |
| D | Input D |
| Y | Output |
| VDD | Power supply |
| VSS | Ground |


## Logic function and Truth table

### Logic function (Python)
<div align="center">
Y = ~(A & B & C & D)
</div>

### Logic function (Boolean)
\\[ Y = \overline{A \cdot B \cdot C \cdot D} \\]

### Truth Table for Y


| A | B | C | D | Y |
| :--- | :--- | :--- | :--- | :--- |
| 0 | - | - | - | 1 | 
| - | 0 | - | - | 1 | 
| - | - | 0 | - | 1 | 
| - | - | - | 0 | 1 | 
| 1 | 1 | 1 | 1 | 0 | 


## Symbol

<div align="center">
<img src="figs/NAND4_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/NAND4_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [NAND4_DL](#nand4_dl) | TBD | TBD |
| [NAND4_D1](#nand4_d1) | TBD | TBD |
| [NAND4_D2](#nand4_d2) | TBD | TBD |
| [NAND4_D4](#nand4_d4) | TBD | TBD |



### NAND4_DL

#### Hierarchical SPICE netlist
```spice
.subckt NAND4_DL A B C D Y VDD VSS
Xnand4 A B C D Y VDD VSS nand4_par WN=4.5e-07 WP=4e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NAND4_DL A B C D Y VDD VSS
XMN0 n0 D VSS VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN1 n1 C n0 VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN2 n2 B n1 VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN3 Y A n2 VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMP0 Y A VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMP1 Y B VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMP2 Y C VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMP3 Y D VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NAND4_DL A B C D Y VDD VSS
*.PININFO A:I B:I C:I D:I Y:O VDD:B VSS:B 
MN0 n0 D VSS VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ng=1 
MN1 n1 C n0 VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ng=1 
MN2 n2 B n1 VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ng=1 
MN3 Y A n2 VSS sg13_lv_nmos w=4.5e-07 l=1.3e-07 ng=1 
MP0 Y A VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ng=1 
MP1 Y B VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ng=1 
MP2 Y C VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ng=1 
MP3 Y D VDD VDD sg13_lv_pmos w=4e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### NAND4_D1

#### Hierarchical SPICE netlist
```spice
.subckt NAND4_D1 A B C D Y VDD VSS
Xnand4 A B C D Y VDD VSS nand4_par 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NAND4_D1 A B C D Y VDD VSS
XMN0 n0 D VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMN1 n1 C n0 VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMN2 n2 B n1 VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMN3 Y A n2 VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMP0 Y A VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ad=2.17e-13 as=2.17e-13 pd=2.02e-06 ps=2.02e-06 ng=1 
XMP1 Y B VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ad=2.17e-13 as=2.17e-13 pd=2.02e-06 ps=2.02e-06 ng=1 
XMP2 Y C VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ad=2.17e-13 as=2.17e-13 pd=2.02e-06 ps=2.02e-06 ng=1 
XMP3 Y D VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ad=2.17e-13 as=2.17e-13 pd=2.02e-06 ps=2.02e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NAND4_D1 A B C D Y VDD VSS
*.PININFO A:I B:I C:I D:I Y:O VDD:B VSS:B 
MN0 n0 D VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MN1 n1 C n0 VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MN2 n2 B n1 VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MN3 Y A n2 VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MP0 Y A VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ng=1 
MP1 Y B VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ng=1 
MP2 Y C VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ng=1 
MP3 Y D VDD VDD sg13_lv_pmos w=7e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### NAND4_D2

#### Hierarchical SPICE netlist
```spice
.subckt NAND4_D2 A B C D Y VDD VSS
Xnand4 A B C D Y VDD VSS nand4_par WN=1.4e-06 WP=1.2e-06 NGN=2 NGP=1 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NAND4_D2 A B C D Y VDD VSS
XMN0 n0 D VSS VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=2 
XMN1 n1 C n0 VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=2 
XMN2 n2 B n1 VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=2 
XMN3 Y A n2 VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=2 
XMP0 Y A VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ad=3.72e-13 as=3.72e-13 pd=3.02e-06 ps=3.02e-06 ng=1 
XMP1 Y B VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ad=3.72e-13 as=3.72e-13 pd=3.02e-06 ps=3.02e-06 ng=1 
XMP2 Y C VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ad=3.72e-13 as=3.72e-13 pd=3.02e-06 ps=3.02e-06 ng=1 
XMP3 Y D VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ad=3.72e-13 as=3.72e-13 pd=3.02e-06 ps=3.02e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NAND4_D2 A B C D Y VDD VSS
*.PININFO A:I B:I C:I D:I Y:O VDD:B VSS:B 
MN0 n0 D VSS VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ng=2 
MN1 n1 C n0 VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ng=2 
MN2 n2 B n1 VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ng=2 
MN3 Y A n2 VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ng=2 
MP0 Y A VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ng=1 
MP1 Y B VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ng=1 
MP2 Y C VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ng=1 
MP3 Y D VDD VDD sg13_lv_pmos w=1.2e-06 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### NAND4_D4

#### Hierarchical SPICE netlist
```spice
.subckt NAND4_D4 A B C D Y VDD VSS
Xnand4 A B C D Y VDD VSS nand4_par WN=3.18e-06 WP=2.6e-06 NGN=3 NGP=2 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NAND4_D4 A B C D Y VDD VSS
XMN0 n0 D VSS VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ad=9.858e-13 as=9.858e-13 pd=6.98e-06 ps=6.98e-06 ng=3 
XMN1 n1 C n0 VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ad=9.858e-13 as=9.858e-13 pd=6.98e-06 ps=6.98e-06 ng=3 
XMN2 n2 B n1 VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ad=9.858e-13 as=9.858e-13 pd=6.98e-06 ps=6.98e-06 ng=3 
XMN3 Y A n2 VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ad=9.858e-13 as=9.858e-13 pd=6.98e-06 ps=6.98e-06 ng=3 
XMP0 Y A VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ad=8.06e-13 as=8.06e-13 pd=5.82e-06 ps=5.82e-06 ng=2 
XMP1 Y B VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ad=8.06e-13 as=8.06e-13 pd=5.82e-06 ps=5.82e-06 ng=2 
XMP2 Y C VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ad=8.06e-13 as=8.06e-13 pd=5.82e-06 ps=5.82e-06 ng=2 
XMP3 Y D VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ad=8.06e-13 as=8.06e-13 pd=5.82e-06 ps=5.82e-06 ng=2 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NAND4_D4 A B C D Y VDD VSS
*.PININFO A:I B:I C:I D:I Y:O VDD:B VSS:B 
MN0 n0 D VSS VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ng=3 
MN1 n1 C n0 VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ng=3 
MN2 n2 B n1 VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ng=3 
MN3 Y A n2 VSS sg13_lv_nmos w=3.18e-06 l=1.3e-07 ng=3 
MP0 Y A VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ng=2 
MP1 Y B VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ng=2 
MP2 Y C VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ng=2 
MP3 Y D VDD VDD sg13_lv_pmos w=2.6e-06 l=1.3e-07 ng=2 
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

