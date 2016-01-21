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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-09-06 16:14:32 $



# Import the libraries
. ${SB_PIPE_LIB}/bash/copasi__utils.sh





# Input parameters
# read the model
model=$1
# the species to knock-down (name of the species as in copasi)
species=$2
# Number of times the model should be simulated. For deterministic 
# simulations, ${param_scan__single_perturb_simulations_number}==1 . For stochastic simulations, ${param_scan__single_perturb_simulations_number}==h. 
param_scan__single_perturb_simulations_number=$3
# Read the models dir
models_dir=$4
# Read the results dir
results_dir=$5
# Read the tmp dir
tmp_dir=$6




echo "Simulating Model: ${model}"

model_noext="${model%.*}"
output_dir="${results_dir}"


names=[]
species_index=-1
species_level=-1

# create ${output_dir} if not present
mkdir -p ${output_dir}

# execute $${param_scan__single_perturb_simulations_number} simulations
for (( i=1; i <= ${param_scan__single_perturb_simulations_number}; i++ ))
do
    echo "Simulation No.: $i"
    # run CopasiSE. Copasi must generate a (TIME COURSE) report called ${model_noext}.csv in ${tmp_dir}
    CopasiSE --nologo ${models_dir}/${model}
    # Replace some string in the report file   
    
   
    if [ ! -f "${tmp_dir}/${model_noext}.csv" ]; then 
	echo "${tmp_dir}/${model_noext}.csv does not exist! ERROR: CANNOT CONTINUE" 
	break
    fi        
    
    `replace_str_copasi_sim_report "${tmp_dir}" "${model}"`
    # THE FOLLOWING CORRECTS A BUG IN COPASI "SCAN PARAMETERS" REPORT..
    # Delete every 2nd line starting from the 1st line (all odd lines).
    # Actually, this is a bug in the report generation. It appears and not.... nice!
    # Therefore, the following command (Removing the second line) is not suitable!
    # sed '1~2 d' -i ${tmp_dir}/${model_noext}.csv
    # This following command deletes duplicate, consecutive lines from a file (emulates "uniq").
    # First line in a set of duplicate lines is kept, rest are deleted.
    sed -i '$!N; /^\(.*\)\n\1$/!P; D' ${tmp_dir}/${model_noext}.csv
    # Delete all blank lines.
    # sed -i "/^$/d" ${tmp_dir}/${model_noext}.csv
    # Delete the characters "[" and "]"
    sed -i 's/\[//g;s/\]//g' ${tmp_dir}/${model_noext}.csv    
    

    # Set the number of intervals
    intervals=$[`grep  -c '^$' ${tmp_dir}/${model_noext}.csv`]
    echo "Intervals: $intervals"
    # Set the number of timepoints
    lines=$[`wc -l ${tmp_dir}/${model_noext}.csv | awk '{print $1'}`]
    timepoints=$[($lines - 1 - $intervals) / $intervals]
    echo "Time points: $timepoints"

    # Find the index of $species in the header file, so it is possible to read the amount at 
    # the second line.
    if [[ $i==1 ]] ; then 
	echo "Retrieving column index for species $species from file ${tmp_dir}/${model_noext}.csv"
	names=(`sed -n "1 p" ${tmp_dir}/${model_noext}.csv | tr "\t" "\n"`)
	for (( j=0; j < ${#names[@]} ; j++)) 
        do 
	  echo "$j ${names[$j]} $species"
	  if [ "${names[$j]}" == "$species" ] ; then species_index=$j ; break; fi; 
	done
	if [ "${species_index}" == "-1" ] ; then echo "Column index for species ${species}: ${species_index}. ERROR: Species not found!!! You must add the species ${species} to the report form in the copasi file (check the report time-course or parameter scan). STOP" ; exit; 
	else echo "Column index for species $species: $species_index"; fi
    fi
      

    for (( j=0; j < $intervals; j++ ))
    do
       # Read the species level
       initial_configuration=(`sed -n "2 p" ${tmp_dir}/${model_noext}.csv | tr "\t" "\n"`)
       species_level=${initial_configuration[$species_index]}

       if [ "${species_level}" == "-1" ] ; then echo "ERROR: species_level not configured!!! STOP" ; exit; 
       else echo "$species level: $species_level (list index: $species_index)"; fi
       

       # copy the -th run to a new file: add 1 to $timepoints because of the header.

       #round_species_level=$(printf %.0f $species_level)
       round_species_level=$species_level
       head -$[$timepoints+1] ${tmp_dir}/${model_noext}.csv > ${output_dir}/${model_noext}__sim_${i}__level_${round_species_level}.csv

       # delete the first 2-$timepoints+2 lines of a file, leaving the header
       # 2 because: 1 header, 1 blank line as separator.
       sed -i "2,$[$timepoints+2] d" ${tmp_dir}/${model_noext}.csv
    done
    rm ${tmp_dir}/${model_noext}.csv

done

