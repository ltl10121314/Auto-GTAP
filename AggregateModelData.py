__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-27"
__altered__ = "2018-4-27"

import os, subprocess


class AggregateModelData(object):
    """Uses GTAPAgg2 to aggregate raw GTAP data"""

    __slots__ = ["simulation_name"]

    def __init__(self, simulation_name: str) -> None:
        self.simulation_name = simulation_name

        work_directory = "Work_Files\\" + self.simulation_name + "\\GTPAg2\\GTAP10p2\\GTAP"
        os.chdir(work_directory)
        subprocess.call("runagg.bat 2014 default.txt")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
