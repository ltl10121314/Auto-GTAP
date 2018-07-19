__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-27"

import os
import subprocess


class AggregateModelData(object):
    """Uses GTAPAgg2 to aggregate raw GTAP data"""

    __slots__ = ["config", "simulation_name", "part_num", "part_work_folder", "agg_scheme_file", "data_subfolder"]

    def __init__(self, config, simulation_name: str, part_num: int) -> None:
        self.config = config
        self.simulation_name = simulation_name
        self.part_num = part_num

        self.part_work_folder = self.config.yaml_file["simulations"][self.simulation_name]["subparts"][self.part_num][
            "work_folder"]

        self.agg_scheme_file = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
            "agg_scheme_file"]
        self.data_subfolder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
            "data_subfolder"]

        old_work_directory = os.getcwd()
        os.chdir("WorkFiles\\" + self.simulation_name + "\\" + self.part_work_folder + "\\GTAP10p2\\GTAP")
        subprocess.call("runagg.bat {0} {1}".format(self.data_subfolder, self.agg_scheme_file))
        os.chdir(old_work_directory)
