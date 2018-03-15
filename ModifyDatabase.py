__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-15"
__altered__ = "2018-3-15"


class ModifyDatabase(object):
    """Cleans database of results to make it more understandable"""

    __slots__ = ["database"]

    def __init__(self, database: dict) -> None:
        self.database = database

    def create(self):
        # Revise database by taking keys to be modified, making changes in new key, and deleting old key#
        outputdatabase = self.database

        for key in list(self.database):
            newkey = list(key)  # define new key to be added

            # Add variable Descriptions
            newkey.append("No Variable Description Available")
            if key[1] == 'pm(FOC_COMM:"USA")': newkey[3] = "Price of Simulation Commodity"

            # Change variable properties to be more understandable
            if key[2] == "Linear": newkey[2] = "Percent Change"
            if key[2] == "Changes": newkey[2] = "Absolute Change"

            # Duplicate simulation name (for use as commodity being shocked)
            newkey.insert(0, newkey[0])

            # Adds column with description of simulation/commodity
            newkey.insert(2, "Unknown Sector")
            if key[0] == "gas": newkey[2] = "Natural Gas"

            # Add newkey to database
            newkey = tuple(newkey)
            outputdatabase[newkey] = outputdatabase[key]
            outputdatabase.pop(key, None)  # Delete old key

        return outputdatabase
