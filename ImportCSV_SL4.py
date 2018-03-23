__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-15"
__altered__ = "2018-3-23"

from typing import List


class ImportCSV_SL4(object):
    """Imports the CSV Files created by SLTOHT"""

    __slots__ = ["simulation_list"]

    def __init__(self, simulation_list: List[str]) -> None:
        self.simulation_list = simulation_list

    def filecontents(self, simulation_name) -> List[str]:
        """
        Reads the CSV file into memory
        :return:
        """
        filename = "sim_{0}.csv".format(simulation_name)
        filepath = "Work_Files//" + simulation_name + "//" + filename
        with open(filepath, "r") as reader:  # Read the csv file
            return [line for line in reader.readlines() if
                    line != " \n"]  # deletes lines that are nothing but line breaks

    def create(self) -> dict:
        """
        Takes the CSV file of lines and returns a dictionary of cleaned values
        :return:
        """
        variable_values = {}
        for simulation in self.simulation_list:
            name_variable = []

            list_variable_properties = [
                "Linear",
                "PreLevel",
                "PostLevel",
                "Changes"
            ]

            for line in self.filecontents(simulation):
                # checks if line contains name of variable by looking if it begins with "! The" and ends with "#" and a line break
                if line[0:7] == " ! The " and line[-5:] == "part\n":
                    # Variable name is between the 7th character of the line and the first space after that character
                    name_variable = (line[7:].split(" "))[0]

                if name_variable != []:
                    if line.split(",")[0].strip() in list_variable_properties:
                        # line defines name of matrix if its equal to array name followed by "("
                        variable_index = line.split(",")[0].strip()
                        variable_value = line.split(",")[1].strip()
                        key = (simulation, name_variable, variable_index)
                        variable_values[key] = variable_value

        return variable_values
