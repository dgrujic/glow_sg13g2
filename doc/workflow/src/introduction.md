# Introduction

Open source tools, and complete design flows, for the design of digital ASICs were readily available for some time, and what was lacking was foundry support.
Process information and Process Design Kits (PDKs) were behind NDA wall, limiting availability and virtually eliminating the possibility of open chip designs.
Furthermore, PDKs were designed for proprietary EDA tools that are prohibitively expensive and subject to restricted availability.

That has changed when some foundries, such as Skywater, Global Foundries and IHP Microelectronics, have released open source PDKs.
Open source PDK discloses the details of a process, such as layout design rules and device models, that enable the design and layout of manufacturable custom analog and digital circuits.

Availability of open source tools *and* PDKs has spurred open chip design and innovation.
However, having access to device models and layout design rules is not enough for building a complex SoC, as it requires the use of many IPs.
Open source community has developed many digital IPs, and the development has accelerated by the use of higher level hardware design languages.
Power, performance and area (PPA) are metrics of digital IPs that not only depend on the quality of RTL code, but also on the standard cell library used for implementation.

There isn't a single metric for quality of standard cell library, as the library can be designed for minimum area, low leakage, high speed etc.
In principle, any digital circuit can be implemented with only a NAND (or a NOR) gate and a storage element (flip-flop), but that would result in a suboptimal design.
Better PPA can be achieved if the standard cell library has more logic gate types in various drive strengths.
Therefore, it is desirable for a digital standard cell library to have as many logic gates and storage elements in different drive strengths as possible.

The following sections cover the role and uses of a digital standard cell library in a digital design flow.
A [short overview of digital design flow](./digital_flow_overview.md) summarizes the steps and tools used in the design of digital SoC.
The section on [design of a standard cell](./standard_cell_design.md) goes into details of all aspects of cell design.
[Design flow](./design_flow.md) section covers the details of generating the standard cell library from individual cell netlists and layouts.



