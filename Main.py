import os
import subprocess
# noinspection PyPep8Naming
import AutoGTAP as ag

# Call Methods
# Load config files that will control program
config = ag.CreateConfig("config.yaml")
# Delete working files directory
ag.CleanWorkFiles()
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
        ag.CopyInputFiles(config, simulation_name, part_num).copy()

        # Copy Work files from the previous part to the work directory for this part, unless this is the first part
        if part_num != 1:
            ag.MoveFilesBetweenSteps(config, simulation_name, part_num)

        # Run the actual work for this part, depending on which type of part it is
        if part_type == "GTPAg2":
            ag.AggregateModelData(config, simulation_name, part_num)

        elif part_type == "MSplitCom-Exe":
            ag.SplitCommodities(simulation_name)

        elif part_type == "modify_har":
            ag.ModifyHAR(config, simulation_name, part_num)

        elif part_type == "GTPVEW-V6" or part_type == "Shocks-V6":
            ag.Gtpvew(config, simulation_name, part_num)

        elif part_type == "GTAP-Adjust":
            ag.GTAPAdjustCMF(config, simulation_name, part_num)

        elif part_type == "GTAP-V6" or part_type == "GTAP-E":
            ag.GtapModel(config, simulation_name, part_num)

        else:
            raise ValueError('Unexpected part type: %s' % part_type)

# Import simulation results into a single database
old_work_directory = os.getcwd()
os.chdir("WorkFiles")
# load the various CSV files created by the experiment simulation into a database
databaseSL4 = ag.ImportCsvSl4(config.csv_paths()).create()
# Modify the database to make it more readable
databaseMod = ag.ModifyDatabase(databaseSL4).create()
# Export the database to a results csv file
ag.ExportDictionary("Results.csv", databaseMod)
# Copy results.csv to the OutputFiles directory, and rename it with a timestamp
os.chdir(old_work_directory)
ag.CreateOutput()
