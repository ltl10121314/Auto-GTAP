__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-15"
__altered__ = "2018-3-23"

import yaml


class CreateConfig(object):
    """Creates config information from yaml file"""

    __slots__ = ["yaml_file_location", "yaml_file"]

    def __init__(self, yaml_file_location: str) -> None:
        with open(yaml_file_location, 'r') as f:
            self.yaml_file = yaml.load(f)

    def simulation_list(self):
        return self.yaml_file["simulations_to_run"]

    def input_directory_list(self):
        list = []
        for simulation in self.simulation_list():
            list.append(self.sim_property(simulation, "input_directory"))
        return list

    def sim_property(self, simulation_name: str, property_name: str):
        return self.yaml_file["simulations"][simulation_name][property_name]
