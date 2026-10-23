# NOR4N1

Four input NOR gate with one input inverted

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| AN | Input AN, inverted |
| B | Input B |
| C | Input C |
| D | Input D |
| Y | Output |
| VDD | Power supply |
| VSS | Ground |


## Logic function and Truth table

### Logic function (Python)
<div align="center">
Y = ~(~AN | B | C | D)
</div>

### Logic function (Boolean)
\\[ Y = \overline{\overline{AN} + B + C + D} \\]

### Truth Table for Y


| AN | B | C | D | Y |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 0 | 0 | 0 | 1 | 
| 0 | - | - | - | 0 | 
| - | 1 | - | - | 0 | 
| - | - | 1 | - | 0 | 
| - | - | - | 1 | 0 | 


## Symbol

<div align="center">
<img src="figs/NOR4N1_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/NOR4N1_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [NOR4N1_DL](#nor4n1_dl) | TBD | TBD |
| [NOR4N1_D1](#nor4n1_d1) | TBD | TBD |
| [NOR4N1_D2](#nor4n1_d2) | TBD | TBD |
| [NOR4N1_D4](#nor4n1_d4) | TBD | TBD |



### NOR4N1_DL

#### Hierarchical SPICE netlist
```spice
.subckt NOR4N1_DL AN B C D Y VDD VSS
Xinv AN A VDD VSS inv_par WN=1.5e-07 WP=2.3e-07 
Xnor4 A B C D Y VDD VSS nor4_par WP=6e-07 WN=2e-07 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NOR4N1_DL AN B C D Y VDD VSS
XMN0 n0 AN VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ad=4.65e-14 as=4.65e-14 pd=9.2e-07 ps=9.2e-07 ng=1 
XMP0 n0 AN VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ad=7.13e-14 as=7.13e-14 pd=1.08e-06 ps=1.08e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN2 Y B VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN3 Y C VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMN4 Y D VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP1 n1 D VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP2 n2 C n1 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP3 n3 B n2 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP4 Y n0 n3 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NOR4N1_DL AN B C D Y VDD VSS
*.PININFO C:I B:I D:I AN:I Y:O VDD:B VSS:B 
MN0 n0 AN VSS VSS sg13_lv_nmos w=1.5e-07 l=1.3e-07 ng=1 
MP0 n0 AN VDD VDD sg13_lv_pmos w=2.3e-07 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN2 Y B VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN3 Y C VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MN4 Y D VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP1 n1 D VDD VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MP2 n2 C n1 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MP3 n3 B n2 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
MP4 Y n0 n3 VDD sg13_lv_pmos w=6e-07 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### NOR4N1_D1

#### Hierarchical SPICE netlist
```spice
.subckt NOR4N1_D1 AN B C D Y VDD VSS
Xinv AN A VDD VSS inv_par WN=2e-07 WP=3e-07 
Xnor4 A B C D Y VDD VSS nor4_par 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NOR4N1_D1 AN B C D Y VDD VSS
XMN0 n0 AN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ad=6.2e-14 as=6.2e-14 pd=1.02e-06 ps=1.02e-06 ng=1 
XMP0 n0 AN VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ad=9.3e-14 as=9.3e-14 pd=1.22e-06 ps=1.22e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN2 Y B VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN3 Y C VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMN4 Y D VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ad=1.55e-13 as=1.55e-13 pd=1.62e-06 ps=1.62e-06 ng=1 
XMP1 n1 D VDD VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=1 
XMP2 n2 C n1 VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=1 
XMP3 n3 B n2 VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=1 
XMP4 Y n0 n3 VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=1 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NOR4N1_D1 AN B C D Y VDD VSS
*.PININFO C:I B:I D:I AN:I Y:O VDD:B VSS:B 
MN0 n0 AN VSS VSS sg13_lv_nmos w=2e-07 l=1.3e-07 ng=1 
MP0 n0 AN VDD VDD sg13_lv_pmos w=3e-07 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN2 Y B VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN3 Y C VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MN4 Y D VSS VSS sg13_lv_nmos w=5e-07 l=1.3e-07 ng=1 
MP1 n1 D VDD VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ng=1 
MP2 n2 C n1 VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ng=1 
MP3 n3 B n2 VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ng=1 
MP4 Y n0 n3 VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ng=1 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### NOR4N1_D2

#### Hierarchical SPICE netlist
```spice
.subckt NOR4N1_D2 AN B C D Y VDD VSS
Xinv AN A VDD VSS inv_par WN=6e-07 WP=9e-07 
Xnor4 A B C D Y VDD VSS nor4_par WP=2.2e-06 NGP=2 WN=8e-07 NGN=1 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NOR4N1_D2 AN B C D Y VDD VSS
XMN0 n0 AN VSS VSS sg13_lv_nmos w=6e-07 l=1.3e-07 ad=1.86e-13 as=1.86e-13 pd=1.82e-06 ps=1.82e-06 ng=1 
XMP0 n0 AN VDD VDD sg13_lv_pmos w=9e-07 l=1.3e-07 ad=2.79e-13 as=2.79e-13 pd=2.42e-06 ps=2.42e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMN2 Y B VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMN3 Y C VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMN4 Y D VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ad=2.48e-13 as=2.48e-13 pd=2.22e-06 ps=2.22e-06 ng=1 
XMP1 n1 D VDD VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ad=6.82e-13 as=6.82e-13 pd=5.02e-06 ps=5.02e-06 ng=2 
XMP2 n2 C n1 VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ad=6.82e-13 as=6.82e-13 pd=5.02e-06 ps=5.02e-06 ng=2 
XMP3 n3 B n2 VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ad=6.82e-13 as=6.82e-13 pd=5.02e-06 ps=5.02e-06 ng=2 
XMP4 Y n0 n3 VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ad=6.82e-13 as=6.82e-13 pd=5.02e-06 ps=5.02e-06 ng=2 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NOR4N1_D2 AN B C D Y VDD VSS
*.PININFO C:I B:I D:I AN:I Y:O VDD:B VSS:B 
MN0 n0 AN VSS VSS sg13_lv_nmos w=6e-07 l=1.3e-07 ng=1 
MP0 n0 AN VDD VDD sg13_lv_pmos w=9e-07 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MN2 Y B VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MN3 Y C VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MN4 Y D VSS VSS sg13_lv_nmos w=8e-07 l=1.3e-07 ng=1 
MP1 n1 D VDD VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ng=2 
MP2 n2 C n1 VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ng=2 
MP3 n3 B n2 VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ng=2 
MP4 Y n0 n3 VDD sg13_lv_pmos w=2.2e-06 l=1.3e-07 ng=2 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/empty_cell_layout.svg" height=500/>
</div>

### NOR4N1_D4

#### Hierarchical SPICE netlist
```spice
.subckt NOR4N1_D4 AN B C D Y VDD VSS
Xinv AN A VDD VSS inv_par WN=8.9e-07 WP=1.4e-06 
Xnor4 A B C D Y VDD VSS nor4_par WP=4.41e-06 NGP=3 WN=1.5e-06 NGN=2 
.ends
```

#### Flat SPICE netlist
```spice
.subckt NOR4N1_D4 AN B C D Y VDD VSS
XMN0 n0 AN VSS VSS sg13_lv_nmos w=8.9e-07 l=1.3e-07 ad=2.759e-13 as=2.759e-13 pd=2.4e-06 ps=2.4e-06 ng=1 
XMP0 n0 AN VDD VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ad=4.34e-13 as=4.34e-13 pd=3.42e-06 ps=3.42e-06 ng=1 
XMN1 Y n0 VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ad=4.65e-13 as=4.65e-13 pd=3.62e-06 ps=3.62e-06 ng=2 
XMN2 Y B VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ad=4.65e-13 as=4.65e-13 pd=3.62e-06 ps=3.62e-06 ng=2 
XMN3 Y C VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ad=4.65e-13 as=4.65e-13 pd=3.62e-06 ps=3.62e-06 ng=2 
XMN4 Y D VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ad=4.65e-13 as=4.65e-13 pd=3.62e-06 ps=3.62e-06 ng=2 
XMP1 n1 D VDD VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ad=1.367e-12 as=1.367e-12 pd=9.44e-06 ps=9.44e-06 ng=3 
XMP2 n2 C n1 VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ad=1.367e-12 as=1.367e-12 pd=9.44e-06 ps=9.44e-06 ng=3 
XMP3 n3 B n2 VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ad=1.367e-12 as=1.367e-12 pd=9.44e-06 ps=9.44e-06 ng=3 
XMP4 Y n0 n3 VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ad=1.367e-12 as=1.367e-12 pd=9.44e-06 ps=9.44e-06 ng=3 
.ends
```

#### CDL netlist
```cdl
.SUBCKT NOR4N1_D4 AN B C D Y VDD VSS
*.PININFO C:I B:I D:I AN:I Y:O VDD:B VSS:B 
MN0 n0 AN VSS VSS sg13_lv_nmos w=8.9e-07 l=1.3e-07 ng=1 
MP0 n0 AN VDD VDD sg13_lv_pmos w=1.4e-06 l=1.3e-07 ng=1 
MN1 Y n0 VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ng=2 
MN2 Y B VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ng=2 
MN3 Y C VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ng=2 
MN4 Y D VSS VSS sg13_lv_nmos w=1.5e-06 l=1.3e-07 ng=2 
MP1 n1 D VDD VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ng=3 
MP2 n2 C n1 VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ng=3 
MP3 n3 B n2 VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ng=3 
MP4 Y n0 n3 VDD sg13_lv_pmos w=4.41e-06 l=1.3e-07 ng=3 
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

