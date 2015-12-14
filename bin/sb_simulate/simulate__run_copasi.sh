#!/bin/bash
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either model 2 of the License, or (at
# your option) any later model.
#    
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
# Object: Execute the model several times for stochastical analysis
#
# Institute for Ageing and Health
# Newcastle University
# Newcastle upon Tyne
# NE4 5PL
# UK
# Tel: +44 (0)191 248 1106
# Fax: +44 (0)191 248 1101
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2012-07-09 16:14:32 $



# Import the libraries
. ${SB_PIPE_LIB}/bash/copasi__utils.sh





# Input parameters
# read the model
model=$1
# read the models dir
models_dir=$2
# The output dir
output_dir=$3
# read the temp dir
tmp_dir=$4
# minimum 2 (required for plotCI, otherwise, ci95 and sderr are NA -> error in ylim)
simulate__model_simulations_number=$5




if [ "${simulate__model_simulations_number}" -lt "2" ]; then 
  printf "ERROR: variable \${simulate__model_simulations_number} must be >= 2";
  exit 1;
fi
  
  
  
  
model_noext="${model%.*}"
mkdir -p ${output_dir}


echo "Simulating Model: $model"
# execute $simulate__model_simulations_number simulations
for (( i=1; i <= $simulate__model_simulations_number; i++ ))
do
    # run CopasiSE. Copasi must generate a (TIME COURSE) report called ${model_noext}.csv in ${tmp_dir}
    CopasiSE --nologo ${models_dir}/${model}
    # Replace some string in the report file
    echo "Simulation No.: $i"
    `replace_str_copasi_sim_report "${tmp_dir}" "${model}"`
    mv ${tmp_dir}/${model_noext}.csv ${output_dir}/${model_noext}__sim_$i.csv
done
