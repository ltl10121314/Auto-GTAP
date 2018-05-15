__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-18"
__altered__ = "2018-5-10"


class Shocks(object):
    """Creates a line list of shocks for insertion into the GTAP CMF file"""

    def __init__(self, shock_type: str) -> None:
        self.shock_type = shock_type

    def create(self):
        # Create lines for shocks

        if self.shock_type == "pop5":
            line_list_shocks = ['Shock pop(REG) = uniform 5;']

        if self.shock_type == "gdp5":
            line_list_shocks = [
                'Swap qgdp(REG) = aoreg(REG);',
                'Shock qgdp(REG) = uniform 5;'
            ]

        if self.shock_type == "alterto5":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);",
                "xSubset REG1 is subset of REG;",
                "xSet XREG = REG - REG1;",
                'swap dtbalr(XREG) = cgdslack(XREG);'
                'Shock to(NSAV_COMM,REG) = uniform 5;'
            ]

        # This shock doesn't actually work
        if self.shock_type == "alterto7target":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);",
                "xSubset REG1 is subset of REG;",
                "xSet XREG = REG - REG1;",
                'swap dtbalr(XREG) = cgdslack(XREG);'
                'Shock to(NSAV_COMM,REG) = target% 7 from file to.shk;'
            ]

        if self.shock_type == "altertms3final":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);",
                "xSubset REG1 is subset of REG;",
                "xSet XREG = REG - REG1;",
                'swap dtbalr(XREG) = cgdslack(XREG);'
                'final_level tms(TRAD_COMM,REG,REG) = uniform 103;'
            ]

        if self.shock_type == "pfactorworld":
            line_list_shocks = ['Shock pfactwld = uniform 10;']


        """Creates a line list of shocks for insertion into the GTAP-Adjust's CMF file"""
        if self.shock_type == "OceanGrains":
            line_list_shocks = [
                '\n',
                '!    old exog                new exog   !   \n',
                'swap qdem("GrainsCropsA","Oceania")=vCOSTS("GrainsCropsA","Oceania");\n',
                'final_level  vCOSTS("GrainsCropsA","Oceania")= 50000; \n',
                'Verbal Description = Adjust GTAP database  ;\n'
            ]

        return line_list_shocks
