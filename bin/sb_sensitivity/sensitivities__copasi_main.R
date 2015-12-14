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
# a single parameter scan using copasi.



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


# read the project name
project=""
# read the main model name (e.g. mtor_mito_ros_model_v27_pw3.m
model=""
# Copasi models list (1 model per species to perturb) (e.g mtor_mito_ros_model_v27_copasi_scan_mTORC1.cps ...)
param_scan__single_perturb_copasi_models_list=()
# list of species to knock-down (name of the species as in copasi) (e.g. mTORC1)
param_scan__single_perturb_species_list=()   # a list separated by blanks
# if Y then, plot only kd (blue), otherwise plot kd and overexpression
param_scan__single_perturb_knock_down_only=""
# the work team: kathrin or glyn
team=""
# The folder containing the models
models_folder=""
# The folder containing the models simulations
simulations_folder=""
# The folder containing the temporary computations
tmp_folder=""
# The legend name for the single perturbation
param_scan__single_perturb_legend=""
# Single perturbation minimum inhibition level
param_scan__single_perturb_min_inhibition_level=0
# Single perturbation maximum overexpression level
param_scan__single_perturb_max_overexpression_level=250
# The prefix for the results filename (e.g. "report_single_perturb_")
param_scan__single_perturb_prefix_results_filename=""
# The number of single pertubation simulations (e.g. 1 for deterministic simulations, 500 for stochastic simulations)
param_scan__single_perturb_simulations_number=1



# read the project and the model name
old_IFS=$IFS
IFS=$','
for line in "${lines[@]}"; do
  echo "$line"
  read -a array <<< "${line}"
  if [ "${array[0]}" == "project" ]; then 
    # The project name (e.g. "p3__mtor_foxo_ros")
    project="${array[1]}"; 
  elif [ "${array[0]}" == "model" ]; then 
    # The list of models to perturb (1 for each species)
    model="${array[1]}"        
  elif [ "${array[0]}" == "param_scan__single_perturb_copasi_models_list" ]; then 
    # The list of species to perturb (1 for each model)
    param_scan__single_perturb_copasi_models_list=("${array[1]}")    
  elif [ "${array[0]}" == "param_scan__single_perturb_species_list" ]; then 
    # The work folder (e.g. working_folder)
    param_scan__single_perturb_species_list=("${array[1]}")
  elif [ "${array[0]}" == "team" ]; then 
    # The team partner (e.g. glyn kathrin)
    team="${array[1]}"     
  elif [ "${array[0]}" == "param_scan__single_perturb_prefix_results_filename" ]; then 
    # The prefix for the results filename of a single perturbation
    param_scan__single_perturb_prefix_results_filename="${array[1]}"        
  elif [ "${array[0]}" == "param_scan__single_perturb_legend" ]; then 
    # The legend name (e.g. single_perturb_legend)
    param_scan__single_perturb_legend="${array[1]}"     
  elif [ "${array[0]}" == "param_scan__single_perturb_min_inhibition_level" ]; then 
    # The minimum level of inhibition in a single perturbation (e.g. 0)
    param_scan__single_perturb_min_inhibition_level=${array[1]}        
  elif [ "${array[0]}" == "param_scan__single_perturb_max_overexpression_level" ]; then 
    # The maximum level of overexpression in a single perturbation (e.g. 250)
    param_scan__single_perturb_max_overexpression_level=${array[1]}      
  elif [ "${array[0]}" == "param_scan__single_perturb_simulations_number" ]; then 
    # The number of copasi simulations for each single perturbation (e.g. 1)
    param_scan__single_perturb_simulations_number=${array[1]}          
  elif [ "${array[0]}" == "dataset_parameter_scan_dir" ]; then 
    #  (e.g. "dataset_parameter_scan")
    dataset_parameter_scan_dir="${array[1]}"        
  elif [ "${array[0]}" == "tc_parameter_scan_dir" ]; then 
    #  (e.g. "tc_parameter_scan")
    tc_parameter_scan_dir="${array[1]}"        
  elif [ "${array[0]}" == "param_scan__single_perturb_knock_down_only" ]; then 
    # A boolean (e.g. true)
    param_scan__single_perturb_knock_down_only="${array[1]}"            
  elif [ "${array[0]}" == "models_folder" ]; then 
    # The Models folder (e.g. Models)
    models_folder="${array[1]}"        
  elif [ "${array[0]}" == "simulations_folder" ]; then 
    # The Simulations folder (e.g. simulations)
    simulations_folder="${array[1]}"      
  elif [ "${array[0]}" == "tmp_folder" ]; then 
    # The Temporary folder (e.g. tmp)
    tmp_folder="${array[1]}"      
  fi
done
IFS=$old_IFS





