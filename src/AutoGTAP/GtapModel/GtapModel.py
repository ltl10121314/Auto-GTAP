__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-7-19"

import os
import subprocess
from AutoGTAP.SimulationCMF.SimulationCMF import SimulationCMF
from AutoGTAP.CreateMAP.CreateMAP import CreateMAP
from AutoGTAP.CreateSTI.CreateSTI import CreateSTI


class GtapModel(object):
    """Runs the GTAP model itself"""

    __slots__ = ["config", "simulation_name", "part_num"]

    def __init__(self, config, simulation_name: str, part_num: int) -> None:

        # Load additional configuration information specific to GTAP simulations
        part_shock = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["shock"]
        part_solution_method = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
            "solution_method"]
        model_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["model_file_name"]
        map_variables = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["map"]

        part_work_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["work_folder"]

        work_directory = "WorkFiles/{0}/{1}".format(simulation_name, part_work_folder)
        part_type = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["type"]

        SimulationCMF(work_directory, simulation_name, part_solution_method, part_work_folder, part_shock,
                      part_type)

        part_sim_environment = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
            "sim_environment"]
        old_work_directory = os.getcwd()
        os.chdir(work_directory)
        if part_sim_environment == "gemsim":
            # Create GSS and GST files for shocks and model gemsim
            subprocess.call("tablo -sti {0}.sti".format(model_file_name))
            subprocess.call("gemsim -cmf {0}.cmf".format(model_file_name))
        if part_sim_environment == "fortran":
            subprocess.call("{0} -cmf {0}.cmf".format(model_file_name))
        os.chdir(old_work_directory)

        # Use SLtoHT export the results of the simulation from sl4 to a CSV file
        CreateMAP(work_directory, "sim", simulation_name,
                  map_variables)  # Map file determines which variables to export
        CreateSTI(work_directory, model_file_name, simulation_name,
                  "sltoht")  # STI file controls running of sltoht
        old_work_directory = os.getcwd()
        os.chdir(work_directory)
        subprocess.call("sltoht -sti {0}_sltoht.sti".format(model_file_name))
        os.chdir(old_work_directory)
