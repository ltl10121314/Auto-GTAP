__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-12"

import shutil
import distutils.dir_util


class CopyInputFiles(object):
    """Copies files from the input files directory to the work files directory"""

    __slots__ = ["config", "simulation_name", "part_num", "input_folder", "work_folder"]

    def __init__(self, config: dict, simulation_name: str, part_num: int) -> None:
        self.config = config
        self.simulation_name = simulation_name
        self.part_num = part_num

        self.input_folder = self.config.yaml_file["simulations"][self.simulation_name]["subparts"][self.part_num][
            "input_folder"]
        self.work_folder = self.config.yaml_file["simulations"][self.simulation_name]["subparts"][self.part_num][
            "work_folder"]

    def copy(self):
        shutil.copytree('InputFiles\\{0}'.format(self.input_folder),
                        'WorkFiles\\{0}\\{1}'.format(self.simulation_name, self.work_folder))

        for additional_input_folder in self.config.part_additional_input_folders(self.simulation_name, self.part_num):
            # need to use this copy method to overwrite files/folders (or copy files to folders that already exist)
            distutils.dir_util.copy_tree("InputFiles\{0}".format(additional_input_folder),
                                         "WorkFiles\{0}\{1}".format(self.simulation_name, self.work_folder))
