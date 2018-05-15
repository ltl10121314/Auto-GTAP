__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-5-4"
__altered__ = "2018-5-4"


class GTAPAdjustShocks(object):
    """Creates a line list of shocks for insertion into the GTAP-Adjust's CMF file"""

    def __init__(self, shock_type: str) -> None:
        self.shock_type = shock_type

    def create(self):
        # Create lines for shocks

        if self.shock_type == "OceanGrains":
            line_list_shocks = [
                '',
                '!    old exog                new exog   !   ',
                'swap qdem("GrainsCropsA","Oceania")=vCOSTS("GrainsCropsA","Oceania");',
                'final_level  vCOSTS("GrainsCropsA","Oceania")= 50000; ',
                'Verbal Description = Adjust GTAP database  ;'
            ]

        return line_list_shocks
