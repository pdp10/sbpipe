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
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-05-30 16:14:32 $

# This scripts provides the user with a complete pipeline of scripts for computing 
# a single parameter scan using copasi.



# Import the library timer.sh for computing the pipeline elapsed time 
. ${SB_PIPE_LIB}/utils/bash/timer.sh




# Input parameters
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
# The folder containing the models
models_folder=""
# The folder containing the models simulations
simulations_folder=""
# The folder containing the temporary computations
tmp_folder=""
# The starting time point of the simulation (e.g. 0)
# This is required for plotting
simulate__start=0
# The ending time point of the simulation (e.g. 120)
# This is required for plotting
simulate__end=10
# The plot x axis label (e.g. Time[min])
# This is required for plotting
simulate__xaxis_label="Time [min]"
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
# The perturbation is performed on percent levels (true) or through a modelled inhibitor/expressor (false)
param_scan__single_perturb_perturbation_in_percent_levels="true"
# The number of levels of inhibition/over-expression
param_scan__single_perturb_levels_number=10
# The name of the folder containing the computed dataset of the parameter scanning (e.g. dataset_parameter_scan)
dataset_parameter_scan_dir=""
# The name of the folder containing the generated plots of the parameter scanning (e.g. tc_parameter_scan)
tc_parameter_scan_dir=""



# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("project") 						echo "$line"; project="${array[1]}" ;; 
    ("model") 							echo "$line"; model="${array[1]}" ;;
    ("param_scan__single_perturb_copasi_models_list") 		echo "$line"; param_scan__single_perturb_copasi_models_list="${array[1]}" ;;
    ("param_scan__single_perturb_species_list") 		echo "$line"; param_scan__single_perturb_species_list="${array[1]}" ;;
    ("param_scan__single_perturb_knock_down_only") 		echo "$line"; param_scan__single_perturb_knock_down_only="${array[1]}" ;;    
    ("models_folder") 						echo "$line"; models_folder="${array[1]}" ;;    
    ("simulations_folder") 					echo "$line"; simulations_folder="${array[1]}" ;;
    ("tmp_folder") 						echo "$line"; tmp_folder="${array[1]}" ;;
    ("simulate__start") 					echo "$line"; simulate__start="${array[1]}" ;;
    ("simulate__end")						echo "$line"; simulate__end="${array[1]}" ;;
    ("simulate__interval_size") 				echo "$line"; simulate__interval_size=${array[1]} ;;    
    ("simulate__xaxis_label")					echo "$line"; simulate__xaxis_label="${array[1]}" ;;      
    ("param_scan__single_perturb_legend") 			echo "$line"; param_scan__single_perturb_legend="${array[1]}" ;;      
    ("param_scan__single_perturb_min_inhibition_level") 	echo "$line"; param_scan__single_perturb_min_inhibition_level=${array[1]} ;;      
    ("param_scan__single_perturb_max_overexpression_level") 	echo "$line"; param_scan__single_perturb_max_overexpression_level=${array[1]} ;;
    ("param_scan__single_perturb_prefix_results_filename") 	echo "$line"; param_scan__single_perturb_prefix_results_filename="${array[1]}" ;;    
    ("param_scan__single_perturb_simulations_number") 		echo "$line"; param_scan__single_perturb_simulations_number=${array[1]} ;;      
    ("param_scan__single_perturb_perturbation_in_percent_levels") echo "$line"; param_scan__single_perturb_perturbation_in_percent_levels="${array[1]}" ;;        
    ("param_scan__single_perturb_levels_number") 		echo "$line"; param_scan__single_perturb_levels_number=${array[1]} ;;        
    ("dataset_parameter_scan_dir") 				echo "$line"; dataset_parameter_scan_dir="${array[1]}" ;;
    ("tc_parameter_scan_dir") 					echo "$line"; tc_parameter_scan_dir="${array[1]}" ;;      
  esac
done
IFS=$old_IFS
   
   
### NOTE
# For some reason, a list assignment seems not to work inside a case-esac construct..
# Particularly, the following assignments don't work:
#   param_scan__single_perturb_copasi_models_list=("${array[1]}")
#   param_scan__single_perturb_species_list=("${array[1]}")
param_scan__single_perturb_copasi_models_list=(${param_scan__single_perturb_copasi_models_list})
param_scan__single_perturb_species_list=(${param_scan__single_perturb_species_list})

   
if [ "$simulate__start" -ge "$simulate__end" ] 
then
  printf "\n ERROR: simulate__start must be less than simulate__end \n\n"
  exit 1
fi



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





models_dir="${project}/${models_folder}/"
results_dir="${project}/${simulations_folder}/${model%.*}/"
tmp_dir="${project}/${tmp_folder}/"




