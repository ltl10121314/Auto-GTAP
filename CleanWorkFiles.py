__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"
__altered__ = "2018-3-23"

import os, shutil


class CleanWorkFiles(object):
    """Delete files from work directory and subfolder in it"""

    __slots__ = ["input_directory_list"]

    def __init__(self, input_directory_list: list) -> None:
        self.input_directory_list = input_directory_list

        # Delete folders in work_files
        folders_to_delete = ['Work_Files//{0}'.format(folder) for folder in self.input_directory_list]
        for folder in folders_to_delete:
            # the try/except structure prevents an error if the folder does not exist
            try:
                shutil.rmtree(folder)
            except OSError:
                pass

        #Delete files in work files
        folder = 'Work_Files'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            # the try/except structure prevents an error if the folder does not exist
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
