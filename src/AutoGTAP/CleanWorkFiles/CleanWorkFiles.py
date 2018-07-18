__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"

import os
import shutil


class CleanWorkFiles(object):
    """Deletes contents of given directories"""

    def __init__(self) -> None:
        # From https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
        directories_to_clean = ['WorkFiles', 'OutputFiles']
        for directory in directories_to_clean:
            for the_file in os.listdir(directory):
                file_path = os.path.join(directory, the_file)
                try:
                    # deletes entry if it is a file
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # deletes entry if it is a folder
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
