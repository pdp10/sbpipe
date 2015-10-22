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
# $Date: 2013-05-30 16:14:32 $

# This scripts provides the user with a complete pipeline of scripts for computing 
# model sensitivity analysis using Copasi



# The file containing the model configuration, usually in working_folder (e.g. model.conf)
model_configuration=$1


printf "\nReading file ${model_configuration} : \n"
# import the model configuration data (project, model-name, association-pattern)
old_IFS=$IFS
IFS=$'\n'
lines=($(cat ${model_configuration}))  # array
IFS=$old_IFS
printf "\n\n"


# NOTE: The idea is that 
# (1) the parameters of model m are estimated 
# (2) model m can be perturbed on n species (in copasi, it is better 1 species per model, since it must be configured in the .cps file)


# The project name (e.g. "p3__mtor_foxo_ros")
project=""
# read the main model name (e.g. mtor_mito_ros_model_v27_pw3.m)
model=""
# Sensitivity copasi model file (e.g mtor_mito_ros_model_v27_copasi_sens.cps ...)
sensitivities__copasi_model=""
# The folder containing the sensitivity analysis results
sensitivities_dir=""
# The folder containing the models (e.g. Models)
models_folder=""
# The folder containing the models simulations (e.g. simulations)
simulations_folder=""



# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"  
  case "${array[0]}" in
    ("project") 			echo "$line"; project="${array[1]}" ;; 
    ("model") 				echo "$line"; model="${array[1]}" ;; 
    ("sensitivities__copasi_model") 	echo "$line"; sensitivities__copasi_model="${array[1]}" ;; 
    ("sensitivities_dir") 		echo "$line"; sensitivities_dir="${array[1]}" ;; 
    ("models_folder") 			echo "$line"; models_folder="${array[1]}" ;; 
    ("simulations_folder") 		echo "$line"; simulations_folder="${array[1]}" ;; 
  esac  
done
IFS=$old_IFS





models_dir="${SB_PIPE}/${project}/${models_folder}/"
sensitivities_path="${SB_PIPE}/${project}/${simulations_folder}/${model%.*}/${sensitivities_dir}/"



printf "\n\n\n<START PIPELINE>:\n\n\n"

    

printf "\n\n\n"
printf "##############################################################################\n"      
printf "##############################################################################\n"
printf "### Processing model ${sensitivities__copasi_model}\n"
printf "##############################################################################\n"
printf "##############################################################################\n"
printf "\n\n"



printf "\n\n\n"
printf "######################################\n"
printf "Cleaning folder ${sensitivities_path}:\n"
printf "######################################\n"
printf "\n"
#rm -rf ${sensitivities_dir}/*.png
mkdir -p ${sensitivities_path}



#printf "\n\n\n"
#printf "########################\n"
#printf "Executing sensitivities:\n"
#printf "########################\n"
#printf "\n"
#bash ${SB_PIPE}/bin/sensitivities__run_copasi.sh ${sp_model} ${models_dir} ${results_dir} ${tmp_dir} 



printf "\n\n\n"
printf "##########################################\n"
printf "Generating plots for sensitivity analysis:\n"
printf "##########################################\n"
printf "\n"
Rscript ${SB_PIPE}/bin/sensitivities__copasi_plot.R ${sensitivities_path}




printf "\n\n\n<END PIPELINE>\n\n\n"


