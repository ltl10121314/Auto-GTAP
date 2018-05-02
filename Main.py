__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-9"
__altered__ = "2018-5-2"

# Import methods
# Import External Methods
import os, subprocess

# Import My Methods
from CleanWorkFiles import CleanWorkFiles
from CopyInputFiles import CopyInputFiles
from CreateSTI import CreateSTI
from SimulationCMF import SimulationCMF
from CreateMAP import CreateMAP
from ImportCSV_SL4 import ImportCSV_SL4
from ModifyDatabase import ModifyDatabase
from ExportDictionary import ExportDictionary
from CreateOutput import CreateOutput
from CreateConfig import CreateConfig
from ModifyHAR import ModifyHAR
from MoveDatabaseFiles import MoveDatabaseFiles
from SplitCommodities import SplitCommodities
from AggregateModelData import AggregateModelData

# Call Methods

# Workspace preparation common to all simulations
config = CreateConfig("config.yaml")
# Setup files for running GEMSIM
CleanWorkFiles()

#Workspace preparations idiosyncratic to particular simulations
for simulation_name in config.simulation_list:
    for part_num in range(1, config.num_parts(simulation_name) + 1):

        part_type=config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["type"]
        part_input_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["input_folder"]
        part_work_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["work_folder"]

        CopyInputFiles(simulation_name, part_input_folder, part_work_folder)

        if part_num != 1:
            prev_part_num = part_num - 1
            prev_part_work_folder = config.yaml_file["simulations"][simulation_name]["subparts"][prev_part_num][
                "work_folder"]
            prev_part_type = config.yaml_file["simulations"][simulation_name]["subparts"][prev_part_num]["type"]
            MoveDatabaseFiles(simulation_name, prev_part_type, part_type)

        if part_type == "GTPAg2":
            AggregateModelData(simulation_name)
        if part_type == "MSplitCom-Exe":
            SplitCommodities(simulation_name)
        if part_type == "modify_har":
            ModifyHAR("Work_Files\\" + simulation_name, "olddefault", "default",
                      config.yaml_file["parameter_modifications"][
                          config.sim_property(simulation_name, "parameter_modifications")])
        if part_type == "GTAP-V6":
            SimulationCMF("sim", simulation_name,
                          "default_{0}".format(config.sim_property(simulation_name, "solution_method")),
                          config.sim_property(simulation_name, "input_directory"),
                          config.sim_property(simulation_name, "shock"),
                          config.sim_property(simulation_name, "model_type"))

# Run Simulation
# Change working directory to Work_Files so all output (and logs) will go there when gemsim or sltoht is called
for simulation_name in config.simulation_list:
    os.chdir("Work_Files\\{0}\\{1}".format(simulation_name,config.sim_property(simulation_name, "input_directory")))
    # Create GSS and GST files for shocks and model gemsim
    subprocess.call("tablo -sti {0}.sti".format(config.sim_property(simulation_name, "model_file_name")))
    subprocess.call("gemsim -cmf sim_{0}.cmf".format(simulation_name))

    # Export Results of Simulation
    # Export sl4 to csv via sltoht
    CreateMAP("sim", simulation_name, config.sim_property(simulation_name, "map"))
    CreateSTI("NA", simulation_name, "sltoht")
    subprocess.call("sltoht -sti sim_{0}_sltoht.sti".format(simulation_name))
    os.chdir("..")
    os.chdir("..")

# Import simulation results into a single database
# Copy results to output directory
databaseSL4 = ImportCSV_SL4(config.model_csv_paths).create()
databaseMod = ModifyDatabase(databaseSL4).create()
ExportDictionary("Results.csv", databaseMod)

# Put results in output directory
os.chdir("..")
CreateOutput()
