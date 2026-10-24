# DFRQ

D flip-flop with synchronous reset and output Q.

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| D | Data input |
| CLK | Clock |
| RN | Synchronous reset, inverted |
| Q | Data output |
| VDD | Power supply |
| VSS | Ground |


## Truth table

| CLK | D | RN | Q | Description | 
| :--- | :--- | :--- | :--- | :--- | 
| ↑ | 0 | 1 | 0 | Write 0 | 
| ↑ | 1 | 1 | 1 | Write 1 | 
| ↑ | - | 0 | 0 | Clear | 


## Symbol

<div align="center">
<img src="figs/DFRQ_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/DFRQ_sch.svg" />
</div>

## Verification simulation waveform

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://svg.wavedrom.com/%7B%22signal%22%3A%5B%7B%22name%22%3A%22CLK%22%2C%22wave%22%3A%220.10101....0....1....0....10.10.%22%7D%2C%7B%22name%22%3A%22D%22%2C%22wave%22%3A%220..1.0..1010101..01010101.......%22%7D%2C%7B%22name%22%3A%22RN%22%2C%22wave%22%3A%221...........................0..1%22%7D%2C%7B%22name%22%3A%22Q%22%2C%22wave%22%3A%220...1.0.........1............0..%22%7D%5D%2C%22config%22%3A%7B%22skin%22%3A%22dark%22%7D%7D">
  <img alt="Timing Diagram" src="https://svg.wavedrom.com/%7B%22signal%22%3A%5B%7B%22name%22%3A%22CLK%22%2C%22wave%22%3A%220.10101....0....1....0....10.10.%22%7D%2C%7B%22name%22%3A%22D%22%2C%22wave%22%3A%220..1.0..1010101..01010101.......%22%7D%2C%7B%22name%22%3A%22RN%22%2C%22wave%22%3A%221...........................0..1%22%7D%2C%7B%22name%22%3A%22Q%22%2C%22wave%22%3A%220...1.0.........1............0..%22%7D%5D%7D">
