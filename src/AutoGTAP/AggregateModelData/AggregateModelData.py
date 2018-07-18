__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-27"

import os
import subprocess


class AggregateModelData(object):
    """Uses GTAPAgg2 to aggregate raw GTAP data"""

    __slots__ = ["simulation_name", "part_work_folder", "agg_scheme_file", "data_subfolder"]

    def __init__(self, simulation_name: str, part_work_folder: str, agg_scheme_files: str, data_subfolder: str) -> None:
        self.simulation_name = simulation_name
        self.part_work_folder = part_work_folder
        self.agg_scheme_file = agg_scheme_files
        self.data_subfolder = data_subfolder

        work_directory = "WorkFiles\\" + self.simulation_name + "\\" + self.part_work_folder + "\\GTAP10p2\\GTAP"
        os.chdir(work_directory)
        subprocess.call("runagg.bat {0} {1}".format(data_subfolder, agg_scheme_files))

        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
