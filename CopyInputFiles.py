__author__ = "Andre Barbe"
__project__ = "GTAP-E-Validation"
__created__ = "2018-3-12"
__altered__ = "2018-3-12"

import shutil


class CopyInputFiles(object):
    """Copies files from the input files directory to the work files directory"""

    __slots__ = ["input_directory_list"]

    def __init__(self, input_directory_list: list) -> None:
        self.input_directory_list = input_directory_list

    def create(self) -> None:
        # Define lists of files to copy.

        for folder in self.input_directory_list:
            # copy files with file_name from Input_Files to Work_Files
            shutil.copytree('Input_Files\\{0}'.format(folder), 'Work_Files\\{0}'.format(folder))
