__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-15"
__altered__ = "2018-3-15"

import yaml


class ReadYaml(object):
    """Creates config information from yaml file"""

    __slots__ = ["yaml_file_location"]

    def __init__(self, yaml_file_location: str) -> None:
        self.yaml_file_location = yaml_file_location

    def create(self) -> None:
        # Import control variables from yaml
        with open(self.yaml_file_location, 'r') as f:
            yaml_file = yaml.load(f)
        # Define control variables from yaml
        config.solution_method = yaml_file["solution_method"]
        config.gtap_file_name = yaml_file["gtap_file_name"]
        config.input_directory_list = yaml_file["input_directory_list"]
        config.simulation_name = "hello"
        config.simulation_list = [simulation_name]
        return config
