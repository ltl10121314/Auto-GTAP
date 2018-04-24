__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-12"
__altered__ = "2018-3-23"

import shutil
from CreateConfig import CreateConfig


class CopyInputFiles(object):
    """Copies files from the input files directory to the work files directory"""

    __slots__ = ["simulation_name","subfolders_to_copy"]

    def __init__(self, simulation_name: str, subfolders_to_copy: list) -> None:
        self.simulation_name = simulation_name
        self.subfolders_to_copy=subfolders_to_copy

        for input_folder in subfolders_to_copy:
            # copy files with file_name from Input_Files to Work_Files in folder simulation_name
            shutil.copytree('Input_Files\\{0}'.format(input_folder),
                            'Work_Files\\{0}\\{1}'.format(self.simulation_name, input_folder))
