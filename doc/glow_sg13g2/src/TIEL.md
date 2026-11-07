# TIEL

Tie low cell - constant logic '0'.

## Pin information

| Pin   | Description   |
| :-:    | :-            |
| Y | Output |
| VDD | Power supply |
| VSS | Ground |


## Logic function and Truth table

### Logic function (Python)
<div align="center">
Y = 0
</div>

### Logic function (Boolean)
\\[ Y = 0 \\]

### Truth Table for Y


| Y |
| :--- |
| 0 | 


## Symbol

<div align="center">
<img src="figs/TIEL_sym.svg" />
</div>

## Schematic

<div align="center">
<img src="figs/TIEL_sch.svg" />
</div>

## Cell variants

| Cell name <br> | Width <br> [unit sites] | Area <br> [\\(\mu m^2\\)] |
| :-        | :-:   | :-:   |
| [TIEL](#tiel) | 2 | 4.1472 |



### TIEL

#### Hierarchical SPICE netlist
```spice
.subckt TIEL Y VDD VSS
XMN0 Y G VSS VSS sg13_lv_nmos w=7.7e-07 l=1.3e-07 ad={7.7e-07*3.1e-07} as={7.7e-07*3.1e-07} pd={2*(7.7e-07+3.1e-07)} ps={2*(7.7e-07+3.1e-07)} 
XMP0 G G VDD VDD sg13_lv_pmos w=7.7e-07 l=1.3e-07 ad={7.7e-07*3.1e-07} as={7.7e-07*3.1e-07} pd={2*(7.7e-07+3.1e-07)} ps={2*(7.7e-07+3.1e-07)} 
.ends
```

#### Flat SPICE netlist
```spice
.subckt TIEL Y VDD VSS
XMN0 Y n0 VSS VSS sg13_lv_nmos w=7.7e-07 l=1.3e-07 ad=2.387e-13 as=2.387e-13 pd=2.16e-06 ps=2.16e-06 
XMP0 n0 n0 VDD VDD sg13_lv_pmos w=7.7e-07 l=1.3e-07 ad=2.387e-13 as=2.387e-13 pd=2.16e-06 ps=2.16e-06 
.ends
```

#### CDL netlist
```cdl
.SUBCKT TIEL Y VDD VSS
*.PININFO Y:O VDD:B VSS:B 
MN0 Y n0 VSS VSS sg13_lv_nmos w=7.7e-07 l=1.3e-07 
MP0 n0 n0 VDD VDD sg13_lv_pmos w=7.7e-07 l=1.3e-07 
.ENDS
```

#### Layout

<div align="center">
<img src="figs/TIEL.svg" height=500/>
</div>

## Pin capacitance
No pin capacitance data


## Static power
No static power data


## Dynamic power
No dynamic power data


## Delay
No delay data

