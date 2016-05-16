#!/bin/bash
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $

# This script was created for combining the results of a partitioned 
# double parameter scan using copasi. Particularly, the task of 
# perturbing two parameters using small intervals can require a considerable 
# amount of time. Therefore, a solution was to divide this task in sub-tasks, 
# each of them computing a specific range of the perturbation. 
# Eventually, the results from these subtasks need to be concatenated and this 
# is the aim of this script.

# It requires a set of files "model_${i}.csv" to be generated in ${path}.
# These files contain the progressive parted double perturbation experiment.


# The project name
project=$1
# The model name 
model=$2
# The number of files to combine
nfiles=$3
# The dataset folder of the double perturbation (e.g. "perturb_AMPK_mTORC1_data")
dp_dataset_dir=$4



fileout="${model}.csv"
path="${SB_PIPE}/${project}/simulations/${model}/${dp_dataset_dir}"

mkdir -p ${path}



str_null=""
header=""

echo ""
echo "Concatenate files generating: ${path}/${fileout}"
echo ""


# Copy the header line in the concatenated file
if [ ${nfiles} -ge 1 ]  # -ge : greater than or equal to
then 
    echo "Copy the header file into ${path}/$fileout"
    head -1 "${path}/${model}1.csv" > ${path}/$fileout
    header=`head -1 "${path}/${model}1.csv"`
    
    # Concatenate nfiles removing the header line.
    for (( i=1; i<=${nfiles}; i+=1 ))
    do
	filein="${model}_${i}.csv"
	echo "Concatenate ${path}/${filein} into ${path}/${fileout}"
	# append filein to the bottom of fileout after deleting header and blank lines
	cat ${path}/${filein} | sed "1d" | awk NF >> ${path}/${fileout}
    done    
    
else 
    printf "ERROR: ${nfiles} must be >= 1 \n" 
fi

