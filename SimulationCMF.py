__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-13"

from Shocks import Shocks


class SimulationCMF(object):
    """Creates an CMF file for controlling gemsim when it runs the policy simulation (as opposed to the shock
    calculation)"""

    __slots__ = ["simulation_name", "solution_method", "model_folder", "shock_type", "model_type"]

    def __init__(self, simulation_name: str, solution_method: str, model_folder: str, shock_type: str,
                 model_type: str) -> None:
        self.solution_method = solution_method
        self.model_folder = model_folder
        self.shock_type = shock_type
        self.model_type = model_type
        self.simulation_name = simulation_name

        if self.model_type == "GTAP-V6":
            cmf_file_name = "gtap.cmf"

        # Create list of lines to be added to CMF file

        # Create lines for solution method
        if self.solution_method == "j":
            line_list_method = [
                "Method = Johansen;",
                "Steps = 1;",
                "automatic accuracy = no;",
                "subintervals = 1;",
                ""]
        elif self.solution_method == "g":
            line_list_method = [
                "Method = Gragg; Steps = 2 4 6; subintervals = 10;",
                "automatic accuracy = yes ; accuracy figures = 4; accuracy percent = 99;",
                "minimum subinterval length = 1.0E-0003;",
                "minimum subinterval fails = stop;",
                "accuracy criterion = Solution;",
                ""]
        else:
            raise ValueError('Unknown solution method in CMF')

        # Create lines for header that gives file locations
        if self.model_type == "gtap-e":
            line_list_header = [
                "CPU = yes; ! log show simulation times",
                "NDS = no ; ! no displays",
                "Extrapolation accuracy file = NO ; ! No XAC file",
                "log file=yes;",
                "aux files = GTAP;",
                "file gtapSETS = sets.har;",
                "file gtapDATA = basedata.har;",
                "Updated file gtapDATA = gtap.har;",
                "",
                "file gtapPARM = default.prm;",
                "",
                "Verbal Description = {0};".format(shock_type),
                ""]

            # Create lines that define which variables are endogeneous and exogeneous
            line_list_exogendo = [
                "exogenous",
                "    afall",
                "    afcom",
                "    afreg",
                "    afsec    ",
                "    ams",
                "    aoall",
                "    aoreg",
                "    aosec",
                "  ! atall               omitted",
                "    atd",
                "    atf",
                "    atm",
                "    ats",
                "    au",
                "    cgdslack",
                "    del_ctgshr",
                "    dpgov",
                "    dppriv",
                "    dpsave",
                "    endwslack",
                "    incomeslack",
                "    pemp",
                "    pfactwld",
                "    pop",
                "    profitslack",
                "    psaveslack",
                "    qo(ENDW_COMM,REG)",
                "    RCTAXB",
                "  ! tf                  omitted",
                "    tfd",
                "    tfm",
                "    tgd",
                "    tgm",
                "    tm",
                "    tms",
                "    to",
                "    tpd",
                "    tpm",
                "    tp",
                "    tradslack",
                "    tx",
                "    txs",
                "pf_slack",
                "    ;",
                "Rest Endogenous ;"
            ]

            line_list_shocks = Shocks(self.shock_type).create()

        if self.model_type == "GTAP-V6":
            line_list_header = [
                "CPU = yes; ! log show simulation times",
                "NDS = no ; ! no displays",
                "Extrapolation accuracy file = NO ; ! No XAC file",
                "log file=yes;",
                "aux files = GTAP;",
                "file gtapSETS = sets.har;",
                "file gtapDATA = basedata.har;",
                "Updated file gtapDATA = gtap.har;",
                "",
                "file gtapPARM = default.prm;",
                "",
                "Verbal Description = none;",
                ""]

            # Create lines that define which variables are endogeneous and exogeneous
            line_list_exogendo = [
                "exogenous",
                "          pop",
                "          psaveslack pfactwld",
                "          profitslack incomeslack endwslack",
                "          cgdslack tradslack",
                "          ams atm atf ats atd",
                "          aosec aoreg avasec avareg",
                "          afcom afsec afreg afecom afesec afereg",
                "          aoall afall afeall",
                "          au dppriv dpgov dpsave",
                "          to tp tm tms tx txs",
                "          qo(ENDW_COMM,REG) ;",
                "Rest Endogenous ;"
            ]

            line_list_shocks = Shocks(self.shock_type).create()

        if self.model_type == "gtap-v7":
            line_list_header = [
                "! This Command file",
                "! was written by RunGTAP (Version 3.61 built 19/Oct/2013)",
                "! If a version has no CMFSTART file of its own",
                "! RunGTAP creates one by copying the supplied file CMFSTART.DEF",
                "CPU = yes;  ! log show simulation times",
                "NDS = yes;  ! no displays",
                "Extrapolation accuracy file = NO ; ! No XAC file",
                "!servants=1; ! use 2 processors at once, if possible",
                "file GTAPSUM = SUMMARY.har;",
                "file WELVIEW = DECOMP.har;",
                "file GTAPVOL = VOLUME.har;",
                "",
                "xSet REG1 (RestofWorld);",
                "xSubset REG1 is subset of REG;",
                "xSet XREG = REG - REG1;",
                "!@ end of CMFSTART part",
                "log file=yes;",
                "aux files = GTAPv7;",
                "file gtapSETS = sets.har;",
                "file gtapDATA = basedata.har;",
                "Updated file gtapDATA = <cmf>.har;",
                "file gtapPARM = default.prm;",
                "Verbal Description =",
                "Numeraire shock;"
            ]

            # Create lines that define which variables are endogeneous and exogeneous
            line_list_exogendo = [
                "! basic closure",
                "Exogenous",
                "          pop",
                "          psaveslack pfactwld",
                "          profitslack incomeslack endwslack",
                "          cgdslack ",
                "          tradslack",
                "          ams atm atf ats atd",
                "          aosec aoreg avasec avareg",
                "          aintsec aintreg aintall",
                "          afcom afsec afreg afecom afesec afereg",
                "          aoall afall afeall",
                "          au dppriv dpgov dpsave",
                "          to tinc ",
                "          tp tm tms tx txs",
                "          qe",
                "          qesf;",
                "Rest endogenous;"
            ]

            line_list_shocks = Shocks(self.shock_type).create()

        # Combine line lists
        line_list_total = line_list_header + line_list_method + line_list_exogendo \
                          + line_list_shocks

        # Create final file
        cmf_file_name_with_path = "Work_Files\\" + self.simulation_name + "\\" + self.model_folder + "\\" + cmf_file_name
        with open(cmf_file_name_with_path, "w+") as writer:  # Create the empty file
            writer.writelines(line + '\n' for line in line_list_total)  # write the line list to the file
