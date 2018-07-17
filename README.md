# Auto-GTAP

Auto-GTAP combines all steps of running a GTAP-based reasearch project under a single framework.

## Why use Auto-GTAP?

In principle, a GTAP simulation can be run with a single command. However, the reality is that the process tends to be much more complicated. A typical GTAP-based research project will need to build balance a database, calculate shocks, and shuffle around various files at each stage, in addition to running the simulation itself, all before finally exporting simulation results.

While the simulation is an automated process, these ambient task require require user interaction. Auto-GTAP aims to provide a unified framework to lift these ambient tasks into the build toolchain. The goal is to increase the speed and replicability of GTAP-based analyses, by reducing the amount of manual orchestration required.

## Getting started

### Prerequisites

TODO: describe the environment

Mandatory
- Python 3.6 (other versions untested)
- Pyyaml 4.2bt (other versions untested)

Additional requirements for GTAP-E Validation advanced example
- GEMPACK 14.0 (other versions untested, requires license from CoPS)

Additional requirements for Productivity Increase advanced example
- GEMPACK 14.0 (other versions untested, requires license from CoPS)

This specific "Raw GTAP Data" above was taken from the PR2_v10_2014_Sep2017 release of GTAPg2. It was located in 

``GTPAg2\GTAP10p2\GTAP\2014``

and should be placed in

``Auto-GTAP\examples\productivity_increase\InputFiles\GTPAg2\GTAP10p2\GTAP\2014``

 
 
### Clone the repository 
 
 ```bash
cd your_project_directory

git clone https://github.com/andre-barbe/Auto-GTAP.git
```

### Create a Python virtual environment
 
```bash
python -m venv venv 
```

### Initialize the workspace

```bash
./setup.ps1
```

- Create WorkFiles folders at

```bash
Auto-GTAP\examples\gtap-e-validation-advanced\WorkFiles
Auto-GTAP\examples\gtap-e-validation-simple\WorkFiles
Auto-GTAP\examples\productivity_increase-advanced\WorkFiles
Auto-GTAP\examples\productivity_increase-simple\WorkFiles

```

- Put Raw GTAP Data in subfolder of InputFiles for your aggregation program

## Example projects

- [Productivity Increase (Simple)](examples/productivity-increase-simple)
- [Productivity Increase (Advanced)](examples/productivity-increase-advanced)
- [GTAP-E Validation (Simple)](examples/gtap-e-validation-simple)
- [GTAP-E Validation (Advanced)](examples/gtap-e-validation-advanced)

## Documentation

- [Components of Auto-GTAP](docs/components-of-auto-gtap.md)

## References

- [Corong et al. 2017](https://jgea.org/resources/jgea/ojs/index.php/jgea/article/view/47)