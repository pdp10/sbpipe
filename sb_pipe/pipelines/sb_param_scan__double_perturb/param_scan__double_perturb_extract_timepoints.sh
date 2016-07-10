#!/bin/bash
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-7 19:14:32 $


# This script was created for extracting the single timepoints of a 
# double parameter scan using copasi. 

# It requires a file "${param_scan__double_perturb_copasi_model}.csv" to be generated in ${path}.
# These files contain the progressive parted double perturbation experiment.
# This script should be executed after parscan__dp_concat_files.sh



# Import the libraries
. ${SB_PIPE_LIB}/bash/copasi__utils.sh





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



