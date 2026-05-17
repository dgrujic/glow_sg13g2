# Standard cell design

Standard digital cell library provides logical and physical views that are used in digital design flow to implement the chip functionality.
Ideally, standard cells should have minimum delay and power - both static and dynamic, while minimizing area and substrate noise injection.
It goes without saying that it is not possible to minimize delay/power/area/noise simultaneously, so a compromise must be made to optimize chosen metrics at the expense of others.

There are two types of standard digital cell libraries: pad ring and core.
- Pad ring cells are connected to chip bonding pads and are arranged into a continuous ring around chip core - hence the name pad ring cells. 
These cells are interface between chip core logic that operates at low voltage (e.g. 1.2 V for 130 nm CMOS) and I/O voltage (e.g. 1.8 or 3.3 V).
They also provide electrostatic discharge (ESD) protection of inputs, outputs and power pins.
- Core cells are used for implementing digital logic in the chip core, and they are usually referred to standard digital cells.

Different designs have different requirements, and there isn't a "one size fits all" standard cell digital library.
To address this issue, some foundries provide several variants (flavours) of standard digital cell libraries that are optimized for different criteria:

- General purpose (GP). GP cells are designed as a compromise of area/delay/power/noise performance, and are suitable for general purpose designs.
- High density (HD). HD cells are optimized for minimum area at expense of delay/power/noise performance. These cells usually don't have n-well/substrate ties to reduce the area, and require the use of special cells for biasing.
Few n-well/substrate ties results in higher substrate noise injection, that could be a problem in mixed-signal designs.
- High performance (HP). Cells are optimized for minimum delay at expense of area/power/noise performance. Area is increased because high performance cells usually contain n-well and substrate ties to pick up charge injected into substrate due to high slew rate and current switching. HP cells can use transistors with lower threshold voltage (low-Vt) to increase the current drive and reduce gate propagation delay. Dynamic power is increased due to higher drive current and operating frequency, but static power is increased as well due to increased leakage of low-Vt transistors. 
- Low noise (LN). Cells are optimized to minimize substrate noise injection. Low noise cells contain n-well and substrate ties connected to a separate rails to minimize substrate noise injection.
- Junction isolated (JI). Junction isolated cells use triple wells to isolate the digital circuits from substrate. JI cells minimize the substrate noise injection.
- Low leakage (LL). Low leakage cells use hight threshold voltage (high-Vt) transistors to minimize leakage current of transistors in off state, and consequently static power.

Regardless of flavour of standard cell library, it consists of several standard cell types:
- Core logic. These cells implement various Boolean functions and memory elements (flip-flops and latches) in variety of drive strengths. Constant '1', called "tie high", and constant '0', called "tie low", cells should be included to avoid connecting transistor gates directly to power and ground.
- Scan chain cells. These cells are used to insert a Design for Test (DFT) scan chain during synthesis. Scan chains are used in automated factory testing to screen for defect chips early.
- Physical cells. These cells do not implement logic, but are needed for physical implementation. Standard cells that do not have integrated n-well and substrate ties require regular placement of special cells that tie n-well to power supply and substrate to ground. Core utilization is never 100%, and filler cells need to be inserted in unplaced sites to connect power and ground rails. Besides connecting the power and ground rails, filler cells also ensure that minimum density of polysilicon and diffusion is met. Alternatively, a cell with capacitor between power and ground can be inserted to provide local power decoupling. Care should be taken when inserting decoupling cells as they are implemented as MOS capacitors that can increase static power due to gate oxide leakage. Some standard cells require placement of special cells at the edges and corners of cell array to satisfy design rules, that are called "end cap" and "corner cap" cells. Finally, "antenna cells" are used to fix antenna DRC errors that occur for large ratio of metal to gate area.

Standard cells should be compact, routed with minimum number of layers - usually only in diffusion, polysilicon and metal 1, so that maximum number metals can be used for routing. 
Cells in advanced nodes might use more than one metal layer to reduce the cell area, but this is offset by large number of available metal layers.

Digital implementation floor planner tool places standard cells in a regular array, as shown in the figure below.
Array rows are separated by alternating horizontal power (VDD) and ground (GND) rails.
Standard cells are Y mirrored in alternating rows to properly connect the power and ground, as is indicated by the orientation mark.

![Standard cell array](figs/stdcells_core.svg)

Router uses pre-defined set of metal track widths and vias (also called "cuts" in a digital flow) for routing. Information about cell geometry and routing is contained in a technology LEF file, that is an integral part of a standard digital library.

## Anatomy of a standard cell

For a cell library to be usable in an automated digital implementation flow, it must conform to some rules:
- Cells must have the same height so that they can be placed in rows.
- Cell width must be an integer multiple of unit cell width.
- Cells must have power and ground rails that can be connected by abutment.
- Cells must conform to DRC rules, even when abutted to any other cell in any valid X/Y mirror condition.
- Cell pins must be on a routing grid and accessible by via without DRC violations.

A standard cell site template shown in the figure below can solve most of the standard cell requirements. 

![Standard cell site](figs/stdcell_site_basic.svg)

