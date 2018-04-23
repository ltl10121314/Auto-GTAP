__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-12"
__altered__ = "2018-3-23"

import shutil


class CopyInputFiles(object):
    """Copies files from the input files directory to the work files directory"""

    __slots__ = ["conif", "simulation"]

    def __init__(self, input_folder: str, simulation_name: str) -> None:
        self.simulation = simulation_name
        self.input_folder = self.yaml_file["simulations"][simulation_name]["input_directory"]



        # copy files with file_name from Input_Files to Work_Files in folder simulation_name
        shutil.copytree('Input_Files\\{0}'.format(self.input_folder),
                        'Work_Files\\{0}\\{1}'.format(self.simulation, self.input_folder))
