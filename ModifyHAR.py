__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-28"
__altered__ = "2018-3-28"

import subprocess


class ModifyHAR(object):
    """Modifies the values of a HAR file"""

    __slots__ = ["input_file", "output_file"]

    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.CreateSTI()
        subprocess.call("modhar -sti command.sti")

    def CreateSTI(self) -> None:
        # Create lines for sti file that controls modhar
        line_list = [
            "bat\n",
            "\n",
            "y\n",
            self.input_file+".har\n",  # old filename
            self.output_file+".prm\n",  # new filename
            "mw\n",
            "EPEN\n",  # header to modify
            "m\n",
            "r\n",
            "o\n",
            "5\n",
            "16\n",
            "w\n",
            "n\n",
            "ex\n",
            "a\n",
            "0\n"]

        # Create final file
        with open("command.sti", "w+") as writer:  # Create the empty file
            writer.writelines(line_list)  # write the line list to the file
