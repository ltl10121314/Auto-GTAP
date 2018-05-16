__author__ = "Andre Barbe"
__project__ = "Auto-GTAP"
__created__ = "2018-3-9"

# Import methods
import os, subprocess, shutil, distutils.dir_util  # External methods
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
from GTAPAdjustCMF import GTAPAdjustCMF

# Call Methods

# Load config files that will control program
config = CreateConfig("config-gtap.yaml")
# Delete working files directory
CleanWorkFiles()

# For each simulation, perform the different subparts (data aggregation, splitting,
# experiment simulation, etc) that make up that simulation
for simulation_name in config.simulation_list:
    # Add one to final range so that python will run the last part too
    for part_num in range(1, config.num_parts(simulation_name) + 1):

        # Load configuration information for this particular part
        part_type = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["type"]
        part_input_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["input_folder"]
        part_work_folder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["work_folder"]

        # Copy input files for this part to the appropriate work directory
        CopyInputFiles(simulation_name, part_input_folder, part_work_folder).copy()

        for additional_input_folder in config.part_additional_input_folders(simulation_name, part_num):
            # need to use this copy method to overwrite files/folders (or copy files to folders taht already exist)
            distutils.dir_util.copy_tree("Input_Files\{0}".format(additional_input_folder),
                                         "Work_Files\{0}\{1}".format(simulation_name, part_work_folder))

        # Copy Work files from the previous part to the work directory for this part, unless this is the first part
        if part_num != 1:
            prev_part_num = part_num - 1
            prev_part_work_folder = config.yaml_file["simulations"][simulation_name]["subparts"][prev_part_num][
                "work_folder"]
            prev_part_type = config.yaml_file["simulations"][simulation_name]["subparts"][prev_part_num]["type"]
            MoveDatabaseFiles(simulation_name, prev_part_type, part_type, prev_part_work_folder, part_work_folder)

        # Run the actual work for this part, depending on which type of part it is
        if part_type == "GTPAg2":
            agg_scheme_file = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
                "agg_scheme_file"]
            data_subfolder = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
                "data_subfolder"]
            AggregateModelData(simulation_name, part_work_folder, agg_scheme_file, data_subfolder)

        if part_type == "MSplitCom-Exe":
            SplitCommodities(simulation_name)

        if part_type == "modify_har":
            # Modify_HAR directly modifies a HAR file
            # This module should be rarely used
            ModifyHAR("Work_Files\\" + simulation_name, "olddefault", "default",
                      config.yaml_file["parameter_modifications"][
                          config.sim_property(simulation_name, "parameter_modifications")])

        if part_type == "GTPVEW-V6" or part_type == "Shocks-V6":
            model_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["model_file_name"]
            cmf_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["cmf_file_name"]

            # Change working directory to Work_Files so all output (and logs) will go there when gemsim or sltoht is called
            os.chdir("Work_Files\\{0}\\{1}".format(simulation_name, part_work_folder))
            # Create GSS and GST files for shocks and model gemsim
            subprocess.call("tablo -sti {0}.sti".format(model_file_name))
            subprocess.call("gemsim -cmf {0}.cmf".format(cmf_file_name))
            os.chdir("..")
            os.chdir("..")
            os.chdir("..")

        if part_type == "GTAP-Adjust":
            part_shock = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["shock"]

            GTAPAdjustCMF(simulation_name, part_solution_method, part_work_folder, part_shock)

            # Change working directory to Work_Files so all output (and logs) will go there when gemsim or sltoht is called
            os.chdir("Work_Files\\{0}\\{1}".format(simulation_name, part_work_folder))
            subprocess.call("adjust.bat")
            os.chdir("..")
            os.chdir("..")
            os.chdir("..")

        if part_type == "GTAP-V6":
            # Load additional configuration information specific to GTAP simulations
            part_shock = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["shock"]
            part_solution_method = config.yaml_file["simulations"][simulation_name]["subparts"][part_num][
                "solution_method"]
            model_file_name = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["model_file_name"]
            map = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["map"]

            SimulationCMF(simulation_name, part_solution_method, part_work_folder, part_shock, part_type)
            # Change working directory to Work_Files so all output (and logs) will go there when gemsim or sltoht is called
            os.chdir("Work_Files\\{0}\\{1}".format(simulation_name, part_work_folder))
            # Create GSS and GST files for shocks and model gemsim
            subprocess.call("tablo -sti {0}.sti".format(model_file_name))
            subprocess.call("gemsim -cmf {0}.cmf".format(model_file_name))

            # Use SLtoHT export the results of the simulation from sl4 to a CSV file
            CreateMAP("sim", simulation_name, map)  # Map file determines which variables to export
            CreateSTI(model_file_name, simulation_name, "sltoht")  # STI file controls running of sltoht
            subprocess.call("sltoht -sti {0}_sltoht.sti".format(model_file_name))

            # Change directory back to Work_Files
            os.chdir("..")
            os.chdir("..")
            os.chdir("..")

# Import simulation results into a single database
os.chdir("Work_Files")
# load the various CSV files created by the experiment simulation into a database
databaseSL4 = ImportCSV_SL4(config.csv_paths()).create()
# Modify the database to make it more readable
databaseMod = ModifyDatabase(databaseSL4).create()
# Export the database to a results csv file
ExportDictionary("Results.csv", databaseMod)
# Copy results.csv to the Output_Files directory, and rename it with a timestamp
os.chdir("..")
CreateOutput()
