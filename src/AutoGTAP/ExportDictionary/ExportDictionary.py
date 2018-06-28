__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-15"

import csv


class ExportDictionary(object):
    """Exports Dictionary of Results as CSV"""

    __slots__ = ["file_name", "database"]

    def __init__(self, file_name: str, database: dict) -> None:
        self.file_name = file_name
        self.database = database

        # Writes the contents of the dictionary to a csv file

        # newline="" is necessary as per https://stackoverflow.com/questions/7200606/python3-writing-csv-files
        with open(self.file_name, 'w+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            header_row = (
                "simulation name", "commodities shocked", "Commodity Description", "variable", "variable property",
                "variable description", "value")
            writer.writerow(header_row)
            for key, value in self.database.items():
                if value != '1.00000000E+10':
                    line = list(key)
                    line.append(value)
                    writer.writerow(line)
