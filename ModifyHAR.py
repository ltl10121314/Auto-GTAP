__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-28"
__altered__ = "2018-3-28"


class ModifyHAR(object):
    """Modifies the values of a HAR file"""

    __slots__ = ["input_file", "output_file"]

    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file = input_file
        self.output_file = output_file

        tab_file_name = "ModifyHAR.tab"

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

        # Create lines for shocks
        gas_price_2005 = 8.86  # https://www.eia.gov/dnav/ng/hist/rngwhhdA.htm
        cpi_2005 = 195.3  # CPI-All Urban Consumers (Current Series)
        gas_price_2016 = 2.52
        cpi_2016 = 240.0
        gas_price_shock = 100 * (gas_price_2005 / cpi_2005) / (gas_price_2016 / cpi_2016) - 100
        line_list_shocks = [
            ' Swap aoall("Gas", "USA") = pm("Gas", "USA");\n',
            ' Shock pm("Gas","USA") = uniform {0};\n'.format(gas_price_shock)
        ]

        # Combine line lists
        line_list_total = line_list_header + line_list_method + line_list_exogendo \
                          + line_list_shocks

        # Create final file
        with open("Work_Files\\" + self.model_folder + "\\" + cmf_file_name, "w+") as writer:  # Create the empty file
            writer.writelines(line_list_total)  # write the line list to the file