printf "\n\n\n<START PIPELINE>\n\n\n"
# Get the pipeline start time
tmr=$(timer)




for ((i=0; $i < ${#param_scan__single_perturb_species_list[@]}; i++))
do
      
      sp_species="${param_scan__single_perturb_species_list[${i}]}"
      sp_model="${param_scan__single_perturb_copasi_models_list[${i}]}"
         
      
      if [ ! -f "${models_dir}/${sp_model}" ]; then 
	echo "${models_dir}/${sp_model} does not exist." 
	exit 1
      fi
      
      
      printf "\n\n\n"
      printf "################################\n"      
      printf "################################\n"
      printf "### Processing model ${sp_model}\n"
      printf "################################\n"
      printf "################################\n"
      printf "\n\n"
      

      
      printf "\n\n\n"
      printf "###################################################\n"
      printf "Cleaning previous results in folder ${results_dir}:\n"
      printf "###################################################\n"
      printf "\n"
      rm -rf ${results_dir}/${dataset_parameter_scan_dir}/${sp_model%.*}*
      rm -rf ${results_dir}/${tc_parameter_scan_dir}/${sp_model%.*}*
      rm -rf ${results_dir}/${tc_parameter_scan_dir}/${param_scan__single_perturb_legend}_${sp_species}*
      rm -rf ${results_dir}/${param_scan__single_perturb_prefix_results_filename}*${sp_model%.*}*
      mkdir -p ${tmp_dir} ${results_dir}/${dataset_parameter_scan_dir} ${results_dir}/${tc_parameter_scan_dir}



      printf "\n\n\n"
      printf "######################\n"
      printf "Executing simulations:\n"
      printf "######################\n"
      printf "\n"
      bash ${SB_PIPE_LIB}/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_run_copasi.sh ${sp_model} ${sp_species} ${param_scan__single_perturb_simulations_number} ${models_dir} ${results_dir}/${dataset_parameter_scan_dir} ${tmp_dir} 



      # Comment if you want to have the knockdown. If so, you must edit plot colours in param_scan__single_perturb_plot.R 
      if [ "${param_scan__single_perturb_perturbation_in_percent_levels}" == "true" ]; then
	printf "\n\n\n"
	printf "########################\n"
	printf "Removing knock out data:\n"
	printf "########################\n"  
	printf "\n"
	rm -rf ${results_dir}/${dataset_parameter_scan_dir}/${sp_model%.*}*__level_0.csv      
      fi
      
      
      
      printf "\n\n\n"
      printf "#################\n"
      printf "Generating plots:\n"
      printf "#################\n"
      printf "\n"
      Rscript ${SB_PIPE_LIB}/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_plot.R ${sp_model%.*} ${sp_species} ${param_scan__single_perturb_knock_down_only} ${results_dir} ${dataset_parameter_scan_dir} ${tc_parameter_scan_dir} ${simulate__start} ${simulate__end} ${simulate__interval_size} "${simulate__xaxis_label}" ${param_scan__single_perturb_simulations_number} ${param_scan__single_perturb_perturbation_in_percent_levels}
      # Prepare the legend
      if [ "${param_scan__single_perturb_knock_down_only}" == "true" ] ; then
	  Rscript ${SB_PIPE_LIB}/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_make_legend.R ${results_dir}/${tc_parameter_scan_dir}/ ${param_scan__single_perturb_legend}_${sp_species} ${param_scan__single_perturb_min_inhibition_level} 100 ${param_scan__single_perturb_knock_down_only} ${param_scan__single_perturb_perturbation_in_percent_levels} ${param_scan__single_perturb_levels_number}
      else
	  Rscript ${SB_PIPE_LIB}/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_make_legend.R ${results_dir}/${tc_parameter_scan_dir}/ ${param_scan__single_perturb_legend}_${sp_species} ${param_scan__single_perturb_min_inhibition_level} ${param_scan__single_perturb_max_overexpression_level} ${param_scan__single_perturb_knock_down_only} ${param_scan__single_perturb_perturbation_in_percent_levels} ${param_scan__single_perturb_levels_number}
      fi 



      printf "\n\n\n"
      printf "###################\n"
      printf "Generating reports:\n"
      printf "###################\n"
      printf "\n"
      python ${SB_PIPE_LIB}/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_gen_report.py ${sp_model%.*} ${sp_species} ${results_dir} ${tc_parameter_scan_dir} ${param_scan__single_perturb_prefix_results_filename} ${param_scan__single_perturb_legend}_${sp_species}


done

# Print the pipeline elapsed time
printf "\n\n\nPipeline elapsed time: %s\n" $(timer $tmr)
printf "\n<END PIPELINE>\n\n\n"

