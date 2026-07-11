# Installation

This section covers steps to install and setup GLOW SG13G2 flow.

First a Python virtual environment should be installed.
Steps for [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) are given in the following text, although any other alternative should work equally well.
After the Miniconda is installed, it should be activated
```sh
source <path_to_miniconda>/bin/activate
```
Optinally restrict Miniconda to only use free community packages with
```sh
conda config --add channels conda-forge
conda config --set channel_priority strict
```
Create a new environment called `glow` with Python version 3.12:
```sh
conda create -n glow python=3.12
```
If the environment was created previously skip this step.

Activate the `glow` environment
```sh
conda activate glow
```
and then install `pip`
```sh
conda install pip
```

Set the variable pointing to GLOW path
```sh
export GLOW_ROOT=<path_to_GLOW>
```
Install `glow_utils` package
```sh
cd $GLOW_ROOT/code/glow_utils
pip install -e .
```
Flag `-e` is usefull for development as changes in package's Python files are immediatelly visible, without the need for package reinstallation. Omit `-e` flag if you don't plan to change the source code.

GLOW can be tested by running test scripts, for example:
```sh
python test_symsim_nand2.py
```
that produces the output
```
Symsim::Elaborate: Circuit is flat.
Symsim::Elaborate: Circuit passes ERC.
Symsim::Elaborate: Inputs  : A B
Symsim::Elaborate: Outputs : Y
Symsim::Elaborate: Power   : VDD
Symsim::Elaborate: Ground  : VSS
Symsim::Elaborate: Nodes   : VDD A B Y n0 VSS
Symsim::Elaborate: Elaboration OK.
****************************************
Determining gate logic function.
Symsim::combSim: Simulating circuit with 2 inputs and 1 outputs.
Symsim::combSim: | 11 | 0
Symsim::combSim: | 10 | 1
Symsim::combSim: | 01 | 1
Symsim::combSim: | 00 | 1
Gate logic function is ~A | ~B
Circuit is OK
Circuit function matches the expected Boolean function.
Circuit function does not match the wrong Boolean function.
```

GLOW targets IHP SG13G2 process and its PDK should be downloaded from
```
https://github.com/IHP-GmbH/IHP-Open-PDK
```
and installed per [installation instructions](https://ihp-open-pdk-docs.readthedocs.io/en/latest/install.html).
Setup of IHP PDK exports two variables `PDK` and `PDK_ROOT` and we will assume that they are correctly set.
If not already installed, IHP PDK Python requirements can be installed in `glow` environment as
```sh
pip install -r $PDK_ROOT/requirements.txt
```
This commands installs, amongst other things, KLayout Python bindings that are used for DRC and LVS checks.

Testing of DRC and LVS can be performed with the following commands:
```sh
cd $GLOW_ROOT/cells/INV_D1
gencell INV_D1
$GLOW_ROOT/code/scripts/check_cell.sh INV_D1.gds INV_D1
```
that runs `gdsinfo` based checks, DRC and LVS, and should produce an output
```
Checking INV_D1	 | GDSINFO OK	 | DRC OK	 | LVS OK	 | ALL OK
```
meaning that all checks have passed.
