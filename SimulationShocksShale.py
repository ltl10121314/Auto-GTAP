__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-4-18"
__altered__ = "2018-5-2"


class SimulationShocks(object):
    """Creates a line list of shocks for insertion into the simulation's CMF file"""

    def __init__(self, shock_type: str) -> None:
        self.shock_type = shock_type

    def create(self):
        # Create lines for shocks
        # NB: most gas data is available at https://www.eia.gov/dnav/ng/ng_sum_lsum_dcu_nus_a.htm
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

        us_gas_exports_2005 = 728601  # Source: EIA Series  N9130US2
        us_gas_exports_2016 = 2335448
        us_gas_export_shock = 100 * (us_gas_exports_2016 / us_gas_exports_2005) - 100

        line_list_gas_shocks_actual = [
            ' Swap pm("Gas", "USA") = to("Gas", "USA");\n',
            ' Swap qo("Gas","USA") = aoall("Gas", "USA");\n',
            ' Swap qiw("Gas","USA") = tm("Gas", "USA");\n',
            ' Swap qxw("Gas","USA") = tx("Gas", "USA");\n',
            ' Shock pm("Gas","USA") = uniform {0};\n'.format(gas_price_shock),
            ' Shock qo("Gas","USA") = uniform {0};\n'.format(us_gas_production_shock),
            ' Shock qiw("Gas","USA") = uniform {0};\n'.format(us_gas_import_shock),
            ' Shock qxw("Gas","USA") = uniform {0};\n'.format(us_gas_export_shock)
        ]

        # NB: Oil data available at https://www.eia.gov/dnav/pet/pet_sum_crdsnd_k_a.htm

        oil_price_2005 = 56.64
        oil_price_2016 = 43.29
        oil_price_shock = 100 * (oil_price_2016 / cpi_2016) / (oil_price_2005 / cpi_2005) - 100

        us_oil_production_2005 = 1892095
        us_oil_production_2016 = 3241591

        us_oil_production_shock = 100 * (us_oil_production_2016 / us_oil_production_2005) - 100

        us_oil_imports_2005 = 3695971
        us_oil_imports__2016 = 2873208
        us_oil_import_shock = 100 * (us_oil_imports__2016 / us_oil_imports_2005) - 100

        us_oil_exports_2005 = 11619
        us_oil_exports_2016 = 216274
        us_oil_export_shock = 100 * (us_oil_exports_2016 / us_oil_exports_2005) - 100

        line_list_oil_shocks_actual = [
            ' Swap pm("Oil", "USA") = to("Oil", "USA");\n',
            ' Swap qo("Oil","USA") = aoall("Oil", "USA");\n',
            ' Swap qiw("Oil","USA") = tm("Oil", "USA");\n',
            ' Swap qxw("Oil","USA") = tx("Oil", "USA");\n',
            ' Shock pm("Oil","USA") = uniform {0};\n'.format(oil_price_shock),
            ' Shock qo("Oil","USA") = uniform {0};\n'.format(us_oil_production_shock),
            ' Shock qiw("Oil","USA") = uniform {0};\n'.format(us_oil_import_shock),
            ' Shock qxw("Oil","USA") = uniform {0};\n'.format(us_oil_export_shock)
        ]

        if self.shock_type == "experiment":
            line_list_shocks = line_list_gas_price_shocks + line_list_gdp_shocks

        if self.shock_type == "actual":
            line_list_shocks = line_list_gdp_shocks \
                               + line_list_gas_shocks_actual \
                               + line_list_oil_shocks_actual

        if self.shock_type == "pop5":
            line_list_shocks = ['Shock pop(REG) = uniform 5;\n']

        if self.shock_type == "pfactorworld":
            line_list_shocks = ['Shock pfactwld = uniform 10;\n']

        return line_list_shocks
