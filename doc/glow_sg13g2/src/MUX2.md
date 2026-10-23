# MUX2

Two input multiplexer.

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| I0 | Input 0 |
| I1 | Input 1 |
| S0 | Select control signal |
| Y | Output |
| VDD | Power supply |
| VSS | Ground |


## Logic function and Truth table

### Logic function (Python)
<div align="center">
Y = (I0 & ~S0) | (I1 & S0)
</div>

### Logic function (Boolean)
\\[ Y = (I0 \cdot \overline{S0} + I1 \cdot S0) \\]

### Truth Table for Y


| I0 | I1 | S0 | Y |
| :--- | :--- | :--- | :--- |
| - | 1 | 1 | 1 | 
| 1 | - | 0 | 1 | 
| 0 | - | 0 | 0 | 
| - | 0 | 1 | 0 | 


## Symbol

<div align="center">
<img src="figs/MUX2_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/MUX2_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [MUX2_DL](#mux2_dl) | TBD | TBD |
| [MUX2_D1](#mux2_d1) | TBD | TBD |



### MUX2_DL

#### Hierarchical SPICE netlist
```spice
.subckt MUX2_DL I0 I1 S0 Y VDD VSS
Xinv_S0 S0 S0B VDD VSS inv_par WN=2e-07 WP=3e-07 
Xinv_y NY Y VDD VSS inv_par WN=3.2e-07 WP=4.9e-07 
Xinvz_I0 I0 S0B S0 NY VDD VSS invz_par WN=2e-07 WP=3e-07 
Xinvz_I1 I1 S0 S0B NY VDD VSS invz_par WN=2e-07 WP=3e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt MUX2_DL I0 I1 S0 Y VDD VSS
XMN0 n0 S0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP0 n0 S0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN1 Y n1 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad=9.92e-14 as=9.92e-14 pd=1.26e-06 ps=1.26e-06 ng=1 
XMP1 Y n1 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ad=1.519e-13 as=1.519e-13 pd=1.6e-06 ps=1.6e-06 ng=1 
XMN2 n1 n0 n2 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN3 n2 I0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP2 n1 S0 n3 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP3 n3 I0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN4 n1 S0 n4 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN5 n4 I1 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP4 n1 n0 n5 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP5 n5 I1 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT MUX2_DL I0 I1 S0 Y VDD VSS
*.PININFO I1:I S0:I I0:I Y:O VDD:B VSS:B 
MN0 n0 S0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP0 n0 S0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN1 Y n1 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ng=1 
MP1 Y n1 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ng=1 
MN2 n1 n0 n2 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN3 n2 I0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP2 n1 S0 n3 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MP3 n3 I0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN4 n1 S0 n4 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN5 n4 I1 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP4 n1 n0 n5 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MP5 n5 I1 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### MUX2_D1

#### Hierarchical SPICE netlist
```spice
.subckt MUX2_D1 I0 I1 S0 Y VDD VSS
Xinv_S0 S0 S0B VDD VSS inv_par WN=1.5e-07 WP=2.3e-07 
Xinv_y NY Y VDD VSS inv_par WN=6.4e-07 WP=9.8e-07 
Xinvz_I0 I0 S0B S0 NY VDD VSS invz_par WN=4e-07 WP=6e-07 
Xinvz_I1 I1 S0 S0B NY VDD VSS invz_par WN=4e-07 WP=6e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt MUX2_D1 I0 I1 S0 Y VDD VSS
XMN0 n0 S0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP0 n0 S0 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN1 Y n1 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 ng=1 
XMP1 Y n1 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ad=3.038e-13 as=3.038e-13 pd=2.58e-06 ps=2.58e-06 ng=1 
XMN2 n1 n0 n2 VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMN3 n2 I0 VSS VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMP2 n1 S0 n3 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP3 n3 I0 VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMN4 n1 S0 n4 VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMN5 n4 I1 VSS VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMP4 n1 n0 n5 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP5 n5 I1 VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT MUX2_D1 I0 I1 S0 Y VDD VSS
*.PININFO I1:I S0:I I0:I Y:O VDD:B VSS:B 
MN0 n0 S0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP0 n0 S0 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN1 Y n1 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ng=1 
MP1 Y n1 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ng=1 
MN2 n1 n0 n2 VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ng=1 
MN3 n2 I0 VSS VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ng=1 
MP2 n1 S0 n3 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MP3 n3 I0 VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MN4 n1 S0 n4 VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ng=1 
MN5 n4 I1 VSS VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ng=1 
MP4 n1 n0 n5 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MP5 n5 I1 VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
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

