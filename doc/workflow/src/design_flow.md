# Design flow

This chapter is work in progress, and only steps to generate CDL and SPICE netlists are complete so far.

When individual cells have been designed, they should be assembled into a library.
The cell manifest holds information about all cells in a library, and a collection of tools is used to:
- Check the cell manifest,
- Generating cells and their CDL and SPICE netlists,
- Checking cell layouts,
- Generating the library databook.

The following chapters show how to perform these steps.

## Checking the cell manifest

First the cell manifest should be checked by
```sh
cd $GLOW_ROOT/cells
checkmanifest cell_manifest.yaml --all
```
This command checks if the manifest is correct, and checks all cells against specification given in manifest, and produces the output
```
********************************************************************************
Reading manifest file : cell_manifest.yaml
Running checks on cells :
AND2_D1 AND2_D2 AND2_D4 AND2_DL AND3_D1 AND3_D2 AND3_D4 AND3_DL AND4_D1 AND4_D2 AND4_D4 AND4_DL AO21_D1 AO21_D2 AO
21_DL AO22_D1 AO22_D2 AO22_DL AOI211_D1 AOI211_D2 AOI211_DL AOI21_D1 AOI21_D2 AOI21_DL AOI221_D1 AOI221_DL AOI222_
D1 AOI222_DL AOI22_D1 AOI22_DL AOI2N1_D1 AOI2N1_D2 AOI2N1_DL AOI2N2_D1 BUF_D1 BUF_D12 BUF_D2 BUF_D3 BUF_D4 BUF_D6 
BUF_D8 BUF_DL CLKBUF_D1 CLKBUF_D12 CLKBUF_D16 CLKBUF_D2 CLKBUF_D3 CLKBUF_D4 CLKBUF_D6 CLKBUF_D8 CLKINV_D1 CLKINV_D
16 CLKINV_D2 CLKINV_D4 CLKINV_D8 DFARQN_D1 DFARQN_DL DFARQQN_D1 DFARQQN_DL DFARQ_D1 DFARQ_DL DFASQN_D1 DFASQN_DL D
FASQQN_D1 DFASQQN_DL DFASQ_D1 DFASQ_DL DFEQN_D1 DFEQN_D2 DFEQN_DL DFEQQN_D1 DFEQQN_D2 DFEQQN_DL DFEQ_D1 DFEQ_D2 DF
EQ_DL DFERQN_D1 DFERQN_D2 DFERQN_DL DFERQQN_D1 DFERQQN_D2 DFERQQN_DL DFERQ_D1 DFERQ_D2 DFERQ_DL DFESQN_D1 DFESQN_D
2 DFESQN_DL DFESQQN_D1 DFESQQN_D2 DFESQQN_DL DFESQ_D1 DFESQ_D2 DFESQ_DL DFQN_D1 DFQN_D2 DFQN_D4 DFQN_DL DFQQN_D1 D
FQQN_D2 DFQQN_D4 DFQQN_DL DFQ_D1 DFQ_D2 DFQ_D4 DFQ_DL DFRQN_D1 DFRQN_D2 DFRQN_DL DFRQQN_D1 DFRQQN_D2 DFRQQN_DL DFR
Q_D1 DFRQ_D2 DFRQ_DL DFSQN_D1 DFSQN_D2 DFSQN_DL DFSQQN_D1 DFSQQN_D2 DFSQQN_DL DFSQ_D1 DFSQ_D2 DFSQ_DL DLN_D1 DLN_D
2 DLN_DL DL_D1 DL_D2 DL_DL INV_D1 INV_D12 INV_D14 INV_D16 INV_D2 INV_D4 INV_D8 INV_DL MUX2N_D1 MUX2N_DL MUX2_D1 MU
X2_DL MUX3_D1 MUX3_DL MUX4_D1 MUX4_DL NAND2_D1 NAND2_D2 NAND2_D4 NAND2_D8 NAND2_DL NAND3_D1 NAND3_D2 NAND3_D4 NAND
3_DL NAND4N1_D1 NAND4N1_D2 NAND4N1_DL NAND4N2_D1 NAND4N2_D2 NAND4N2_DL NAND4_D1 NAND4_D2 NAND4_D4 NAND4_DL NOR2_D1
 NOR2_D2 NOR2_D4 NOR2_D8 NOR2_DL NOR3_D1 NOR3_D2 NOR3_D4 NOR3_DL NOR4N1_D1 NOR4N1_D2 NOR4N1_D4 NOR4N1_DL NOR4N2_D1
 NOR4N2_D2 NOR4N2_DL NOR4_D1 NOR4_D2 NOR4_D4 NOR4_DL OA21_D1 OA21_D2 OA21_D4 OA21_DL OA22_D1 OA22_D2 OA22_DL OAI21
1_D1 OAI211_DL OAI221_D1 OAI221_DL OAI222_D1 OAI222_DL OAI22_D1 OAI22_DL OR2_D1 OR2_D2 OR2_D4 OR2_DL OR3_D1 OR3_D2
 OR3_D4 OR3_DL OR4_D1 OR4_D2 OR4_D4 OR4_DL TIEH TIEL XNOR2_D1 XNOR2_DL XOR2_D1 XOR2_DL
********************************************************************************
Checking cell AND2_D1
Succesfully imported and generated Python code.
Cell and manifest pins match.
Symsim::Elaborate: Circuit is flat.
Symsim::Elaborate: Circuit passes ERC.
Symsim::Elaborate: Inputs  : A B
Symsim::Elaborate: Outputs : Y
Symsim::Elaborate: Power   : VDD
Symsim::Elaborate: Ground  : VSS
Symsim::Elaborate: Nodes   : A B VDD VSS Y n0 n1
Symsim::Elaborate: Elaboration OK.
********************************************************************************

⋮

Gate logic functions :
	(A & ~B) | (B & ~A)
Expected logic functions :
	A ^ B
Function A ^ B successfully mapped to (A & ~B) | (B & ~A)
	Symbol mapping : 
	A -> A
	B -> B
Cell check function from manifest specification OK
ALL OK [218]
```
`ALL OK` at the end of report means that checks on all cells have passed.
On success the script returns 0 as exit value that can be used for checking the status programmatically.

