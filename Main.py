__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-9"
__altered__ = "2018-3-23"

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

# Call Methods
config = CreateConfig("config.yaml")
# Setup files for running GEMSIM
CleanWorkFiles(config.simulation_list)
for simulation_name in config.simulation_list:
    CopyInputFiles(config.sim_property(simulation_name, "input_directory"), simulation_name)
    SimulationCMF("sim", simulation_name, "default_{0}".format(config.sim_property(simulation_name, "solution_method")),
                  simulation_name).create("Gas")
    if config.sim_property(simulation_name, "modify_har"):
        ModifyHAR("Work_Files\\"+simulation_name,"olddefault", "default")

# Run Simulation
# Change working directory to Work_Files so all output (and logs) will go there when gemsim or sltoht is called
for simulation_name in config.simulation_list:
    os.chdir("Work_Files\\{0}".format(simulation_name))
    # Create GSS and GST files for shocks and model gemsim
    CreateSTI(config.sim_property(simulation_name, "model_file_name"), "NA", "gtap")
    subprocess.call("tablo -sti {0}.sti".format(config.sim_property(simulation_name, "model_file_name")))
    subprocess.call("gemsim -cmf sim_{0}.cmf".format(simulation_name))

    # Export Results of Simulation
    # Export sl4 to csv via sltoht
    CreateMAP("sim", simulation_name)
    CreateSTI("NA", simulation_name, "sltoht")
    subprocess.call("sltoht -sti sim_{0}_sltoht.sti".format(simulation_name))
    os.chdir("..")
    os.chdir("..")

# Import simulation results into a single database
# Copy results to output directory
databaseSL4 = ImportCSV_SL4(config.simulation_list).create()
databaseMod = ModifyDatabase(databaseSL4).create()
os.chdir("Work_Files")
ExportDictionary("Results.csv", databaseMod)

os.chdir("..")
# Put results in output directory
CreateOutput()
