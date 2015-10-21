#!/bin/bash

# Piero Dalle Pezze (2013)

# This script was created for extracting the single timepoints of a 
# double parameter scan using copasi. 

# It requires a file "${param_scan__double_perturb_copasi_model}.csv" to be generated in ${path}.
# These files contain the progressive parted double perturbation experiment.
# This script should be executed after parscan__dp_concat_files.sh



# Import the libraries
. ${PROJ_LIB}/bash/copasi__utils.sh





# Input parameters
# The path (same for input/output since we are working on the same datasets)
path=$1
# The model which is double perturbed
param_scan__double_perturb_copasi_model=$2
# The length of the simulation (e.g 21)
param_scan__double_perturb_simulation_length=$3




mkdir -p ${path}


echo ""
echo "Extraction of time points for the model: ${param_scan__double_perturb_copasi_model}"
echo ""

# The following two lines are very time-consuming. 
# clean the file header
`replace_str_copasi_sim_report "${path}" "${param_scan__double_perturb_copasi_model%.*}.csv"`
# remove blank lines, if present (this is required if one single instance of copasi is executed)
sed -i '/^$/d' ${path}/${param_scan__double_perturb_copasi_model%.*}.csv



# Extract a selected time point from all perturbed time courses contained in ${param_scan__double_perturb_copasi_model%.*}.csv
for (( i=0; i<=${param_scan__double_perturb_simulation_length}; i++ ))
do
    fileout="${param_scan__double_perturb_copasi_model%.*}__tp_${i}.csv"
    echo "Extract time point: ${i}"
    # extract the header line and clean it
    head -1 "${path}/${param_scan__double_perturb_copasi_model%.*}.csv" > ${path}/$fileout
    #`replace_str_copasi_sim_report "${path}" "${fileout}"`  
    # extract the i-th time point
    sed -n "$((${i}+2))~$((${param_scan__double_perturb_simulation_length}+1))p" "${path}/${param_scan__double_perturb_copasi_model%.*}.csv" >> ${path}/$fileout
done



