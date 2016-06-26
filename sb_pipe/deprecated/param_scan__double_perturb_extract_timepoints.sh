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

# This script was created for extracting the single timepoints of a 
# double parameter scan using copasi. 

# It requires a file "$model.csv" to be generated in ${path}.
# These files contain the progressive parted double perturbation experiment.
# This script should be executed after parscan__dp_concat_files.sh



# The project name
project=$1
# The model name 
model=$2
# The length of the simulation (e.g 21)
sim_length=$3
# The dataset folder of the double perturbation (e.g. "perturb_AMPK_mTORC1_data")
dp_dataset_dir=$4



# header manipulation
str_ini_pn="\[InitialParticleNumber\]"
str_ini_conc="\[InitialConcentration\]"
str_pn="\[ParticleNumber\]"
str_conc="\[Concentration\]"
str_value="\[Value\]"
str_null=""
fileout=""


path="${SB_PIPE}/${project}/simulations/${model}/${dp_dataset_dir}"

mkdir -p ${path}


# remove file extention (if any)
model=`echo $model | sed 's/\.csv$//g'`




echo ""
echo "Extraction of time points for the model: ${model}"
echo ""

# Extract a selected time point from all perturbed time courses contained in $model.csv
for (( i=0; i<=${sim_length}; i+=1 ))
do
    fileout="${model}_tp_${i}.csv"
    echo "Extract time point: ${i}"
    # extract the header line and clean it
    head -1 "${path}/$model.csv" > ${path}/$fileout
    sed -i "s/$str_pn/$str_null/g" ${path}/$fileout
    sed -i "s/$str_conc/$str_null/g" ${path}/$fileout
    sed -i "s/$str_ini_pn/$str_null/g" ${path}/$fileout
    sed -i "s/$str_ini_conc/$str_null/g" ${path}/$fileout
    sed -i "s/$str_value/$str_null/g" ${path}/$fileout
    # extract the i-th time point
    sed -n "$((${i}+2))~$((${sim_length}+1))p" "${path}/$model.csv" >> ${path}/$fileout
done



