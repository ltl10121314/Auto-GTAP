__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-12"
__altered__ = "2018-3-23"

import shutil
from CreateConfig import CreateConfig


class CopyInputFiles(object):
    """Copies files from the input files directory to the work files directory"""

    __slots__ = ["simulation_name", "input_folder", "work_folder"]

    def __init__(self, simulation_name: str, input_folder: str, work_folder: str) -> None:
        self.simulation_name = simulation_name
        self.input_folder = input_folder
        self.work_folder = work_folder

        shutil.copytree('Input_Files\\{0}'.format(input_folder),
                        'Work_Files\\{0}\\{1}'.format(self.simulation_name, input_folder))