if [ "${#param_scan__single_perturb_copasi_models_list[@]}" -ne "${#param_scan__single_perturb_species_list[@]}" ]
then 
  printf "\n ERROR: One model MUST BE defined for each species to perturb! (${#param_scan__single_perturb_copasi_models_list[@]} != ${#param_scan__single_perturb_species_list[@]} ) \n\n"
  exit 1
fi


if [ "${param_scan__single_perturb_min_inhibition_level}" -lt "0" ]
then 
  printf "\n ERROR: param_scan__single_perturb_min_inhibition_level MUST BE non negative \n\n"
  exit 2
fi

if [ "${param_scan__single_perturb_max_overexpression_level}" -le "100" ]
then 
  printf "\n ERROR: param_scan__single_perturb_max_overexpression_level MUST BE greater than 100 \n\n"
  exit 3;
fi



# remove the path in case this was specified.
#model_configuration=$(basename ${model_configuration})
#model_configuration_with_path="${SB_PIPE}/${project}/${work_folder}/${model_configuration}"





models_dir="${SB_PIPE}/${project}/${models_folder}/"
results_dir="${SB_PIPE}/${project}/${simulations_folder}/${model%.*}/"
tmp_dir="${SB_PIPE}/${project}/${tmp_folder}/"




printf "\n\n\n<START PIPELINE>:\n\n\n"


for ((i=0; $i < ${#param_scan__single_perturb_species_list[@]}; i++))
do
      
      sp_species="${param_scan__single_perturb_species_list[${i}]}"
      sp_model="${param_scan__single_perturb_copasi_models_list[${i}]}"
      printf "\n\n\n"
      printf "##############################################################################\n"      
      printf "##############################################################################\n"
      printf "### Processing model ${sp_model} and species ${sp_species}\n"
      printf "##############################################################################\n"
      printf "##############################################################################\n"
      printf "\n\n"
      

      
      printf "\n\n\n"
      printf "###############################\n"
      printf "Cleaning folder ${results_dir}:\n"
      printf "###############################\n"
      printf "\n"
      rm -rf ${results_dir}/${dataset_parameter_scan_dir}/*${sp_species}*
      rm -rf ${results_dir}/${tc_parameter_scan_dir}/*${sp_species}*
      rm -rf ${results_dir}/${tc_parameter_scan_dir}/${param_scan__single_perturb_legend}*
      rm -rf ${results_dir}/${param_scan__single_perturb_prefix_results_filename}*${sp_species}*
      mkdir -p ${results_dir}/${dataset_parameter_scan_dir} ${results_dir}/${tc_parameter_scan_dir}



      printf "\n\n\n"
      printf "######################\n"
      printf "Executing simulations:\n"
      printf "######################\n"
      printf "\n"
      bash ${SB_PIPE}/bin/sb_sensitivity/param_scan__single_perturb_run_copasi.sh ${sp_model} ${sp_species} ${param_scan__single_perturb_simulations_number} ${models_dir} ${results_dir} ${tmp_dir} 



      printf "\n\n\n"
      printf "####################################\n"
      printf "Generating plots for parameter scan:\n"
      printf "####################################\n"
      printf "\n"
      Rscript ${SB_PIPE}/bin/sb_sensitivity/param_scan__single_perturb_plot.R ${sp_model%.*} ${sp_species} ${param_scan__single_perturb_knock_down_only} ${results_dir} ${dataset_parameter_scan_dir} ${tc_parameter_scan_dir} ${team} ${param_scan__single_perturb_simulations_number}
      # Prepare the legend
      if [ "${param_scan__single_perturb_knock_down_only}" == "true" ] ; then
	  Rscript ${SB_PIPE}/bin/sb_sensitivity/param_scan__single_perturb_make_legend.R ${results_dir}/${tc_parameter_scan_dir}/ ${param_scan__single_perturb_legend} ${param_scan__single_perturb_min_inhibition_level} 100 ${param_scan__single_perturb_knock_down_only}
      else
	  Rscript ${SB_PIPE}/bin/sb_sensitivity/param_scan__single_perturb_make_legend.R ${results_dir}/${tc_parameter_scan_dir}/ ${param_scan__single_perturb_legend} ${param_scan__single_perturb_min_inhibition_level} ${param_scan__single_perturb_max_overexpression_level} ${param_scan__single_perturb_knock_down_only}
      fi 



      printf "\n\n\n"
      printf "###################\n"
      printf "Generating reports:\n"
      printf "###################\n"
      printf "\n"
      bash ${SB_PIPE}/bin/sb_sensitivity/param_scan__single_perturb_gen_report.sh ${sp_model%.*} ${sp_species} ${results_dir} ${tc_parameter_scan_dir} ${param_scan__single_perturb_prefix_results_filename} ${tc_parameter_scan_dir} ${param_scan__single_perturb_legend}


done


printf "\n\n\n<END PIPELINE>\n\n\n"