## Generating cells and their CDL and SPICE netlists

The next step is to generate CDL and SPICE netlists for all cells by running
``` sh
cd $GLOW_ROOT/cells
batch_gencell cell_manifest.yaml --all --parallel 0
```
At the end of report there should be a message
```
ALL OK [218]
```
that signifies that all of the cells pass internal checks and that netlists have been succesfully generated.

Individual cell netlists can be packed to a single netlist file by running
``` sh
cd $GLOW_ROOT/cells
packnetlists cell_manifest.yaml --all
```
If the command succedes, the end of report should contain
```
ALL OK
```
Full CDL netlist will be available at `$GLOW_ROOT/library/cdl/glow_sg13g2.cdl`, 
while the SPICE netlist will be available at `$GLOW_ROOT/library/spice/glow_sg13g2.sp`.

## Checking cell layouts

Cell layouts should be checked for conformance to conventions and user-defined rules, as well as foundry DRC and LVS.
These checks are performed by `check_cell.sh` script, and are:
- Layout passes `gdsinfo` check
    ```
    gdsinfo file.gds -c cell_name --noref --errlay *,* --uselay 1,0 --uselay 5,0 --uselay 6,0 --uselay 8,0 --uselay 8,2 --uselay 8,25 --uselay 14,0 --uselay 31,0 --uselay 189,* --label VDD --label VSS --nolabel 'vdd!' --nolabel 'vss!'
    ```
    - Argument `--noref` forces that a cell has flat hierarchy,
    - Argument `--errlay *,*` marks all layers and purposes as error layers, and individual `--uselay` arguments explicitly allow only specific layers,
    - Arguments `--label VDD` and `--label VSS` require that pins with labels `VDD` and `VSS` are present,
    - Arguments `--nolabel 'vdd!'` and `--nolabel 'vss!'` forbid the use of global labels `vdd!` and `vss!`.
- Layout passed DRC check. This check ensures that the cell is manufacturable.
- Layout passed LVS check. This check ensures that the cell netlist and layout match.

## Generating the library databook

Databook reports can be generated by running
``` sh
cd $GLOW_ROOT/cells
genreport cell_manifest.yaml --all --summary
```
If reports are generated succesfully the end of report should be:
```
Generating summary...	OK
Generating introduction...	OK
ALL OK [70]
```