Standard cell site template provides:
- Place and Route (PnR) boundary for cell alignment and abutment. Cell layout extends beyond PnR boundary, and when cells are abutted from left, right, top and bottom some parts of layouts overlap. For example, abutting a cell from top or bottom results in overlap of power rails, diffusions and contacts, but the composite layout is still DRC clean.
- Power and ground rails in metal 1.
- N-well for PMOS transistors. Height of n-well is chosen to reflect the different widths of NMOS and PMOS transistors due to different hole and electron mobilities.
- N-well and substrate ties, that include diffusion, P and N implants and contacts to metal 1. Contacts to diffusions are arranged on a grid so they are aligned with cells from rows above and below.
- Height of all cells is guaranteed to be the same, and cell width is always an integer multiple of a unit cell width. Cells have half of unit width on left and right sides to allow seamless abutment of standard cells.
- Routing grid markings, shown in red dashed lines, to explicitly show routing tracks and possible pin placements.
- General keep out areas on the left and right sides of a cell are sized so that minimum spacing rules are satisfied in all cases.
When cells are abutted, keep out areas of adjoining cells are joined, so the width of two keep out areas should be equal to largest minimum spacing rule of layers used in a standard cell. Layout of standard cells uses only diffusion, polysilicon and metal 1, so the width of keep out area is  
`keepout_w = 0.5 * max(min_spacing(diffusion), min_spacing(polysilicon), min_spacing(metal_1))`  
In the case of [IHP SG13G2 process design rules](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/main/ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf) minimum dimensions are
    | Layer       | Minimum spacing |
    |-------------|-----------------|
    | Diffusion   | 210 nm          |
    | Polysilicon | 180 nm          |
    | Metal 1     | 180 nm          |
    | Keep out    | 105 nm          |
- Channel keep out area is determined by DRC rule that sets minimum distance of NMOS transistor channel to n-well and minimum n-well enclosure of PMOS transistor channel. For [IHP SG13G2 process design rules](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/main/ihp-sg13g2/libs.doc/doc/SG13G2_os_layout_rules.pdf) minimum channel keep out distance from n-well edge is determined by rules NW.c and NW.d, and is 310 nm, for a total of 620 nm channel keep out area height.

Standard cell site template can speed up the development of layouts as physical constraints are marked, as well as pin positions. The only thing that remains is to define the unit site size.
Unit site height is traditionally "measured" in the number of horizontal metal tracks that can be routed over the height of a cell - usually 7 metal tracks for high density cell, and 9 or 11 tracks for general purpose and high performance cells, while the width is determined by vertical metal track pitch.

Metal track pitch is constrained by minimum metal width and spacing, although other factors such as design for manufacturability (DFM) or better track utilization may affect the decision on track pitch.
On a first glance, horizontal and vertical track pitch should be the same because it is common that metals used in digital implementation have the same minimum width and spacing.
Metal 1 is an exception and usually has smaller minimum width and spacing to allow more compact routing in standard cells.

In SG13G2 process minimum metal 2 to 5 width is 200 nm and minimum spacing is 210 nm. This results in theoretical minimum for track pitch of 410 nm. Open source IHP standard cell library uses 420 nm pitch for horizontal metals (M2 and M4) and 480 nm for vertical metals (M3 and M5).
Horizontal pitch of 420 nm, instead of minimum of 410 nm, can be attributed to relaxed spacing to increase the yield, but it does not explain why the vertical track pitch is 480 nm.
The reason for larger vertical track pitch is that via connected to metal has to have an endcap overhang (rule Mn.c1 requires 50 nm) that enlarges the metal width.
For a single via, that is usually used for routing digital designs, endcap overhang must be present on at least two sides, resulting in minimum track pitch of 200 + 210 + 50 = 460 nm, that is close to 480 nm used in IHP cells.
Such arrangement reserves space for endcaps only in one dimension, that might result in routing obstruction in dense designs.

GLOW SG13G2 standard cell library is designed to use the same routing pitch for both horizontal and vertical tracks of 480 nm, reserving space for endcaps in both dimensions.
Increasing the horizontal pitch from 420 to 480 nm results in 9 tracks cell height of 4.32 um instead of 3.78 um - about 15% increase in unit cell area.
This area is not wasted for several reasons (numbers for DRC rules are for IHP SG13G2 technology):
- Minimum spacing of well/substrate tie to transistor channel is 300 nm. Together with 150 nm of tap diffusion inside the PnR area results in minium of 450 nm spacing of transistor channel from PnR vertical boundary. Including 620 nm of channel keep out area near n-well edge, it results in 1520 nm of cell height that cannot be used for transistor gates. Nine track cell with horizontal pitch of 420 nm has a total height of 3.78 um, but transistor channels can only occupy height of 2.26 um, while the cell with 480 nm pitch has a total height of 4.32 um, where transistors can occupy height of 2.8 um - an increase of almost 24%. This increase should be understood as a potential for area reduction as 15% of cell area is traded for (potential) 24% increase in transistor area. Not all cells will benefit from space available for wider transistors, but many cells will, especially if transistor dimensions are chosen to maximize the use of available area.
- More space for routing of complex logic inside a standard cell, potentially reducing cell width and overall area.
- Flexibility of via endcaps in both horizontal and vertical tracks might reduce routing obstructions.

# Design flow for standard digital cells

## Netlist design


## Layout design and verification


## Cell characterization


## Abstract view generation


## Standard cell library assembly



