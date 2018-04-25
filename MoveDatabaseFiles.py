__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-25"
__altered__ = "2018-4-25"

class MoveDatabaseFiles(object):
    """Moves files. Typically moves the output of one module to the input of another module"""

    __slots__ = ["source","destination"]

    def __init__(self, source: str, destination:str) -> None:
        self.source=source
        self.destination=destination

        if self.source=="flexagg21":
            flexagg_output_folder="flexagg21\\output"
            source_flows_file="".format(flexagg_output_folder)
            source_parameters_file = "".format(flexagg_output_folder)
            source_sets_file="".format(flexagg_output_folder)
        
        if self.source=="MSplitCom-Exe":
            source_flows_file=""
            source_parameters_file = ""
            source_sets_file=""
        
        if self.destination=="MSplitCom-Exe":
            destination_flows_file=""
            destination_parameters_file = ""
            destination_sets_file=""

        if self.destination == "GTAP-V6":
            destination_flows_file = ""
            destination_parameters_file = ""
            destination_sets_file = ""
