# CLKBUF

Clock buffer for clock tree synthesis

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| A | Buffer input |
| Y | Output |
| VDD | Power supply |
| VSS | Ground |


## Logic function and Truth table

### Logic function (Python)
<div align="center">
Y = A
</div>

### Logic function (Boolean)
\\[ Y = A \\]

### Truth Table for Y


| A | Y |
| :--- | :--- |
| 1 | 1 | 
| 0 | 0 | 


## Symbol

<div align="center">
<img src="figs/CLKBUF_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/CLKBUF_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [CLKBUF_D1](#clkbuf_d1) | TBD | TBD |
| [CLKBUF_D2](#clkbuf_d2) | TBD | TBD |
| [CLKBUF_D3](#clkbuf_d3) | TBD | TBD |
| [CLKBUF_D4](#clkbuf_d4) | TBD | TBD |
| [CLKBUF_D6](#clkbuf_d6) | TBD | TBD |
| [CLKBUF_D8](#clkbuf_d8) | TBD | TBD |
| [CLKBUF_D12](#clkbuf_d12) | TBD | TBD |
| [CLKBUF_D16](#clkbuf_d16) | TBD | TBD |



### CLKBUF_D1

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D1 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=1.5e-07 WP=4.3e-07 
Xinv2 AN Y VDD VSS inv_par WN=3.4000000000000003e-07 WP=9.8e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D1 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=4.3e-07 l=1.3e-07 ad=1.333e-13 as=1.333e-13 pd=1.48e-06 ps=1.48e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=3.4e-07 l=1.3e-07 ad=1.054e-13 as=1.054e-13 pd=1.3e-06 ps=1.3e-06 ng=1 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ad=3.038e-13 as=3.038e-13 pd=2.58e-06 ps=2.58e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D1 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=4.3e-07 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=3.4e-07 l=1.3e-07 ng=1 
MP1 Y n0 VDD VDD sg13_lv_pmos w=9.8e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### CLKBUF_D2

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D2 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=2e-07 WP=5.8e-07 
Xinv2 AN Y VDD VSS inv_par WN=5e-07 WP=1.45e-06 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D2 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=5.8e-07 l=1.3e-07 ad=1.798e-13 as=1.798e-13 pd=1.78e-06 ps=1.78e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=1.45e-06 l=1.3e-07 ad=4.495e-13 as=4.495e-13 pd=3.52e-06 ps=3.52e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D2 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=5.8e-07 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MP1 Y n0 VDD VDD sg13_lv_pmos w=1.45e-06 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### CLKBUF_D3

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D3 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=3e-07 WP=8.7e-07 
Xinv2 AN Y VDD VSS inv_par WN=8e-07 WP=2.2e-06 NGN=1 NGP=2 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D3 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=8.7e-07 l=1.3e-07 ad=2.697e-13 as=2.697e-13 pd=2.36e-06 ps=2.36e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ad=6.82e-13 as=6.82e-13 pd=5.02e-06 ps=5.02e-06 ng=2 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D3 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=3e-07 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=8.7e-07 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MP1 Y n0 VDD VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ng=2 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### CLKBUF_D4

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D4 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=3.6e-07 WP=1.08e-06 
Xinv2 AN Y VDD VSS inv_par WN=1e-06 WP=3e-06 NGN=2 NGP=2 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D4 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=3.6e-07 l=1.3e-07 ad=1.116e-13 as=1.116e-13 pd=1.34e-06 ps=1.34e-06 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=1.08e-06 l=1.3e-07 ad=3.348e-13 as=3.348e-13 pd=2.78e-06 ps=2.78e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ad=3.1e-13 as=3.1e-13 pd=2.62e-06 ps=2.62e-06 ng=2 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=3e-06 l=1.3e-07 ad=9.3e-13 as=9.3e-13 pd=6.62e-06 ps=6.62e-06 ng=2 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D4 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=3.6e-07 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=1.08e-06 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=1e-06 l=1.3e-07 ng=2 
MP1 Y n0 VDD VDD sg13_lv_pmos w=3e-06 l=1.3e-07 ng=2 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### CLKBUF_D6

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D6 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=4.8e-07 WP=1.4399999999999998e-06 
Xinv2 AN Y VDD VSS inv_par WN=1.3e-06 WP=3.9e-06 NGN=2 NGP=2 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D6 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=4.8e-07 l=1.3e-07 ad=1.488e-13 as=1.488e-13 pd=1.58e-06 ps=1.58e-06 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=1.44e-06 l=1.3e-07 ad=4.464e-13 as=4.464e-13 pd=3.5e-06 ps=3.5e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=1.3e-06 l=1.3e-07 ad=4.03e-13 as=4.03e-13 pd=3.22e-06 ps=3.22e-06 ng=2 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=3.9e-06 l=1.3e-07 ad=1.209e-12 as=1.209e-12 pd=8.42e-06 ps=8.42e-06 ng=2 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D6 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=4.8e-07 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=1.44e-06 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=1.3e-06 l=1.3e-07 ng=2 
MP1 Y n0 VDD VDD sg13_lv_pmos w=3.9e-06 l=1.3e-07 ng=2 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### CLKBUF_D8

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D8 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=7.6e-07 WP=2.28e-06 
Xinv2 AN Y VDD VSS inv_par WN=2.2e-06 WP=6.6e-06 NGN=4 NGP=4 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D8 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=7.6e-07 l=1.3e-07 ad=2.356e-13 as=2.356e-13 pd=2.14e-06 ps=2.14e-06 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=2.28e-06 l=1.3e-07 ad=7.068e-13 as=7.068e-13 pd=5.18e-06 ps=5.18e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=2.2e-06 l=1.3e-07 ad=6.82e-13 as=6.82e-13 pd=5.02e-06 ps=5.02e-06 ng=4 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=6.6e-06 l=1.3e-07 ad=2.046e-12 as=2.046e-12 pd=1.382e-05 ps=1.382e-05 ng=4 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D8 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=7.6e-07 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=2.28e-06 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=2.2e-06 l=1.3e-07 ng=4 
MP1 Y n0 VDD VDD sg13_lv_pmos w=6.6e-06 l=1.3e-07 ng=4 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### CLKBUF_D12

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D12 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=1.1e-06 WP=3.3e-06 
Xinv2 AN Y VDD VSS inv_par WN=3.3e-06 WP=9.9e-06 NGN=6 NGP=6 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D12 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=1.1e-06 l=1.3e-07 ad=3.41e-13 as=3.41e-13 pd=2.82e-06 ps=2.82e-06 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=3.3e-06 l=1.3e-07 ad=1.023e-12 as=1.023e-12 pd=7.22e-06 ps=7.22e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=3.3e-06 l=1.3e-07 ad=1.023e-12 as=1.023e-12 pd=7.22e-06 ps=7.22e-06 ng=6 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=9.9e-06 l=1.3e-07 ad=3.069e-12 as=3.069e-12 pd=2.042e-05 ps=2.042e-05 ng=6 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D12 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=1.1e-06 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=3.3e-06 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=3.3e-06 l=1.3e-07 ng=6 
MP1 Y n0 VDD VDD sg13_lv_pmos w=9.9e-06 l=1.3e-07 ng=6 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### CLKBUF_D16

#### Hierarchical SPICE netlist
```spice
.subckt CLKBUF_D16 A Y VDD VSS
Xinv1 A AN VDD VSS inv_par WN=1.4e-06 WP=4.2e-06 
Xinv2 AN Y VDD VSS inv_par WN=4e-06 WP=1.2e-05 NGN=8 NGP=8 
.ends
```

#### Flat SPICE netlist
```spice
.subckt CLKBUF_D16 A Y VDD VSS
XMN0 n0 A VSS VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=1 
XMP0 n0 A VDD VDD sg13_lv_pmos w=4.2e-06 l=1.3e-07 ad=1.302e-12 as=1.302e-12 pd=9.02e-06 ps=9.02e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=4e-06 l=1.3e-07 ad=1.24e-12 as=1.24e-12 pd=8.62e-06 ps=8.62e-06 ng=8 
XMP1 Y n0 VDD VDD sg13_lv_pmos w=1.2e-05 l=1.3e-07 ad=3.72e-12 as=3.72e-12 pd=2.462e-05 ps=2.462e-05 ng=8 
.ends
```

#### CDL netlist
```cdl
.SUBCKT CLKBUF_D16 A Y VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B 
MN0 n0 A VSS VSS sg13_lv_nmos w=1.4e-06 l=1.3e-07 ng=1 
MP0 n0 A VDD VDD sg13_lv_pmos w=4.2e-06 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=4e-06 l=1.3e-07 ng=8 
MP1 Y n0 VDD VDD sg13_lv_pmos w=1.2e-05 l=1.3e-07 ng=8 
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

