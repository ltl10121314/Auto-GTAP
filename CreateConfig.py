__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-15"
__altered__ = "2018-3-23"

import yaml


class CreateConfig(object):
    """Creates config information from yaml file"""

    __slots__ = ["yaml_file_location", "yaml_file", "simulation_list", "input_directory_list", "model_csv_paths"]

    def __init__(self, yaml_file_location: str) -> None:
        with open(yaml_file_location, 'r') as f:
            self.yaml_file = yaml.load(f)

        self.simulation_list = self.yaml_file["simulations_to_run"]

        self.input_directory_list = []
        self.model_csv_paths = []
        for simulation in self.simulation_list:
            self.input_directory_list.append(self.sim_property(simulation, "input_directory"))
            model_csv_path = simulation + "//" + self.sim_property(simulation,
                                                                   "input_directory") + "//sim_" + simulation + ".csv"
            self.model_csv_paths.append(model_csv_path)

    def sim_property(self, simulation_name: str, property_name: str):
        return self.yaml_file["simulations"][simulation_name][property_name]

    def subfolders_to_copy(self, simulation_name: str):
        simulation_folder = self.yaml_file["simulations"][simulation_name]["input_directory"]

        try:
            other_folders = self.yaml_file["simulations"][simulation_name]["other_input_directories"]
        except ImportError:
            other_folders = []

        all_folders = [simulation_folder] + other_folders

        return all_folders

    def num_parts(self, simulation_name:str):
        return len(self.yaml_file["simulations"][simulation_name]["subparts"])
