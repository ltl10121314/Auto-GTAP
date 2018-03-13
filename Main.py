__author__ = "Andre Barbe"
__project__ = "GTAP-E-Validation"
__created__ = "2018-3-9"
__altered__ = "2018-3-12"

# Import methods
# Import External Methods
import yaml

# Import My Methods
from CleanWorkFiles import CleanWorkFiles
from CopyInputFiles import CopyInputFiles

# Import control variables from yaml
with open('config.yaml', 'r') as f:
    config = yaml.load(f)
# Define control variables from yaml
solution_method = config["solution_method"]
gtap_file_name = config["gtap_file_name"]

# Call Methods
# Setup files for running GEMSIM
CleanWorkFiles().create()
CopyInputFiles().create()
