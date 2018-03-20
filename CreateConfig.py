__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-15"
__altered__ = "2018-3-15"

import yaml


class CreateConfig(object):
    """Creates config information from yaml file"""

    __slots__ = ["yaml_file_location"]

    def __init__(self, yaml_file_location: str) -> None:
        self.yaml_file_location = yaml_file_location

    def create(self) -> None:
        # Import control variables from yaml
        with open(self.yaml_file_location, 'r') as f:
            yaml_file = yaml.load(f)

        # Define control variables from yaml

        self.solution_method = yaml_file["Validate GTAP-E"]["solution_method"]
        self.gtap_file_name = yaml_file["Validate GTAP-E"]["gtap_file_name"]
        self.input_directory_list = yaml_file["Validate GTAP-E"]["input_directory_list"]
        self.simulation_name = "hello"
        self.simulation_list = [self.simulation_name]
