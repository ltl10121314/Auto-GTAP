__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-25"
__altered__ = "2018-4-25"

import shutil

class MoveDatabaseFiles(object):
    """Moves files. Typically moves the output of one module to the input of another module"""

    __slots__ = ["source", "destination", "files", "simulation_name"]

    def __init__(self, simulation_name: str, source: str, destination: str) -> None:
        self.simulation_name = simulation_name
        self.source=source
        self.destination=destination

        work_directory = "Work_Files\\" + self.simulation_name + "\\"

        if self.source == "GTPAg2":
            flexagg_output_folder = work_directory + "GTPAg2\\GTAP10p2\\GTAP\\output"
            source_flows_file = "{0}\\basedata.har".format(flexagg_output_folder)
            source_parameters_file = "{0}\\default.prm".format(flexagg_output_folder)
            source_sets_file = "{0}\\sets.har".format(flexagg_output_folder)
            source_tax_rates_file = "{0}\\baserate.har".format(flexagg_output_folder)
            source_view_file = "{0}\\baseview.har".format(flexagg_output_folder)

        
        if self.source=="MSplitCom-Exe":
            source_folder = work_directory + "MSplitCom-Exe\\output"
            source_flows_file = "{0}\\basedata.har".format(source_folder)
            source_parameters_file = "{0}\\default.prm".format(source_folder)
            source_sets_file = "{0}\\sets.har".format(source_folder)
            source_tax_rates_file = "{0}\\taxrates.har".format(source_folder)
            source_view_file = "{0}\\gtapview.har".format(source_folder)
        
        if self.destination=="MSplitCom-Exe":
            destination_folder = work_directory + "MSplitCom-Exe\\input"
            destination_flows_file = "{0}\\basedata.har".format(destination_folder)
            destination_parameters_file = "{0}\\default.prm".format(destination_folder)
            destination_sets_file = "{0}\\sets.har".format(destination_folder)
            destination_tax_rates_file = "{0}\\baserate.har".format(destination_folder)
            destination_view_file = "{0}\\baseview.har".format(destination_folder)

        if self.destination == "GTAP-V6":
            destination_flows_file = ""
            destination_parameters_file = ""
            destination_sets_file = ""

        if self.destination == "GTAP-V7":
            destination_folder = work_directory + "GTAP-V7"
            destination_flows_file = "{0}\\basedata.har".format(destination_folder)
            destination_parameters_file = "{0}\\default.prm".format(destination_folder)
            destination_sets_file = "{0}\\sets.har".format(destination_folder)
            destination_tax_rates_file = "{0}\\baserate.har".format(destination_folder)
            destination_view_file = "{0}\\baseview.har".format(destination_folder)

        self.files = {
            "flows": [source_flows_file, destination_flows_file],
            "parameters": [source_parameters_file, destination_parameters_file],
            "sets": [source_sets_file, destination_sets_file],
            "tax_rates": [source_tax_rates_file, destination_tax_rates_file],
            "view": [source_view_file, destination_view_file],
        }

        for key, value in self.files.items():
            shutil.copy(value[0], value[1])
