__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-25"
__altered__ = "2018-5-2"

import shutil


class MoveDatabaseFiles(object):
    """Moves files. Typically moves the output of one module to the input of another module"""

    __slots__ = ["source_type", "destination_type", "files", "simulation_name", "source_part_folder",
                 "destination_part_folder"]

    def __init__(self, simulation_name: str, source_type: str, destination_type: str, source_part_folder: str,
                 destination_part_folder: str) -> None:
        self.simulation_name = simulation_name
        self.source_type = source_type
        self.destination_type = destination_type
        self.source_part_folder = source_part_folder
        self.destination_part_folder = destination_part_folder

        source_part_folder = "Work_Files\\" + self.simulation_name + "\\" + self.source_part_folder + "\\"
        destination_part_folder = "Work_Files\\" + self.simulation_name + "\\" + self.destination_part_folder + "\\"

        if self.source_type == "GTPAg2":
            flexagg_output_folder = source_part_folder + "GTAP10p2\\GTAP\\output\\"
            source_flows_file = "{0}basedata.har".format(flexagg_output_folder)
            source_parameters_file = "{0}default.prm".format(flexagg_output_folder)
            source_sets_file = "{0}sets.har".format(flexagg_output_folder)
            source_tax_rates_file = "{0}baserate.har".format(flexagg_output_folder)
            source_view_file = "{0}baseview.har".format(flexagg_output_folder)

        if self.source_type == "MSplitCom-Exe":
            source_folder = source_part_folder + "output\\"
            source_flows_file = "{0}basedata.har".format(source_folder)
            source_parameters_file = "{0}default.prm".format(source_folder)
            source_sets_file = "{0}sets.har".format(source_folder)
            source_tax_rates_file = "{0}taxrates.har".format(source_folder)
            source_view_file = "{0}gtapview.har".format(source_folder)

        if self.destination_type == "MSplitCom-Exe":
            destination_folder = destination_part_folder + "input\\"
            destination_flows_file = "{0}basedata.har".format(destination_folder)
            destination_parameters_file = "{0}default.prm".format(destination_folder)
            destination_sets_file = "{0}sets.har".format(destination_folder)
            destination_tax_rates_file = "{0}baserate.har".format(destination_folder)
            destination_view_file = "{0}baseview.har".format(destination_folder)

        if self.destination_type == "GTAP-V7" or self.destination_type == "GTAP-V6" or self.destination_type == "Shocks-V6":
            destination_folder = destination_part_folder
            destination_flows_file = "{0}basedata.har".format(destination_folder)
            destination_parameters_file = "{0}default.prm".format(destination_folder)
            destination_sets_file = "{0}sets.har".format(destination_folder)
            destination_tax_rates_file = "{0}baserate.har".format(destination_folder)
            destination_view_file = "{0}baseview.har".format(destination_folder)

        if self.source_type == "GTAP-V7" or self.source_type == "GTAP-V6":
            source_folder = source_part_folder
            source_flows_file = "{0}gtap.har".format(source_folder)
            source_parameters_file = "{0}default.prm".format(source_folder)
            source_sets_file = "{0}sets.har".format(source_folder)

        if self.destination_type == "GTPVEW-V6":
            destination_folder = destination_part_folder
            destination_flows_file = "{0}gtap.har".format(destination_folder)
            destination_parameters_file = "{0}default.prm".format(destination_folder)
            destination_sets_file = "{0}sets.har".format(destination_folder)

        if self.source_type == "GTPVEW-V6":
            source_folder = source_part_folder
            source_flows_file = "{0}gtap.har".format(source_folder)
            source_parameters_file = "{0}default.prm".format(source_folder)
            source_sets_file = "{0}sets.har".format(source_folder)
            source_tax_rates_file = "{0}newrate.har".format(source_folder)
            source_view_file = "{0}newview.har".format(source_folder)

        if self.source_type == "Shocks-V6":
            source_folder = source_part_folder
            source_flows_file = "{0}basedata.har".format(source_folder)
            source_parameters_file = "{0}default.prm".format(source_folder)
            source_sets_file = "{0}sets.har".format(source_folder)
            source_tax_rates_file = "{0}baserate.har".format(source_folder)
            source_view_file = "{0}baseview.har".format(source_folder)

        self.files = {
            "flows": [source_flows_file, destination_flows_file],
            "parameters": [source_parameters_file, destination_parameters_file],
            "sets": [source_sets_file, destination_sets_file],
        }
        if self.source_type != "GTAP-V6":
            self.files["tax_rates"] = [source_tax_rates_file, destination_tax_rates_file]
            self.files["view"] = [source_view_file, destination_view_file]

        # Shock files only need to be created once, and then only updated if tax rates change. So they can be moved around constantly
        # if self.destination_type != "Shocks-V6" and (
        #         self.source_type == "GTAP-V6" or self.source_type == "GTAP-V7" or self.source_type == "GTPVEW-V6" or self.source_type == "Shocks-V6"):
        #     shockfiles = ["to", "tf", "tpi", "tpd", "tgi", "tgd", "tfi", "tfd", "txs", "tms"]
        #     for shockfile in shockfiles:
        #         self.files[shockfile] = [source_folder + shockfile + ".shk", destination_folder + shockfile + ".shk"]

        for key, value in self.files.items():
            shutil.copy(value[0], value[1])
