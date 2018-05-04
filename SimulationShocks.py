__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-18"
__altered__ = "2018-5-3"


class SimulationShocks(object):
    """Creates a line list of shocks for insertion into the simulation's CMF file"""

    def __init__(self, shock_type: str) -> None:
        self.shock_type = shock_type

    def create(self):
        # Create lines for shocks

        if self.shock_type == "pop5":
            line_list_shocks = ['Shock pop(REG) = uniform 5;\n']

        if self.shock_type == "gdp5":
            line_list_shocks = [
                'Swap qgdp(REG) = aoreg(REG);\n',
                'Shock qgdp(REG) = uniform 5;\n'
            ]

        if self.shock_type == "alterto5":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);\n",
                "xSubset REG1 is subset of REG;\n",
                "xSet XREG = REG - REG1;\n",
                'swap dtbalr(XREG) = cgdslack(XREG);\n'
                'Shock to(NSAV_COMM,REG) = uniform 5;\n'
            ]

        # This shock doesn't actually work
        if self.shock_type == "alterto7target":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);\n",
                "xSubset REG1 is subset of REG;\n",
                "xSet XREG = REG - REG1;\n",
                'swap dtbalr(XREG) = cgdslack(XREG);\n'
                'Shock to(NSAV_COMM,REG) = target% 7 from file to.shk;\n'
            ]

        if self.shock_type == "altertms3final":
            line_list_shocks = [
                "xSet REG1 (RestofWorld);\n",
                "xSubset REG1 is subset of REG;\n",
                "xSet XREG = REG - REG1;\n",
                'swap dtbalr(XREG) = cgdslack(XREG);\n'
                'final_level tms(TRAD_COMM,REG,REG) = uniform 103;\n'
            ]

        if self.shock_type == "pfactorworld":
            line_list_shocks = ['Shock pfactwld = uniform 10;\n']

        return line_list_shocks
