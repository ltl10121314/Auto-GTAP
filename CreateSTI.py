__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"
__altered__ = "2018-5-1"


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
                "bat         		! Run in batch. \n",
                "log		        ! Start a log file \n",
                "b		        	! Output to both terminal and log file \n",
                "sim_{0}_sltoth_sti.log	    	! Name of log file\n".format(self.simulation_name),
                "ses                ! Output to spreadsheet with element labels \n",
                ",                  ! Character to use for data separation \n",
                "shl                ! Show level results, if available \n",
                "                   ! Done selecting general options \n",
                "sim_{0}.sl4            ! Location of sl4 file to convert to csv \n".format(self.simulation_name),
                "c                  ! Want both levels and cumulative from solution file \n",
                "y                  ! Use file to choose which variables and components to ouptut \n",
                "sim_{0}.map            ! Name of file to use choosing which variables and components to output \n".format(
                    self.simulation_name),
                "sim_{0}.csv            ! Name of file to output to".format(self.simulation_name)
            ]
            output_file_name = "sim_{0}_sltoht".format(self.simulation_name)

        # Create final file
        with open("{0}.sti".format(output_file_name), "w+") as writer:  # Create the empty file
            writer.writelines(line_list)  # write the line list to the file
