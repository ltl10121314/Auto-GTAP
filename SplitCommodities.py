__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-23"
__altered__ = "2018-4-27"

import os, subprocess


class SplitCommodities(object):
    """Uses MSplitCom to Split a Commodity in a HAR data file"""

    __slots__ = ["har_file_location", "MSplitCom_location", "simulation_name"]

    def __init__(self, simulation_name: str) -> None:
        self.simulation_name = simulation_name
        # self.har_file_location =
        # self.MSplitCom_location =

        work_directory = "Work_Files\\" + self.simulation_name + "\\MSplitCom-Exe"
        os.chdir(work_directory)
        subprocess.call("msplitbat.bat")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
