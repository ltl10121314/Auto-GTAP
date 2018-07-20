# Auto-GTAP

Auto-GTAP combines all steps of running a GTAP-based research project into a single automated framework.

## Why use Auto-GTAP?

In principle, a GTAP simulation can be run with a single command. However, GTAP-based research projects usually contain more than just the model simulation. A project may also need to build a database, change aggregations, modify parameters, calculate shocks, or run multiple simulations, all the while shuffle around various files at each stage. While a single model simulation is already automated, these other task are not.

Auto-GTAP combines all these tasks into a single automated framework. By reducing the amount of manual orchestration required to run a GTAP project, Auto-GTAP will increase the speed and replicability of your analysis.

## Getting started

### Prerequisites

Mandatory
- Python 3.6 (other versions untested)
- Pyyaml 4.2b4 (other versions untested)

Additional requirements for GTAP-E Validation advanced example
- GEMPACK 14.0 (other versions untested, [purchase information](https://www.copsmodels.com/gempack.htm))

Additional requirements for Productivity Increase advanced example
- GEMPACK 14.0 (other versions untested, [purchase information](https://www.copsmodels.com/gempack.htm))
- GTAP Data File v10_2014 ([purchase information](https://www.gtap.agecon.purdue.edu/databases/default.asp))
 
### Clone the repository 
 
 ```bash
cd your_project_directory

git clone https://github.com/andre-barbe/Auto-GTAP.git
```

### Create a Python virtual environment
 
```bash
python -m venv venv 
```

### Running the program
- Script path: Main.py
- Working directory: Depends on example, e.g. examples\productivity-increase-simple

### (Optional) Prepare Productivity Increase advanced example

Put Raw GTAP Data in subfolder of InputFiles for your aggregation program. This specific "Raw GTAP Data" above was taken from the PR2_v10_2014_Sep2017 release of GTAPg2. It was located in 

``GTPAg2\GTAP10p2\GTAP\2014``

and should be placed in

``Auto-GTAP\examples\productivity_increase\InputFiles\GTPAg2\GTAP10p2\GTAP\2014``

## Example projects

- [Productivity Increase (Simple)](examples/productivity-increase-simple)
- [Productivity Increase (Advanced)](examples/productivity-increase-advanced)
- [GTAP-E Validation (Simple)](examples/gtap-e-validation-simple)
- [GTAP-E Validation (Advanced)](examples/gtap-e-validation-advanced)

## Documentation

- [Components of Auto-GTAP](docs/components-of-auto-gtap.md)
- [GTAP Prior to Auto-GTAP](docs/gtap-prior-to-auto-gtap.md)