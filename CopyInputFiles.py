__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-12"
__altered__ = "2018-3-23"

import shutil


class CopyInputFiles(object):
    """Copies files from the input files directory to the work files directory"""

    __slots__ = ["input_folder", "simulation_name"]

    def __init__(self, input_folder: str, simulation_name: str) -> None:
        self.input_folder = input_folder
        self.simulation_name = simulation_name

    def create(self) -> None:
        # copy files with file_name from Input_Files to Work_Files in folder simulation_name
        shutil.copytree('Input_Files\\{0}'.format(self.input_folder), 'Work_Files\\{0}'.format(self.simulation_name))
