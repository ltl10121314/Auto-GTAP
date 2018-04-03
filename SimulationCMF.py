__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-13"
__altered__ = "2018-4-3"


class SimulationCMF(object):
    """Creates an CMF file for controlling gemsim when it runs the policy simulation (as opposed to the shock
    calculation)"""

    __slots__ = ["project", "simulation_name", "solution_method", "model_folder", "shock_type"]

    def __init__(self, project: str, simulation_name: str, solution_method: str, model_folder: str,
                 shock_type: str) -> None:
        self.project = project
        self.simulation_name = simulation_name
        self.solution_method = solution_method
        self.model_folder = model_folder
        self.shock_type = shock_type

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
        # NB: Gas production data
        # https://www.eia.gov/dnav/ng/hist/n9010us2A.htm
        # 2005: 23,456,822
        # 2016: 32,635,511

        gas_price_2005 = 8.86  # https://www.eia.gov/dnav/ng/hist/rngwhhdA.htm
        cpi_2005 = 195.3  # CPI-All Urban Consumers (Current Series)
        gas_price_2016 = 2.52
        cpi_2016 = 240.0
        gas_price_shock = 100 * (gas_price_2016 / cpi_2016) / (gas_price_2005 / cpi_2005) - 100
        line_list_gas_price_shocks = [
            ' Swap aoall("Gas", "USA") = pm("Gas", "USA");\n',
            ' Shock pm("Gas","USA") = uniform {0};\n'.format(gas_price_shock)
        ]

        us_gdp_2005 = 14.706  # https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.KD?contextual=default&locations=US-1W
        us_gdp_2016 = 17.27
        world_gdp_2005 = 76.235
        world_gdp_2016 = 112.152
        non_us_gdp_2005 = world_gdp_2005 - us_gdp_2005
        non_us_gdp_2016 = world_gdp_2016 - us_gdp_2016
        us_gdp_shock = 100 * us_gdp_2016 / us_gdp_2005 - 100
        non_us_gdp_shock = 100 * non_us_gdp_2016 / non_us_gdp_2005 - 100
        line_list_gdp_shocks = [
            ' Swap aoreg = qgdp;\n',
            ' Shock qgdp("USA") = uniform {0};\n'.format(us_gdp_shock),
            ' XSET USset ## (USA);\n',
            ' XSUBSET USset is subset of REG;\n',
            ' XSET non_US = REG - USset;\n',
            ' Shock qgdp(non_US) = uniform {0};\n'.format(non_us_gdp_shock)
        ]

        us_gas_production_2005 = 18050598  # Source: EIA Series N9070US2
        us_gas_production_2016 = 26662774
        us_gas_production_shock = 100 * (us_gas_production_2016 / us_gas_production_2005) - 100

        us_gas_imports_2005 = 4341034  # Source: EIA Series  N9100US2
        us_gas_imports__2016 = 3006439
        us_gas_import_shock = 100 * (us_gas_imports__2016 / us_gas_imports_2005) - 100

        us_gas_exports_2005 = 18050598  # Source: EIA Series  N9130US2
        us_gas_exports_2016 = 26662774
        us_gas_export_shock = 100 * (us_gas_exports_2016 / us_gas_exports_2005) - 100

        line_list_gas_quantity_shocks_actual = [
            ' Swap qo("Gas","USA") = aoall("Gas", "USA");\n',
            ' Swap qiw("Gas","USA") = tm("Gas", "USA");\n',
            ' Swap qxw("Gas","USA") = tx("Gas", "USA");\n',
            ' Shock qo("Gas","USA") = uniform {0};\n'.format(us_gas_production_shock),
            ' Shock qiw("Gas","USA") = uniform {0};\n'.format(us_gas_import_shock),
            ' Shock qxw("Gas","USA") = uniform {0};\n'.format(us_gas_export_shock)
        ]

        if self.shock_type == "experiment":
            line_list_shocks = line_list_gas_price_shocks + line_list_gdp_shocks

        if self.shock_type == "actual":
            line_list_shocks = line_list_gas_quantity_shocks_actual

        # Combine line lists
        line_list_total = line_list_header + line_list_method + line_list_exogendo \
                          + line_list_shocks

        # Create final file
        with open("Work_Files\\" + self.model_folder + "\\" + cmf_file_name, "w+") as writer:  # Create the empty file
            writer.writelines(line_list_total)  # write the line list to the file
