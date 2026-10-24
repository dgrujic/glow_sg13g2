# OR3

Three input OR gate

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
Y = A | B | C
</div>

### Logic function (Boolean)
\\[ Y = A + B + C \\]

### Truth Table for Y


| A | B | C | Y |
| :--- | :--- | :--- | :--- |
| 1 | - | - | 1 | 
| - | 1 | - | 1 | 
| - | - | 1 | 1 | 
| 0 | 0 | 0 | 0 | 


## Symbol

<div align="center">
<img src="figs/OR3_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/OR3_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [OR3_DL](#or3_dl) | TBD | TBD |
| [OR3_D1](#or3_d1) | TBD | TBD |
| [OR3_D2](#or3_d2) | TBD | TBD |
| [OR3_D4](#or3_d4) | TBD | TBD |



### OR3_DL

#### Hierarchical SPICE netlist
```spice
.subckt OR3_DL A B C Y VDD VSS
Xnor3 A B C NO VDD VSS nor3_par WN=1.7e-07 WP=5.1e-07 
Xinv NO Y VDD VSS inv_par WN=3.2e-07 WP=4.9e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt OR3_DL A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=1.7e-07 l=1.3e-07 ad=5.27e-14 as=5.27e-14 pd=9.6e-07 ps=9.6e-07 ng=1 
XMN1 n0 B VSS VSS sg13_lv_nmos w=1.7e-07 l=1.3e-07 ad=5.27e-14 as=5.27e-14 pd=9.6e-07 ps=9.6e-07 ng=1 
XMN2 n0 C VSS VSS sg13_lv_nmos w=1.7e-07 l=1.3e-07 ad=5.27e-14 as=5.27e-14 pd=9.6e-07 ps=9.6e-07 ng=1 
XMP0 n1 A VDD VDD sg13_lv_pmos w=5.1e-07 l=1.3e-07 ad=1.581e-13 as=1.581e-13 pd=1.64e-06 ps=1.64e-06 ng=1 
XMP1 n2 B n1 VDD sg13_lv_pmos w=5.1e-07 l=1.3e-07 ad=1.581e-13 as=1.581e-13 pd=1.64e-06 ps=1.64e-06 ng=1 
XMP2 n0 C n2 VDD sg13_lv_pmos w=5.1e-07 l=1.3e-07 ad=1.581e-13 as=1.581e-13 pd=1.64e-06 ps=1.64e-06 ng=1 
XMN3 Y n0 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad=9.92e-14 as=9.92e-14 pd=1.26e-06 ps=1.26e-06 ng=1 
XMP3 Y n0 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ad=1.519e-13 as=1.519e-13 pd=1.6e-06 ps=1.6e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT OR3_DL A B C Y VDD VSS
*.PININFO A:I B:I C:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=1.7e-07 l=1.3e-07 ng=1 
MN1 n0 B VSS VSS sg13_lv_nmos w=1.7e-07 l=1.3e-07 ng=1 
MN2 n0 C VSS VSS sg13_lv_nmos w=1.7e-07 l=1.3e-07 ng=1 
MP0 n1 A VDD VDD sg13_lv_pmos w=5.1e-07 l=1.3e-07 ng=1 
MP1 n2 B n1 VDD sg13_lv_pmos w=5.1e-07 l=1.3e-07 ng=1 
MP2 n0 C n2 VDD sg13_lv_pmos w=5.1e-07 l=1.3e-07 ng=1 
MN3 Y n0 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ng=1 
MP3 Y n0 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### OR3_D1

#### Hierarchical SPICE netlist
```spice
.subckt OR3_D1 A B C Y VDD VSS
Xnor3 A B C NO VDD VSS nor3_par WN=2e-07 WP=6e-07 
Xinv NO Y VDD VSS inv_par WN=6.4e-07 WP=9.8e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt OR3_D1 A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN1 n0 B VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN2 n0 C VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP0 n1 A VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP1 n2 B n1 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP2 n0 C n2 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMN3 Y n0 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 ng=1 
XMP3 Y n0 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ad=3.038e-13 as=3.038e-13 pd=2.58e-06 ps=2.58e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT OR3_D1 A B C Y VDD VSS
*.PININFO A:I B:I C:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN1 n0 B VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN2 n0 C VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP0 n1 A VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MP1 n2 B n1 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MP2 n0 C n2 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MN3 Y n0 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ng=1 
MP3 Y n0 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### OR3_D2

#### Hierarchical SPICE netlist
```spice
.subckt OR3_D2 A B C Y VDD VSS
Xnor3 A B C NO VDD VSS nor3_par WN=5e-07 WP=1.1e-06 
Xinv NO Y VDD VSS inv_par WN=1.07e-06 WP=1.6e-06 NGN=2 NGP=2 
.ends
```

#### Flat SPICE netlist
```spice
.subckt OR3_D2 A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN1 n0 B VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN2 n0 C VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMP0 n1 A VDD VDD sg13_lv_pmos w=1.1e-06 l=1.3e-07 ad=3.41e-13 as=3.41e-13 pd=2.82e-06 ps=2.82e-06 ng=1 
XMP1 n2 B n1 VDD sg13_lv_pmos w=1.1e-06 l=1.3e-07 ad=3.41e-13 as=3.41e-13 pd=2.82e-06 ps=2.82e-06 ng=1 
XMP2 n0 C n2 VDD sg13_lv_pmos w=1.1e-06 l=1.3e-07 ad=3.41e-13 as=3.41e-13 pd=2.82e-06 ps=2.82e-06 ng=1 
XMN3 Y n0 VSS VSS sg13_lv_nmos w=1.07e-06 l=1.3e-07 ad=3.317e-13 as=3.317e-13 pd=2.76e-06 ps=2.76e-06 ng=2 
XMP3 Y n0 VDD VDD sg13_lv_pmos w=1.6e-06 l=1.3e-07 ad=4.96e-13 as=4.96e-13 pd=3.82e-06 ps=3.82e-06 ng=2 
.ends
```

#### CDL netlist
```cdl
.SUBCKT OR3_D2 A B C Y VDD VSS
*.PININFO A:I B:I C:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN1 n0 B VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN2 n0 C VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MP0 n1 A VDD VDD sg13_lv_pmos w=1.1e-06 l=1.3e-07 ng=1 
MP1 n2 B n1 VDD sg13_lv_pmos w=1.1e-06 l=1.3e-07 ng=1 
MP2 n0 C n2 VDD sg13_lv_pmos w=1.1e-06 l=1.3e-07 ng=1 
MN3 Y n0 VSS VSS sg13_lv_nmos w=1.07e-06 l=1.3e-07 ng=2 
MP3 Y n0 VDD VDD sg13_lv_pmos w=1.6e-06 l=1.3e-07 ng=2 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### OR3_D4

#### Hierarchical SPICE netlist
```spice
.subckt OR3_D4 A B C Y VDD VSS
Xnor3 A B C NO VDD VSS nor3_par WN=8e-07 WP=2.4e-06 NGN=2 NGP=2 
Xinv NO Y VDD VSS inv_par WN=2.4e-06 WP=3.2e-06 NGN=3 NGP=3 
.ends
```

#### Flat SPICE netlist
```spice
.subckt OR3_D4 A B C Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=2 
XMN1 n0 B VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=2 
XMN2 n0 C VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=2 
XMP0 n1 A VDD VDD sg13_lv_pmos w=2.4e-06 l=1.3e-07 ad=7.44e-13 as=7.44e-13 pd=5.42e-06 ps=5.42e-06 ng=2 
XMP1 n2 B n1 VDD sg13_lv_pmos w=2.4e-06 l=1.3e-07 ad=7.44e-13 as=7.44e-13 pd=5.42e-06 ps=5.42e-06 ng=2 
XMP2 n0 C n2 VDD sg13_lv_pmos w=2.4e-06 l=1.3e-07 ad=7.44e-13 as=7.44e-13 pd=5.42e-06 ps=5.42e-06 ng=2 
XMN3 Y n0 VSS VSS sg13_lv_nmos w=2.4e-06 l=1.3e-07 ad=7.44e-13 as=7.44e-13 pd=5.42e-06 ps=5.42e-06 ng=3 
XMP3 Y n0 VDD VDD sg13_lv_pmos w=3.2e-06 l=1.3e-07 ad=9.92e-13 as=9.92e-13 pd=7.02e-06 ps=7.02e-06 ng=3 
.ends
```

#### CDL netlist
```cdl
.SUBCKT OR3_D4 A B C Y VDD VSS
*.PININFO A:I B:I C:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=2 
MN1 n0 B VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=2 
MN2 n0 C VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=2 
MP0 n1 A VDD VDD sg13_lv_pmos w=2.4e-06 l=1.3e-07 ng=2 
MP1 n2 B n1 VDD sg13_lv_pmos w=2.4e-06 l=1.3e-07 ng=2 
MP2 n0 C n2 VDD sg13_lv_pmos w=2.4e-06 l=1.3e-07 ng=2 
MN3 Y n0 VSS VSS sg13_lv_nmos w=2.4e-06 l=1.3e-07 ng=3 
MP3 Y n0 VDD VDD sg13_lv_pmos w=3.2e-06 l=1.3e-07 ng=3 
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

