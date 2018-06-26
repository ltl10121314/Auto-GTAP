# Auto-GTAP Read Me

Auto-GTAP project is a project to create a modern cross-platform project format for CGE research.

## Overview

In principle, a GTAP simulation can be run with a single command. However, the reality is that the
process tends to be much more complicated. A typical GTAP-based research project will need to build
balance a database, calculate shocks, and shuffle around various files at each stage, in addition
to running the simulation itself, all before finally exporting simulation results.

While the simulation is an automated process, these ambient task require require user interaction.
Auto-GTAP aims to provide a unified framework to lift these ambient tasks into the build toolchain.
The goal is to increase the speed and replicability of GTAP-based analyses, by reducing the amount
of manual orchestration required historically.

## Why Auto-GTAP?

The Global Trade Analysis Project (GTAP) model was developed in [19XX]() to estimate the effect
of government policies on international trade.

The popularity of the GTAP modeling framework is due in large part to the ecosystem of tools and 
model extensions developed and contributed by researchers over years.

Alongside the canonical model, contributors have developed numerous extensions to focus on a variety
of topics such as [energy](), [biofuels](), and [electricity](). 

Developers have also created a number of other software tools for dealing with the anciliary issues 
that crop up in these research projects, especially with databases. There are tools automating the 
process of data [aggregation](https://www.gtap.agecon.purdue.edu/products/packages.asp), 
[disaggregation](https://www.gtap.agecon.purdue.edu/resources/splitcom.asp), 
[other](https://www.copsmodels.com/archivep.htm) types of 
[revisions](https://www.copsmodels.com/webhelp/rungtap/index.html?hc_altertax.htm). The existence 
of these tools makes it possible for developers to tailor the model for their specific project.

However, some parts of a GTAP-based research have not been automated. In particular, there is no 
overarching framework controlling both the model and all these tools: the process of running the 
tools, specifying their settings, and moving the output to the input of other tools must all be 
done manually.

Auto-GTAP provides a framework to define a proper toolchain in GTAP-based research projects.

## Getting started

### Prerequisites

TODO: describe the environment
 
 
### Clone the repository 
 
 ```powershell
cd your_project_directory

git clone https://github.com/andre-barbe/Auto-GTAP.git
```

### Create a Python virtual environment
 
 ```powershell
python -m venv venv 
```

### Initialize the workspace

```powershell
./setup.ps1
```

## Example projects

TODO

- [Hello World!](examples/hello_world_example)
- [Free Trade Agreement](examples/free_trade_agreement_example)

## Documentation

- [Components of Auto-GTAP](docs/components-of-auto-gtap.md)