# AND3

Three input AND gate

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| A | Input A |
| B | Input B |
| C | Input C |
| Y | Output |
| VDD | Power supply |
| VSS | Ground |


## Logic function and Truth table

### Logic function (Python)
<div align="center">
Y = A & B & C
</div>

### Logic function (Boolean)
\\[ Y = A \cdot B \cdot C \\]

### Truth Table for Y


| A | B | C | Y |
| :--- | :--- | :--- | :--- |
| 1 | 1 | 1 | 1 | 
| 0 | - | - | 0 | 
| - | 0 | - | 0 | 
| - | - | 0 | 0 | 


## Symbol

<div align="center">
<img src="figs/AND3_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/AND3_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [AND3_DL](#and3_dl) | TBD | TBD |
| [AND3_D1](#and3_d1) | TBD | TBD |
| [AND3_D2](#and3_d2) | TBD | TBD |
| [AND3_D4](#and3_d4) | TBD | TBD |



### AND3_DL

#### Hierarchical SPICE netlist
```spice
.subckt AND3_DL A B C Y VDD VSS
Xnand3 A B C NO VDD VSS nand3_par WN=3.3e-07 WP=3e-07 
Xinv NO Y VDD VSS inv_par WN=3.2e-07 WP=4.9e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt AND3_DL A B C Y VDD VSS
XMN0 n0 C VSS VSS sg13_lv_nmos w=3.3e-07 l=1.3e-07 ad=1.023e-13 as=1.023e-13 pd=1.28e-06 ps=1.28e-06 ng=1 
XMN1 n1 B n0 VSS sg13_lv_nmos w=3.3e-07 l=1.3e-07 ad=1.023e-13 as=1.023e-13 pd=1.28e-06 ps=1.28e-06 ng=1 
XMN2 n2 A n1 VSS sg13_lv_nmos w=3.3e-07 l=1.3e-07 ad=1.023e-13 as=1.023e-13 pd=1.28e-06 ps=1.28e-06 ng=1 
XMP0 n2 A VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP1 n2 B VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP2 n2 C VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN3 Y n2 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad=9.92e-14 as=9.92e-14 pd=1.26e-06 ps=1.26e-06 ng=1 
XMP3 Y n2 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ad=1.519e-13 as=1.519e-13 pd=1.6e-06 ps=1.6e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT AND3_DL A B C Y VDD VSS
*.PININFO C:I B:I A:I Y:O VDD:B VSS:B 
MN0 n0 C VSS VSS sg13_lv_nmos w=3.3e-07 l=1.3e-07 ng=1 
MN1 n1 B n0 VSS sg13_lv_nmos w=3.3e-07 l=1.3e-07 ng=1 
MN2 n2 A n1 VSS sg13_lv_nmos w=3.3e-07 l=1.3e-07 ng=1 
MP0 n2 A VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MP1 n2 B VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MP2 n2 C VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN3 Y n2 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ng=1 
MP3 Y n2 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### AND3_D1

#### Hierarchical SPICE netlist
```spice
.subckt AND3_D1 A B C Y VDD VSS
Xnand3 A B C NO VDD VSS nand3_par WN=4.2e-07 WP=3.8e-07 
Xinv NO Y VDD VSS inv_par WN=6.4e-07 WP=9.8e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt AND3_D1 A B C Y VDD VSS
XMN0 n0 C VSS VSS sg13_lv_nmos w=4.2e-07 l=1.3e-07 ad=1.302e-13 as=1.302e-13 pd=1.46e-06 ps=1.46e-06 ng=1 
XMN1 n1 B n0 VSS sg13_lv_nmos w=4.2e-07 l=1.3e-07 ad=1.302e-13 as=1.302e-13 pd=1.46e-06 ps=1.46e-06 ng=1 
XMN2 n2 A n1 VSS sg13_lv_nmos w=4.2e-07 l=1.3e-07 ad=1.302e-13 as=1.302e-13 pd=1.46e-06 ps=1.46e-06 ng=1 
XMP0 n2 A VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ad=1.178e-13 as=1.178e-13 pd=1.38e-06 ps=1.38e-06 ng=1 
XMP1 n2 B VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ad=1.178e-13 as=1.178e-13 pd=1.38e-06 ps=1.38e-06 ng=1 
XMP2 n2 C VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ad=1.178e-13 as=1.178e-13 pd=1.38e-06 ps=1.38e-06 ng=1 
XMN3 Y n2 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 ng=1 
XMP3 Y n2 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ad=3.038e-13 as=3.038e-13 pd=2.58e-06 ps=2.58e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT AND3_D1 A B C Y VDD VSS
*.PININFO C:I B:I A:I Y:O VDD:B VSS:B 
MN0 n0 C VSS VSS sg13_lv_nmos w=4.2e-07 l=1.3e-07 ng=1 
MN1 n1 B n0 VSS sg13_lv_nmos w=4.2e-07 l=1.3e-07 ng=1 
MN2 n2 A n1 VSS sg13_lv_nmos w=4.2e-07 l=1.3e-07 ng=1 
MP0 n2 A VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ng=1 
MP1 n2 B VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ng=1 
MP2 n2 C VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ng=1 
MN3 Y n2 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ng=1 
MP3 Y n2 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### AND3_D2

#### Hierarchical SPICE netlist
```spice
.subckt AND3_D2 A B C Y VDD VSS
Xnand3 A B C NO VDD VSS nand3_par WN=5e-07 WP=4.5e-07 
Xinv NO Y VDD VSS inv_par WN=1.07e-06 WP=1.6e-06 
.ends
```

#### Flat SPICE netlist
```spice
.subckt AND3_D2 A B C Y VDD VSS
XMN0 n0 C VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN1 n1 B n0 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN2 n2 A n1 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMP0 n2 A VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMP1 n2 B VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMP2 n2 C VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN3 Y n2 VSS VSS sg13_lv_nmos w=1.07e-06 l=1.3e-07 ad=3.317e-13 as=3.317e-13 pd=2.76e-06 ps=2.76e-06 ng=1 
XMP3 Y n2 VDD VDD sg13_lv_pmos w=1.6e-06 l=1.3e-07 ad=4.96e-13 as=4.96e-13 pd=3.82e-06 ps=3.82e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT AND3_D2 A B C Y VDD VSS
*.PININFO C:I B:I A:I Y:O VDD:B VSS:B 
MN0 n0 C VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN1 n1 B n0 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN2 n2 A n1 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MP0 n2 A VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MP1 n2 B VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MP2 n2 C VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MN3 Y n2 VSS VSS sg13_lv_nmos w=1.07e-06 l=1.3e-07 ng=1 
MP3 Y n2 VDD VDD sg13_lv_pmos w=1.6e-06 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### AND3_D4

#### Hierarchical SPICE netlist
```spice
.subckt AND3_D4 A B C Y VDD VSS
Xnand3 A B C NO VDD VSS nand3_par WN=1e-06 WP=8e-07 
Xinv NO Y VDD VSS inv_par WN=2.14e-06 WP=3.2e-06 NGN=2 NGP=2 
.ends
```

#### Flat SPICE netlist
```spice
.subckt AND3_D4 A B C Y VDD VSS
XMN0 n0 C VSS VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ad=3.1e-13 as=3.1e-13 pd=2.62e-06 ps=2.62e-06 ng=1 
XMN1 n1 B n0 VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ad=3.1e-13 as=3.1e-13 pd=2.62e-06 ps=2.62e-06 ng=1 
XMN2 n2 A n1 VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ad=3.1e-13 as=3.1e-13 pd=2.62e-06 ps=2.62e-06 ng=1 
XMP0 n2 A VDD VDD sg13_lv_pmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMP1 n2 B VDD VDD sg13_lv_pmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMP2 n2 C VDD VDD sg13_lv_pmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMN3 Y n2 VSS VSS sg13_lv_nmos w=2.14e-06 l=1.3e-07 ad=6.634e-13 as=6.634e-13 pd=4.9e-06 ps=4.9e-06 ng=2 
XMP3 Y n2 VDD VDD sg13_lv_pmos w=3.2e-06 l=1.3e-07 ad=9.92e-13 as=9.92e-13 pd=7.02e-06 ps=7.02e-06 ng=2 
.ends
```

#### CDL netlist
```cdl
.SUBCKT AND3_D4 A B C Y VDD VSS
*.PININFO C:I B:I A:I Y:O VDD:B VSS:B 
MN0 n0 C VSS VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ng=1 
MN1 n1 B n0 VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ng=1 
MN2 n2 A n1 VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ng=1 
MP0 n2 A VDD VDD sg13_lv_pmos w=8e-07 l=1.3e-07 ng=1 
MP1 n2 B VDD VDD sg13_lv_pmos w=8e-07 l=1.3e-07 ng=1 
MP2 n2 C VDD VDD sg13_lv_pmos w=8e-07 l=1.3e-07 ng=1 
MN3 Y n2 VSS VSS sg13_lv_nmos w=2.14e-06 l=1.3e-07 ng=2 
MP3 Y n2 VDD VDD sg13_lv_pmos w=3.2e-06 l=1.3e-07 ng=2 
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

