__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-7-19"

import os
import subprocess


class Gtpvew(object):
    """Runs the gtpvew GEMPACK or FORTRAN program"""

    __slots__ = ["config", "simulation_name", "part_num"]

    def __init__(self, config, simulation_name: str, part_num: int) -> None:
        part_work_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["work_folder"]
        model_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["model_file_name"]
        cmf_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["cmf_file_name"]
        work_directory = "WorkFiles\\{0}\\{1}".format(simulation_name, part_work_folder)

        part_sim_environment = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
            "sim_environment"]

        old_work_directory = os.getcwd()
        os.chdir(work_directory)
        if part_sim_environment == "gemsim":
            # Create GSS and GST files for shocks and model gemsim
            subprocess.call("tablo -sti {0}.sti".format(model_file_name))
            subprocess.call("gemsim -cmf {0}.cmf".format(cmf_file_name))
        if part_sim_environment == "fortran":
            subprocess.call("{0} -cmf {1}.cmf".format(model_file_name, cmf_file_name))
        os.chdir(old_work_directory)
