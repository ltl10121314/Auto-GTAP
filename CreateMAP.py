__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"
__altered__ = "2018-5-3"


class CreateMAP(object):
    """Creates the MAP File for use in SLTOTH
    Map gives the list of variables to be exported from the sl4 to the csv results file"""

    __slots__ = ["project_name", "simulation_name", "map_lines"]

    def __init__(self, project_name: str, simulation_name: str, map_lines: list) -> None:
        self.project_name = project_name
        self.simulation_name = simulation_name
        self.map_lines = map_lines

        # Create final file
        with open("gtap.map", "w+") as writer:  # Create the empty file
            writer.writelines(self.map_lines)  # write the line list to the file
