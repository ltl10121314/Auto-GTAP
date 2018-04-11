__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-28"
__altered__ = "2018-4-11"

import subprocess


class ModifyHAR(object):
    """Modifies the values of a HAR file"""

    __slots__ = ["directory", "input_file", "output_file", "sti_file", "modifications"]

    def __init__(self, directory: str, input_file: str, output_file: str, modifications: list) -> None:
        self.directory= directory
        self.input_file = directory+"\\"+ input_file
        self.output_file = directory+"\\"+output_file
        self.sti_file=directory+"\\cmd_modify_har.sti"
        self.modifications = modifications
        self.CreateSTI()
        subprocess.call("modhar -sti {0}".format(self.sti_file))

    def CreateSTI(self) -> None:
        # Create lines for sti file that controls modhar
        line_list1 = [
            "bat\n",
            "\n",
            "y\n",
            self.input_file + ".har\n",  # old filename
            self.output_file + ".prm\n",  # new filename
            "mw\n",
            "EPEN\n",  # header to modify
            "m\n",
            "r\n",  # replace entries of array
            "o\n",  # *one* entry
            "5\n",
            "16\n",
            "w\n",
            "n\n",
            "ex\n",
            "a\n",
            "0\n"]

        line_list_start = [
            "bat\n",
            "\n",
            "y\n",
            self.input_file + ".har\n",  # old filename
            self.output_file + ".prm\n"  # new filename
            #
            # "mw\n",  # task menu: modify and write
            # "EFNC\n",  # header to modify
            # "m\n",  #subcommand: modify the data
            # "s\n",  # scale entries of array
            # "w\n",  # whole matrix to be scaled
            # "s\n",  # multiply by scalar or matrix
            # "0.1\n",  # value of scalar
            # "w\n",  # write it to new file
            # "n\n",  # reuse array again?
            #
        ]
        line_list_modifications = []

        for modification in self.modifications:
            header = modification[0]
            location = modification[1]
            value = modification[2]
            line_list_new_mod = [
                "mw\n",  # task menu: modify and write
                "{0}\n".format(header),  # header to modify
                "m\n",  # subcommand: modify the data
                "r\n",  # replace entries of array
                "o\n",  # one entry to be changed
                "{0}\n".format(location),  # entry to be changed
                "{0}\n".format(value),  # value of replacement
                "w\n",  # write it to new file
                "n\n"  # reuse array again?
            ]

            #
            line_list_modifications = line_list_modifications + line_list_new_mod

        # "mw\n",  # task menu: modify and write
        # "ESBM\n",  # header to modify ESBD
        # "m\n",  # subcommand: modify the data
        # "r\n",  # replace entries of array
        # "o\n",  # one entry to be changed
        # "4\n",  # entry to be changed
        # "0.2\n",  # value of replacement
        # "w\n",  # write it to new file
        # "n\n",  # reuse array again?

        line_list_end = [
            "ex\n",  # task menu: exit, saving changes
            "a\n",  # transfer all remaining arrays
            "0\n"  # do not add history for the new file
        ]

        line_list_total = line_list_start + line_list_modifications + line_list_end

        # Create final file
        with open(self.sti_file, "w+") as writer:  # Create the empty file
            writer.writelines(line_list_total)  # write the line list to the file
