#!/bin/bash

# Piero Dalle Pezze (2013)

# This script processes the parted datasets of a double perturbation 
# experiment and generates the plots. 


# The project name
project=$1
# The model name 
model=$2
# The number of files to combine
nfiles=$3
# The dataset folder of the double perturbation (e.g. "perturb_AMPK_mTORC1_data")
dp_dataset_dir=$4
# The length of the simulation (e.g 21)
sim_length=$5



# Concatenates the parted files of a double perturbation experiment (${nfiles} subfiles => 1 merged file)
${SB_PIPE}/bin/param_scan__double_perturb_concat_files.sh ${project} ${model} ${nfiles} ${dp_dataset_dir}

# Extract the single timepoints of the double perturbation (1 merged file => ${sim_length} time-point files}
${SB_PIPE}/bin/param_scan__double_perturb_extract_timepoints.sh ${project} ${model} ${sim_length} ${dp_dataset_dir}

# Generate plots for each time points 
path="${SB_PIPE}/${project}/simulations/"
folderin="dp_dataset_dir"
matlab -desktop -r "try; path=\'${path}\'; folderin=\'${folderin}\'; run(\'${SB_PIPE}/bin/param_scan__double_perturb_plot_surfaces.m\'); catch; end; quit"