</picture>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [DFRQ_DL](#dfrq_dl) | TBD | TBD |
| [DFRQ_D1](#dfrq_d1) | TBD | TBD |
| [DFRQ_D2](#dfrq_d2) | TBD | TBD |



### DFRQ_DL

#### Hierarchical SPICE netlist
```spice
.subckt DFRQ_DL D CLK RN Q VDD VSS
Xinv_clkn CLK clkn VDD VSS inv_par WN=2e-07 WP=3e-07 
Xinv_clki clkn clki VDD VSS inv_par WN=2e-07 WP=3e-07 
Xnand_in RN D dnand VDD VSS nand2_par WN=2e-07 WP=2.3e-07 
Xinvz_in dnand clkn clki dn VDD VSS invz2_par WN=1.5e-07 WP=2.3e-07 
Xinv_ml dn di VDD VSS inv_par WN=1.5e-07 WP=2.3e-07 
Xinvz_mfb di clki clkn dn VDD VSS invz_par WN=1.5e-07 WP=2.3e-07 WEAK=1 
Xinvz_ms di clki clkn qin VDD VSS invz_par WN=2e-07 WP=3e-07 
Xinv_sl qin qi VDD VSS inv_par WN=1.5e-07 WP=2.3e-07 
Xinvz_sfb qi clkn clki qin VDD VSS invz_par WN=1.5e-07 WP=1.5e-07 
Xinv_Q qi Q VDD VSS inv_par WN=3.2e-07 WP=4.9e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt DFRQ_DL D CLK RN Q VDD VSS
XMN0 n0 CLK VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP0 n0 CLK VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN2 n2 RN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN3 n3 D n2 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP2 n3 RN VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP3 n3 D VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN4 n4 n3 n5 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN5 n5 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP4 n4 n3 n6 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP5 n6 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN6 n7 n4 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP6 n7 n4 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN7 n4 n1 n8 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN8 n8 n7 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP7 n4 n0 n9 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP8 n9 n7 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN9 n10 n1 n11 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN10 n11 n7 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP9 n10 n0 n12 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP10 n12 n7 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN11 n13 n10 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP11 n13 n10 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN12 n10 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP12 n10 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN14 Q n13 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ad=9.92e-14 as=9.92e-14 pd=1.26e-06 ps=1.26e-06 ng=1 
XMP14 Q n13 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ad=1.519e-13 as=1.519e-13 pd=1.6e-06 ps=1.6e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT DFRQ_DL D CLK RN Q VDD VSS
*.PININFO CLK:I D:I RN:I Q:O VDD:B VSS:B 
MN0 n0 CLK VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP0 n0 CLK VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN2 n2 RN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN3 n3 D n2 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP2 n3 RN VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP3 n3 D VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN4 n4 n3 n5 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN5 n5 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP4 n4 n3 n6 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP5 n6 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN6 n7 n4 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP6 n7 n4 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN7 n4 n1 n8 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN8 n8 n7 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP7 n4 n0 n9 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP8 n9 n7 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN9 n10 n1 n11 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN10 n11 n7 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP9 n10 n0 n12 VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MP10 n12 n7 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN11 n13 n10 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP11 n13 n10 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN12 n10 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP12 n10 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MN14 Q n13 VSS VSS sg13_lv_nmos w=3.2e-07 l=1.3e-07 ng=1 
MP14 Q n13 VDD VDD sg13_lv_pmos w=4.9e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### DFRQ_D1

#### Hierarchical SPICE netlist
```spice
.subckt DFRQ_D1 D CLK RN Q VDD VSS
Xinv_clkn CLK clkn VDD VSS inv_par WN=3e-07 WP=4.5e-07 
Xinv_clki clkn clki VDD VSS inv_par WN=2e-07 WP=3e-07 
Xnand_in RN D dnand VDD VSS nand2_par WN=2e-07 WP=2.3e-07 
Xinvz_in dnand clkn clki dn VDD VSS invz2_par WN=1.5e-07 WP=2.3e-07 
Xinv_ml dn di VDD VSS inv_par WN=2e-07 WP=3e-07 
Xinvz_mfb di clki clkn dn VDD VSS invz_par WN=1.5e-07 WP=2.3e-07 WEAK=1 
Xinvz_ms di clki clkn qin VDD VSS invz_par WN=5e-07 WP=7.5e-07 
Xinv_sl qin qi VDD VSS inv_par WN=3e-07 WP=4.5e-07 
Xinvz_sfb qi clkn clki qin VDD VSS invz_par WN=1.5e-07 WP=1.5e-07 
Xinv_Q qi Q VDD VSS inv_par WN=6.4e-07 WP=9.8e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt DFRQ_D1 D CLK RN Q VDD VSS
XMN0 n0 CLK VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP0 n0 CLK VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN2 n2 RN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN3 n3 D n2 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP2 n3 RN VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP3 n3 D VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN4 n4 n3 n5 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN5 n5 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP4 n4 n3 n6 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP5 n6 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN6 n7 n4 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP6 n7 n4 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN7 n4 n1 n8 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN8 n8 n7 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP7 n4 n0 n9 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP8 n9 n7 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN9 n10 n1 n11 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN10 n11 n7 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMP9 n10 n0 n12 VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ad=2.325e-13 as=2.325e-13 pd=2.12e-06 ps=2.12e-06 ng=1 
XMP10 n12 n7 VDD VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ad=2.325e-13 as=2.325e-13 pd=2.12e-06 ps=2.12e-06 ng=1 
XMN11 n13 n10 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP11 n13 n10 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN12 n10 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP12 n10 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN14 Q n13 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ad=1.984e-13 as=1.984e-13 pd=1.9e-06 ps=1.9e-06 ng=1 
XMP14 Q n13 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ad=3.038e-13 as=3.038e-13 pd=2.58e-06 ps=2.58e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT DFRQ_D1 D CLK RN Q VDD VSS
*.PININFO CLK:I D:I RN:I Q:O VDD:B VSS:B 
MN0 n0 CLK VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP0 n0 CLK VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MN1 n1 n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP1 n1 n0 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN2 n2 RN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN3 n3 D n2 VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP2 n3 RN VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP3 n3 D VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN4 n4 n3 n5 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN5 n5 n0 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP4 n4 n3 n6 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP5 n6 n1 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN6 n7 n4 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP6 n7 n4 VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN7 n4 n1 n8 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN8 n8 n7 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP7 n4 n0 n9 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP8 n9 n7 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN9 n10 n1 n11 VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN10 n11 n7 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MP9 n10 n0 n12 VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ng=1 
MP10 n12 n7 VDD VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ng=1 
MN11 n13 n10 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP11 n13 n10 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MN12 n10 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP12 n10 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MN14 Q n13 VSS VSS sg13_lv_nmos w=6.4e-07 l=1.3e-07 ng=1 
MP14 Q n13 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### DFRQ_D2

#### Hierarchical SPICE netlist
```spice
.subckt DFRQ_D2 D CLK RN Q VDD VSS
Xinv_clkn CLK clkn VDD VSS inv_par WN=4e-07 WP=6e-07 
Xinv_clki clkn clki VDD VSS inv_par WN=3e-07 WP=4.5e-07 
Xnand_in RN D dnand VDD VSS nand2_par WN=3e-07 WP=3.3e-07 
Xinvz_in dnand clkn clki dn VDD VSS invz_par WN=2.5e-07 WP=3.8e-07 
Xinv_ml dn di VDD VSS inv_par WN=3e-07 WP=4.5e-07 
Xinvz_mfb di clki clkn dn VDD VSS invz_par WN=1.5e-07 WP=2.3e-07 WEAK=1 
Xinvz_ms di clki clkn qin VDD VSS invz_par WN=9.2e-07 WP=1.38e-06 
Xinv_sl qin qi VDD VSS inv_par WN=5e-07 WP=7.5e-07 
Xinvz_sfb qi clkn clki qin VDD VSS invz_par WN=1.5e-07 WP=1.5e-07 
Xinv_Q qi Q VDD VSS inv_par WN=1.07e-06 WP=1.6e-06 
.ends
```

#### Flat SPICE netlist
```spice
.subckt DFRQ_D2 D CLK RN Q VDD VSS
XMN0 n0 CLK VSS VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ad=1.24e-13 as=1.24e-13 pd=1.42e-06 ps=1.42e-06 ng=1 
XMP0 n0 CLK VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMN1 n1 n0 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP1 n1 n0 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN2 n2 RN VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN3 n3 D n2 VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP2 n3 RN VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ad=1.023e-13 as=1.023e-13 pd=1.28e-06 ps=1.28e-06 ng=1 
XMP3 n3 D VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ad=1.023e-13 as=1.023e-13 pd=1.28e-06 ps=1.28e-06 ng=1 
XMN4 n4 n0 n5 VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 ng=1 
XMN5 n5 n3 VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ad=7.75e-14 as=7.75e-14 pd=1.12e-06 ps=1.12e-06 ng=1 
XMP4 n4 n1 n6 VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ad=1.178e-13 as=1.178e-13 pd=1.38e-06 ps=1.38e-06 ng=1 
XMP5 n6 n3 VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ad=1.178e-13 as=1.178e-13 pd=1.38e-06 ps=1.38e-06 ng=1 
XMN6 n7 n4 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP6 n7 n4 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ad=1.395e-13 as=1.395e-13 pd=1.52e-06 ps=1.52e-06 ng=1 
XMN7 n4 n1 n8 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN8 n8 n7 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP7 n4 n0 n9 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMP8 n9 n7 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN9 n10 n1 n11 VSS sg13_lv_nmos w=9.2e-07 l=1.3e-07 ad=2.852e-13 as=2.852e-13 pd=2.46e-06 ps=2.46e-06 ng=1 
XMN10 n11 n7 VSS VSS sg13_lv_nmos w=9.2e-07 l=1.3e-07 ad=2.852e-13 as=2.852e-13 pd=2.46e-06 ps=2.46e-06 ng=1 
XMP9 n10 n0 n12 VDD sg13_lv_pmos w=1.38e-06 l=1.3e-07 ad=4.278e-13 as=4.278e-13 pd=3.38e-06 ps=3.38e-06 ng=1 
XMP10 n12 n7 VDD VDD sg13_lv_pmos w=1.38e-06 l=1.3e-07 ad=4.278e-13 as=4.278e-13 pd=3.38e-06 ps=3.38e-06 ng=1 
XMN11 n13 n10 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMP11 n13 n10 VDD VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ad=2.325e-13 as=2.325e-13 pd=2.12e-06 ps=2.12e-06 ng=1 
XMN12 n10 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP12 n10 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMN14 Q n13 VSS VSS sg13_lv_nmos w=1.07e-06 l=1.3e-07 ad=3.317e-13 as=3.317e-13 pd=2.76e-06 ps=2.76e-06 ng=1 
XMP14 Q n13 VDD VDD sg13_lv_pmos w=1.6e-06 l=1.3e-07 ad=4.96e-13 as=4.96e-13 pd=3.82e-06 ps=3.82e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT DFRQ_D2 D CLK RN Q VDD VSS
*.PININFO CLK:I D:I RN:I Q:O VDD:B VSS:B 
MN0 n0 CLK VSS VSS sg13_lv_nmos w=4e-07 l=1.3e-07 ng=1 
MP0 n0 CLK VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MN1 n1 n0 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP1 n1 n0 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MN2 n2 RN VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MN3 n3 D n2 VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP2 n3 RN VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ng=1 
MP3 n3 D VDD VDD sg13_lv_pmos w=3.3e-07 l=1.3e-07 ng=1 
MN4 n4 n0 n5 VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ng=1 
MN5 n5 n3 VSS VSS sg13_lv_nmos w=2.5e-07 l=1.3e-07 ng=1 
MP4 n4 n1 n6 VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ng=1 
MP5 n6 n3 VDD VDD sg13_lv_pmos w=3.8e-07 l=1.3e-07 ng=1 
MN6 n7 n4 VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP6 n7 n4 VDD VDD sg13_lv_pmos w=4.5e-07 l=1.3e-07 ng=1 
MN7 n4 n1 n8 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN8 n8 n7 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP7 n4 n0 n9 VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MP8 n9 n7 VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN9 n10 n1 n11 VSS sg13_lv_nmos w=9.2e-07 l=1.3e-07 ng=1 
MN10 n11 n7 VSS VSS sg13_lv_nmos w=9.2e-07 l=1.3e-07 ng=1 
MP9 n10 n0 n12 VDD sg13_lv_pmos w=1.38e-06 l=1.3e-07 ng=1 
MP10 n12 n7 VDD VDD sg13_lv_pmos w=1.38e-06 l=1.3e-07 ng=1 
MN11 n13 n10 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MP11 n13 n10 VDD VDD sg13_lv_pmos w=7.5e-07 l=1.3e-07 ng=1 
MN12 n10 n0 n14 VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MN13 n14 n13 VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP12 n10 n1 n15 VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MP13 n15 n13 VDD VDD sg13_lv_pmos w=1.5e-07 l=1.3e-07 ng=1 
MN14 Q n13 VSS VSS sg13_lv_nmos w=1.07e-06 l=1.3e-07 ng=1 
MP14 Q n13 VDD VDD sg13_lv_pmos w=1.6e-06 l=1.3e-07 ng=1 
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

