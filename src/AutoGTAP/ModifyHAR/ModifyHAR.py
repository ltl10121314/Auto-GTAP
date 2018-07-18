__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-28"


class ModifyHAR(object):
    """Modifies the values of a HAR file"""

    __slots__ = ["input_file", "output_file", "sti_file", "modifications"]

    def __init__(self, input_file: str, output_file: str, modifications: list) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.sti_file = "cmd_modify_har.sti"
        self.modifications = modifications
        self.CreateSTI()

    def CreateSTI(self) -> None:
        # Create lines for sti file that controls modhar
        line_list_start = [
            "bat",
            "",
            "y",
            self.input_file + ".har",  # old filename
            self.output_file + ".prm"  # new filename
            #
            # "mw",  # task menu: modify and write
            # "EFNC",  # header to modify
            # "m",  #subcommand: modify the data
            # "s",  # scale entries of array
            # "w",  # whole matrix to be scaled
            # "s",  # multiply by scalar or matrix
            # "0.1",  # value of scalar
            # "w",  # write it to new file
            # "n",  # reuse array again?
            #
        ]
        line_list_modifications = []

        for modification in self.modifications:
            header = modification[0]
            location = modification[1]
            value = modification[2]
            line_list_new_mod = [
                "mw",  # task menu: modify and write
                "{0}".format(header),  # header to modify
                "m",  # subcommand: modify the data
                "r",  # replace entries of array
                "o",  # one entry to be changed
                "{0}".format(location),  # entry to be changed
                "{0}".format(value),  # value of replacement
                "w",  # write it to new file
                "n"  # reuse array again?
            ]

            #
            line_list_modifications = line_list_modifications + line_list_new_mod

        # "mw",  # task menu: modify and write
        # "ESBM",  # header to modify ESBD
        # "m",  # subcommand: modify the data
        # "r",  # replace entries of array
        # "o",  # one entry to be changed
        # "4",  # entry to be changed
        # "0.2",  # value of replacement
        # "w",  # write it to new file
        # "n",  # reuse array again?

        line_list_end = [
            "ex",  # task menu: exit, saving changes
            "a",  # transfer all remaining arrays
            "0"  # do not add history for the new file
        ]

        line_list_total = line_list_start + line_list_modifications + line_list_end

        # Create final file
        with open(self.sti_file, "w+") as writer:  # Create the empty file
            writer.writelines(line + '\n' for line in line_list_total)  # write the line list to the file
