__author__ = "Andre Barbe"
__project__ = "GTAP-E-Validation"
__created__ = "2018-3-12"
__altered__ = "2018-3-12"

import shutil


class CopyInputFiles(object):
    """Copies files from the input files directory to the work files directory"""

    # __slots__ = []

    def create(self) -> None:
        # Define lists of files to copy.
        files_gtap = [
            "gtap.tab",
            "basedata.har",
            "baserate.har",
            "baseview.har",
            "sets.har",
            "default.prm"
        ]

        files_other = [
        ]

        list_of_files_to_copy = files_gtap + files_other

        for file_name in list_of_files_to_copy:
            # copy files with file_name from Input_Files to Work_Files
            shutil.copy('Input_Files\\{0}'.format(file_name), 'Work_Files\\{0}'.format(file_name))
