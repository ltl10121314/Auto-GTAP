__author__ = "Andre Barbe"
__project__ = "GTAP-E Validation"
__created__ = "2018-3-9"
__altered__ = "2018-3-15"

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

# Call Methods
config = ReadYaml().create()
# Setup files for running GEMSIM
CleanWorkFiles(input_directory_list).create()
CopyInputFiles(input_directory_list).create()
SimulationCMF("sim", simulation_name, "default_{0}".format(solution_method), "GTAP-E").create(simulation_name)

# Run Simulation
# Change working directory to Work_Files so all output (and logs) will go there when gemsim or sltoht is called
os.chdir("Work_Files\\GTAP-E")
# Create GSS and GST files for shocks and model gemsim
CreateSTI(gtap_file_name, "NA", "gtap").create()
subprocess.call("tablo -sti {0}.sti".format(gtap_file_name))
subprocess.call("gemsim -cmf sim_{0}.cmf".format(simulation_name))

# Export Results of Simulation
# Export sl4 to csv via sltoht
CreateMAP("sim", simulation_name).create()
CreateSTI("NA", simulation_name, "sltoht").create()
subprocess.call("sltoht -sti sim_{0}_sltoht.sti".format(simulation_name))
# Copy results to output directory
databaseSL4 = ImportCSV_SL4("sim_", simulation_list).create()
databaseMod = ModifyDatabase(databaseSL4).create()
ExportDictionary("Results {0}.csv".format(solution_method), databaseMod).create()
os.chdir("..")
os.chdir("..")
# Put results in output directory
for simulation_name in simulation_list:
    CreateOutput(["Results {0}.csv".format(solution_method)]).create()
