__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"
__altered__ = "2018-4-30"


class CreateMAP(object):
    """Creates the MAP File for use in SLTOTH
    Map gives the list of variables to be exported from the sl4 to the csv results file"""

    __slots__ = ["project_name", "simulation_name", "map_lines"]

    def __init__(self, project_name: str, simulation_name: str, map_lines: list) -> None:
        self.project_name = project_name
        self.simulation_name = simulation_name
        self.map_lines

        line_list_gas = [
            'pm("Gas","USA")\n',
            'aoall("Gas","USA")\n',
            'qo("Gas","USA")\n',
            'qxw("Gas","USA")\n',
            'qiw("Gas","USA")\n'
            ]

        line_list_oil = [
            'pm("Oil","USA")\n',
            'aoall("Oil","USA")\n',
            'qo("Oil","USA")\n',
            'qxw("Oil","USA")\n',
            'qiw("Oil","USA")\n'
        ]

        # line_list_total = ['pms("c_Crops","EU_28")\n']
        # line_list_total = ['pxwreg("EU_28")\n']
        line_list_total = self.map_lines

        # Create final file
        file_name = self.project_name + "_" + self.simulation_name
        with open("{0}.map".format(file_name), "w+") as writer:  # Create the empty file
            writer.writelines(line_list_total)  # write the line list to the file
