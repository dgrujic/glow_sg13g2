# DFASQN

D flip-flop with asynchronous set and output QN.

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| D | Data input |
| CLK | Clock |
| SN | Asynchronous set, inverted |
| QN | Data output, inverted |
| VDD | Power supply |
| VSS | Ground |


## Truth table

| CLK | D | SN | QN | Description | 
| :--- | :--- | :--- | :--- | :--- | 
| ↑ | 0 | 1 | 1 | Write 0 | 
| ↑ | 1 | 1 | 0 | Write 1 | 
| - | - | 0 | 0 | Set | 


## Symbol

<div align="center">
<img src="figs/DFASQN_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/DFASQN_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [DFASQN_DL](#dfasqn_dl) | TBD | TBD |
| [DFASQN_D1](#dfasqn_d1) | TBD | TBD |



### DFASQN_DL

#### Hierarchical SPICE netlist
```spice
.subckt DFASQN_DL D CLK QN SN VDD VSS
Xinv_clkn CLK clkn VDD VSS inv_par WN=2e-07 WP=3e-07 
Xinv_clki clkn clki VDD VSS inv_par WN=2e-07 WP=3e-07 
Xinvz_in D clkn clki dn VDD VSS invz2_par WN=1.5e-07 WP=2.3e-07 
Xnand_ml SN dn di VDD VSS nand2_par WN=2e-07 WP=2.2e-07 
Xinvz_mfb di clki clkn dn VDD VSS invz_par WN=1.5e-07 WP=2.3e-07 WEAK=1 
Xinvz_ms di clki clkn qin VDD VSS invz_par WN=3e-07 WP=4.5e-07 
Xnand_sl SN qin qi VDD VSS nand2_par WN=2e-07 WP=2.2e-07 
Xinvz_sfb qi clkn clki qin VDD VSS invz_par WN=1.5e-07 WP=1.5e-07 
Xinv_QN qi QN VDD VSS inv_par WN=3.2e-07 WP=4.8e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt DFASQN_DL D CLK QN SN VDD VSS
XMN0 n0 CLK VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP0 n0 CLK VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN2 n2 D n3 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN3 n3 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP2 n2 D n4 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP3 n4 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN4 n5 SN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN5 n6 n2 n5 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP4 n6 SN VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ad=6.82e-14 as=6.82e-14 pd=1.06e-06 ps=1.06e-06 ng=1 
XMP5 n6 n2 VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ad=6.82e-14 as=6.82e-14 pd=1.06e-06 ps=1.06e-06 ng=1 
XMN6 n2 n1 n7 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN7 n7 n6 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP6 n2 n0 n8 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP7 n8 n6 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN8 n9 n1 n10 VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN9 n10 n6 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP8 n9 n0 n11 VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMP9 n11 n6 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN10 n12 SN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN11 n13 n9 n12 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP10 n13 SN VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ad=6.82e-14 as=6.82e-14 pd=1.06e-06 ps=1.06e-06 ng=1 
XMP11 n13 n9 VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ad=6.82e-14 as=6.82e-14 pd=1.06e-06 ps=1.06e-06 ng=1 
XMN12 n9 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP12 n9 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN14 QN n13 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad=9.92e-14 as=9.92e-14 pd=1.26e-06 ps=1.26e-06 ng=1 
XMP14 QN n13 VDD VDD sg13_lv_pmos w=4.8e-07 l=1.3e-07 ad=1.488e-13 as=1.488e-13 pd=1.58e-06 ps=1.58e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT DFASQN_DL D CLK QN SN VDD VSS
*.PININFO CLK:I D:I SN:I QN:O VDD:B VSS:B 
MN0 n0 CLK VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP0 n0 CLK VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN2 n2 D n3 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN3 n3 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP2 n2 D n4 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP3 n4 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN4 n5 SN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN5 n6 n2 n5 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP4 n6 SN VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ng=1 
MP5 n6 n2 VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ng=1 
MN6 n2 n1 n7 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN7 n7 n6 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP6 n2 n0 n8 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP7 n8 n6 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN8 n9 n1 n10 VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MN9 n10 n6 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP8 n9 n0 n11 VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MP9 n11 n6 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MN10 n12 SN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN11 n13 n9 n12 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP10 n13 SN VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ng=1 
MP11 n13 n9 VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ng=1 
MN12 n9 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP12 n9 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MN14 QN n13 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ng=1 
MP14 QN n13 VDD VDD sg13_lv_pmos w=4.8e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### DFASQN_D1

#### Hierarchical SPICE netlist
```spice
.subckt DFASQN_D1 D CLK QN SN VDD VSS
Xinv_clkn CLK clkn VDD VSS inv_par WN=3e-07 WP=4.5e-07 
Xinv_clki clkn clki VDD VSS inv_par WN=2e-07 WP=3e-07 
Xinvz_in D clkn clki dn VDD VSS invz2_par WN=1.5e-07 WP=2.3e-07 
Xnand_ml SN dn di VDD VSS nand2_par WN=2e-07 WP=2.2e-07 
Xinvz_mfb di clki clkn dn VDD VSS invz_par WN=1.5e-07 WP=2.3e-07 WEAK=1 
Xinvz_ms di clki clkn qin VDD VSS invz_par WN=5e-07 WP=7.5e-07 
Xnand_sl SN qin qi VDD VSS nand2_par WN=3e-07 WP=3.3e-07 
Xinvz_sfb qi clkn clki qin VDD VSS invz_par WN=1.5e-07 WP=1.5e-07 
Xinv_QN qi QN VDD VSS inv_par WN=6.4e-07 WP=9.8e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt DFASQN_D1 D CLK QN SN VDD VSS
XMN0 n0 CLK VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP0 n0 CLK VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN2 n2 D n3 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN3 n3 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP2 n2 D n4 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP3 n4 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN4 n5 SN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN5 n6 n2 n5 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP4 n6 SN VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ad=6.82e-14 as=6.82e-14 pd=1.06e-06 ps=1.06e-06 ng=1 
XMP5 n6 n2 VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ad=6.82e-14 as=6.82e-14 pd=1.06e-06 ps=1.06e-06 ng=1 
XMN6 n2 n1 n7 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN7 n7 n6 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP6 n2 n0 n8 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP7 n8 n6 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN8 n9 n1 n10 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN9 n10 n6 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMP8 n9 n0 n11 VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ad=2.325e-13 as=2.325e-13 pd=2.12e-06 ps=2.12e-06 ng=1 
XMP9 n11 n6 VDD VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ad=2.325e-13 as=2.325e-13 pd=2.12e-06 ps=2.12e-06 ng=1 
XMN10 n12 SN VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN11 n13 n9 n12 VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP10 n13 SN VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ad=1.023e-13 as=1.023e-13 pd=1.28e-06 ps=1.28e-06 ng=1 
XMP11 n13 n9 VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ad=1.023e-13 as=1.023e-13 pd=1.28e-06 ps=1.28e-06 ng=1 
XMN12 n9 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP12 n9 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN14 QN n13 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 ng=1 
XMP14 QN n13 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ad=3.038e-13 as=3.038e-13 pd=2.58e-06 ps=2.58e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT DFASQN_D1 D CLK QN SN VDD VSS
*.PININFO CLK:I D:I SN:I QN:O VDD:B VSS:B 
MN0 n0 CLK VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP0 n0 CLK VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN2 n2 D n3 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN3 n3 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP2 n2 D n4 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP3 n4 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN4 n5 SN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN5 n6 n2 n5 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP4 n6 SN VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ng=1 
MP5 n6 n2 VDD VDD sg13_lv_pmos w=2.2e-07 l=1.3e-07 ng=1 
MN6 n2 n1 n7 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN7 n7 n6 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP6 n2 n0 n8 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP7 n8 n6 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN8 n9 n1 n10 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN9 n10 n6 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MP8 n9 n0 n11 VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ng=1 
MP9 n11 n6 VDD VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ng=1 
MN10 n12 SN VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MN11 n13 n9 n12 VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP10 n13 SN VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ng=1 
MP11 n13 n9 VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ng=1 
MN12 n9 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP12 n9 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MN14 QN n13 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ng=1 
MP14 QN n13 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ng=1 
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

