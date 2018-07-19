import AutoGTAP as Ag

# Call Methods
# Load config files that will control program
config = Ag.CreateConfig("config.yaml")
# Delete working files directory
Ag.CleanWorkFiles()
# For each simulation, perform the different subparts (data aggregation, splitting,
# experiment simulation, etc) that make up that simulation
for simulation_name in config.simulation_list:
    # Add one to final range so that python will run the last part too
    for part_num in range(1, config.num_parts(simulation_name) + 1):

        part_type = config.yaml_file["simulations"][simulation_name]["subparts"][part_num]["type"]

        # Copy input files for this part to the appropriate work directory
        Ag.CopyInputFiles(config, simulation_name, part_num).copy()

        # Copy Work files from the previous part to the work directory for this part, unless this is the first part
        if part_num != 1:
            Ag.MoveFilesBetweenSteps(config, simulation_name, part_num)

        # Run the actual work for this part, depending on which type of part it is
        if part_type == "GTPAg2":
            Ag.AggregateModelData(config, simulation_name, part_num)

        elif part_type == "MSplitCom-Exe":
            Ag.SplitCommodities(simulation_name)

        elif part_type == "modify_har":
            Ag.ModifyHAR(config, simulation_name, part_num)

        elif part_type == "GTPVEW-V6" or part_type == "Shocks-V6":
            Ag.Gtpvew(config, simulation_name, part_num)

        elif part_type == "GTAP-Adjust":
            Ag.GTAPAdjustCMF(config, simulation_name, part_num)

        elif part_type == "GTAP-V6" or part_type == "GTAP-E":
            Ag.GtapModel(config, simulation_name, part_num)

        else:
            raise ValueError('Unexpected part type: %s' % part_type)

Ag.ExportResults(config)
