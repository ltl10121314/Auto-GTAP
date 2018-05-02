__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-27"
__altered__ = "2018-4-27"

import os, subprocess


class AggregateModelData(object):
    """Uses GTAPAgg2 to aggregate raw GTAP data"""

    __slots__ = ["simulation_name", "part_work_folder"]

    def __init__(self, simulation_name: str, part_work_folder: str) -> None:
        self.simulation_name = simulation_name
        self.part_work_folder = part_work_folder

        work_directory = "Work_Files\\" + self.simulation_name + "\\" + self.part_work_folder + "\\GTAP10p2\\GTAP"
        os.chdir(work_directory)
        subprocess.call("runagg.bat 2014 default.txt")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
