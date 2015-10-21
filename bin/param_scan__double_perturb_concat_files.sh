#!/bin/bash

# Piero Dalle Pezze (2013)

# This script was created for combining the results of a partitioned 
# double parameter scan using copasi. Particularly, the task of 
# perturbing two parameters using small intervals can require a considerable 
# amount of time. Therefore, a solution was to divide this task in sub-tasks, 
# each of them computing a specific range of the perturbation. 
# Eventually, the results from these subtasks need to be concatenated and this 
# is the aim of this script.

# It requires a set of files "model_${i}.csv" to be generated in ${path}.
# These files contain the progressive parted double perturbation experiment.


# The path (same for input/output since we are working on the same datasets)
path=$1
# The model which is double perturbed
param_scan__double_perturb_copasi_model=$2
# The number of files to combine
param_scan__double_perturb_subtasks_number=$3






fileout="${param_scan__double_perturb_copasi_model%.*}.csv"


mkdir -p ${path}



str_null=""
header=""

echo ""
echo "Concatenate files generating: ${path}/${fileout}"
echo ""


# Copy the header line in the concatenated file
if [ "${param_scan__double_perturb_subtasks_number}" -ge "1" ]  # -ge : greater than or equal to
then 
    echo "Copy the header file into ${path}/$fileout"
    head -1 "${path}/${param_scan__double_perturb_copasi_model%.*}_1.csv" > ${path}/$fileout
    header=`head -1 "${path}/${param_scan__double_perturb_copasi_model%.*}_1.csv"`
    
    # Concatenate param_scan__double_perturb_subtasks_number removing the header line.
    for (( i=1; i<=${param_scan__double_perturb_subtasks_number}; i++ ))
    do
	filein="${param_scan__double_perturb_copasi_model%.*}_${i}.csv"
	echo "Concatenate ${path}/${filein} into ${path}/${fileout}"
	# append filein to the bottom of fileout after deleting header and blank lines
	cat ${path}/${filein} | sed "1d" | awk NF >> ${path}/${fileout}
    done    
    
else 
    printf "ERROR: param_scan__double_perturb_subtasks_number must be >= 1 \n" 
fi

