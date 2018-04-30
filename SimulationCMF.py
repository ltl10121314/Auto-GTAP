__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"
__altered__ = "2018-4-30"

from SimulationShocks import SimulationShocks

class SimulationCMF(object):
    """Creates an CMF file for controlling gemsim when it runs the policy simulation (as opposed to the shock
    calculation)"""

    __slots__ = ["project", "simulation_name", "solution_method", "model_folder", "shock_type", "model_type"]

    def __init__(self, project: str, simulation_name: str, solution_method: str, model_folder: str,
                 shock_type: str, model_type: str) -> None:
        self.project = project
        self.simulation_name = simulation_name
        self.solution_method = solution_method
        self.model_folder = model_folder
        self.shock_type = shock_type
        self.model_type = model_type


    def shockedsectors(self):
        list_shocked_sectors = self.simulation_name
        return list_shocked_sectors

    def create(self, shocked_sector: str) -> None:

        cmf_file_name = self.project + "_" + self.simulation_name + ".cmf"
        # Create list of lines to be added to CMF file

        # Create lines for solution method
        if self.solution_method == "default_j":
            line_list_method = [
                "Method = Johansen;\n",
                "Steps = 1;\n",
                "automatic accuracy = no;\n",
                "subintervals = 1;\n",
                "\n"]
        elif self.solution_method == "default_g":
            line_list_method = [
                "Method = Gragg; Steps = 2 4 6; subintervals = 10;\n",
                "automatic accuracy = yes ; accuracy figures = 4; accuracy percent = 99;\n",
                "minimum subinterval length = 1.0E-0003;\n",
                "minimum subinterval fails = stop;\n",
                "accuracy criterion = Solution;\n",
                "\n"]
        else:
            raise ValueError('Unknown solution method in CMF')

        # Create lines for header that gives file locations
        if self.model_type == "gtap-e":
            line_list_header = [
            "CPU = yes; ! log show simulation times\n",
            "NDS = no ; ! no displays\n",
            "Extrapolation accuracy file = NO ; ! No XAC file\n",
            "log file=yes;\n",
            "aux files = GTAP;\n",
            "file gtapSETS = sets.har;\n",
            "file gtapDATA = basedata.har;\n",
            "Updated file gtapDATA = <cmf>.har;\n",
            "\n",
            "file gtapPARM = default.prm;\n",
            "\n",
            "Verbal Description = none;\n",
            "\n"]

            # Create lines that define which variables are endogeneous and exogeneous
            line_list_exogendo = [
                "exogenous\n",
                "    afall\n",
                "    afcom\n",
                "    afreg\n",
                "    afsec    \n",
                "    ams\n",
                "    aoall\n",
                "    aoreg\n",
                "    aosec\n",
                "  ! atall               omitted\n",
                "    atd\n",
                "    atf\n",
                "    atm\n",
                "    ats\n",
                "    au\n",
                "    cgdslack\n",
                "    del_ctgshr\n",
                "    dpgov\n",
                "    dppriv\n",
                "    dpsave\n",
                "    endwslack\n",
                "    incomeslack\n",
                "    pemp\n",
                "    pfactwld\n",
                "    pop\n",
                "    profitslack\n",
                "    psaveslack\n",
                "    qo(ENDW_COMM,REG)\n",
                "    RCTAXB\n",
                "  ! tf                  omitted\n",
                "    tfd\n",
                "    tfm\n",
                "    tgd\n",
                "    tgm\n",
                "    tm\n",
                "    tms\n",
                "    to\n",
                "    tpd\n",
                "    tpm\n",
                "    tp\n",
                "    tradslack\n",
                "    tx\n",
                "    txs\n",
                "pf_slack\n",
                "    ;\n",
                "Rest Endogenous ;"
            ]

            line_list_shocks = SimulationShocks(self.shock_type).create()

        if self.model_type == "gtap-v7":
            line_list_header = [
                "! This Command file\n",
                "! was written by RunGTAP (Version 3.61 built 19/Oct/2013)\n",
                "! If a version has no CMFSTART file of its own\n",
                "! RunGTAP creates one by copying the supplied file CMFSTART.DEF\n",
                "CPU = yes;  ! log show simulation times\n",
                "NDS = yes;  ! no displays\n",
                "Extrapolation accuracy file = NO ; ! No XAC file\n",
                "!servants=1; ! use 2 processors at once, if possible\n",
                "file GTAPSUM = SUMMARY.har;\n",
                "file WELVIEW = DECOMP.har;\n",
                "file GTAPVOL = VOLUME.har;\n",
                "\n",
                "xSet REG1 (RestofWorld);\n",
                "xSubset REG1 is subset of REG;\n",
                "xSet XREG = REG - REG1;\n",
                "!@ end of CMFSTART part\n",
                "aux files = GTAPv7;\n",
                "file gtapSETS = sets.har;\n",
                "file gtapDATA = basedata.har;\n",
                "Updated file gtapDATA = <cmf>.har;\n",
                "file gtapPARM = default.prm;\n",
                "Verbal Description =\n",
                "Numeraire shock;\n"
            ]

            # Create lines that define which variables are endogeneous and exogeneous
            line_list_exogendo = [
                "! basic closure\n",
                "Exogenous\n",
                "          pop\n",
                "          psaveslack pfactwld\n",
                "          profitslack incomeslack endwslack\n",
                "          cgdslack \n",
                "          tradslack\n",
                "          ams atm atf ats atd\n",
                "          aosec aoreg avasec avareg\n",
                "          aintsec aintreg aintall\n",
                "          afcom afsec afreg afecom afesec afereg\n",
                "          aoall afall afeall\n",
                "          au dppriv dpgov dpsave\n",
                "          to tinc \n",
                "          tp tm tms tx txs\n",
                "          qe\n",
                "          qesf;\n",
                "Rest endogenous;\n"
            ]

            line_list_shocks = SimulationShocks(self.shock_type).create()

        # Combine line lists
        line_list_total = line_list_header + line_list_method + line_list_exogendo \
                          + line_list_shocks

        # Create final file
        cmf_file_name_with_path = "Work_Files\\" +self.simulation_name+"\\"+ self.model_folder + "\\" + cmf_file_name
        with open(cmf_file_name_with_path, "w+") as writer:  # Create the empty file
            writer.writelines(line_list_total)  # write the line list to the file
