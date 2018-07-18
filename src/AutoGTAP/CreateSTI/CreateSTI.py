__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"


class CreateSTI(object):
    """Creates an STI File for controlling SLTOHT
    SLTOHT exports variables from the .sl4 file to a .csv file
    The STI file tells SLTOHT where its input and output files are"""

    # Also creates STI files for PGSing .tab files

    __slots__ = ["input_file_name", "simulation_name", "sti_type"]

    def __init__(self, input_file_name: str, simulation_name: str, sti_type: str) -> None:
        self.input_file_name = input_file_name
        self.simulation_name = simulation_name
        self.sti_type = sti_type

        # Create list of lines to write to STI file
        if self.sti_type == "sltoht":
            line_list = [
                # First, select general options
                "bat         		! Run in batch. ",
                "log		        ! Start a log file ",
                "b		        	! Output to both terminal and log file ",
                "{0}_sltoht.log	    	! Name of log file".format(self.input_file_name),
                "ses                ! Output to spreadsheet with element labels ",
                ",                  ! Character to use for data separation ",
                "shl                ! Show level results, if available ",
                "                   ! Done selecting general options ",
                "{0}.sl4            ! Location of sl4 file to convert to csv ".format(self.input_file_name),
                "c                  ! Want both levels and cumulative from solution file ",
                "y                  ! Use file to choose which variables and components to output ",
                "{0}.map            ! Name of file to use choosing which variables and components to output ".format(
                    self.input_file_name),
                "{0}.csv            ! Name of file to output to".format(self.input_file_name)
            ]
            output_file_name = "{0}_sltoht".format(self.input_file_name)

        else:
            raise ValueError('Unexpected sti type: %s' % self.sti_type)

        # Create final file
        with open("{0}.sti".format(output_file_name), "w+") as writer:  # Create the empty file
            writer.writelines(line + '\n' for line in line_list)  # write the line list to the file
