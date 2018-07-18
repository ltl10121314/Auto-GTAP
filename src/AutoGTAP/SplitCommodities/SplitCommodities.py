__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-23"

import os
import subprocess


class SplitCommodities(object):
    """Uses MSplitCom to Split a Commodity in a HAR data file"""

    __slots__ = ["har_file_location", "MSplitCom_location", "simulation_name"]

    def __init__(self, simulation_name: str) -> None:
        self.simulation_name = simulation_name

        work_directory = "WorkFiles\\" + self.simulation_name + "\\MSplitCom-Exe"
        os.chdir(work_directory)
        subprocess.call("msplitbat.bat")
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
