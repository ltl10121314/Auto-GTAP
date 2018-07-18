__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-18"


class Shocks(object):
    """Creates a line list of shocks for insertion into the GTAP CMF file"""

    def __init__(self, shock_type: str) -> None:
        self.shock_type = shock_type

    def create(self):
        # Create lines for shocks

        """Creates a line list of shocks for insertion into the GTAP-Adjust's CMF file"""

        if self.shock_type == "pop5":
            line_list_shocks = ['Shock pop(REG) = uniform 5;']

        elif self.shock_type == "gdp5":
            line_list_shocks = [
                'Swap qgdp(REG) = aoreg(REG);',
                'Shock qgdp(REG) = uniform 5;'
            ]

        elif self.shock_type == "alterto5":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);",
                "xSubset REG1 is subset of REG;",
                "xSet XREG = REG - REG1;",
                'swap dtbalr(XREG) = cgdslack(XREG);'
                'Shock to(NSAV_COMM,REG) = uniform 5;'
            ]

        elif self.shock_type == "alterto7target":
            # This shock doesn't actually work
            line_list_shocks = [
                "xSet REG1 (RestofWorld);",
                "xSubset REG1 is subset of REG;",
                "xSet XREG = REG - REG1;",
                'swap dtbalr(XREG) = cgdslack(XREG);'
                'Shock to(NSAV_COMM,REG) = target% 7 from file to.shk;'
            ]

        elif self.shock_type == "altertms3final":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);",
                "xSubset REG1 is subset of REG;",
                "xSet XREG = REG - REG1;",
                'swap dtbalr(XREG) = cgdslack(XREG);'
                'final_level tms(TRAD_COMM,REG,REG) = uniform 103;'
            ]

        elif self.shock_type == "pfactorworld":
            line_list_shocks = ['Shock pfactwld = uniform 10;']

        elif self.shock_type == "OceanGrains":
            line_list_shocks = [
                '',
                '!    old exog                new exog   !   ',
                'swap qdem("GrainsCropsA","Oceania")=vCOSTS("GrainsCropsA","Oceania");',
                'final_level  vCOSTS("GrainsCropsA","Oceania")= 50000; ',
                'Verbal Description = Adjust GTAP database  ;'
            ]

        else:
            raise ValueError('Unexpected shock type: %s' % self.shock_type)

        return line_list_shocks
