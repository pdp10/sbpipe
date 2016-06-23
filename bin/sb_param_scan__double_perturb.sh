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
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-05-30 16:14:32 $

# This script processes the parted datasets of a double perturbation 
# experiment and generates the plots. 



# Import the library timer.sh for computing the pipeline elapsed time 
. ${SB_PIPE_LIB}/bash/timer.sh




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




# read the project name
project=""
# read the main model name (e.g. mtor_mito_ros_model_v27_pw3.m
model=""
# read the model pattern for the double perturbation (e.g. mtor_mito_ros_model_v27_scan_mTORC1_AMPK.cps)
# Since the generation of datasets for double perturbation is particularly expensive, it is reasonable 
# to split the task in subtasks. This is done by configuring the beginning and end of each sub-double perturbation 
# in Copasi. Each of this models will be called mtor_mito_ros_model_v27_scan_mTORC1_AMPK_k.cps, where 'k' is a 
# number between 1 and ${param_scan__double_perturb_subtasks_number}. This models will be unified using this script.
param_scan__double_perturb_copasi_model=""
# The number of subtasks (models) to be concatenated (e.g. 2)
param_scan__double_perturb_subtasks_number=2
# The length of the simulation (e.g 21)
param_scan__double_perturb_simulation_length=1
# The species to be perturbed (e.g. mTORC1_AMPK)
param_scan__double_perturb_copasi_species=""
# The suffix of the folder containing the dataset (e.g. _dataset)
param_scan__double_perturb_suffix_dataset_folder=""
# The suffix of the folder containing the plots (e.g. _plots)
param_scan__double_perturb_suffix_plots_folder=""
# The number of intervals for the first variable to be perturbed (e.g. mTORC1)
param_scan__double_perturb_intervals_first_species=9 
# The type of perturbation for the first species among: inhibition, overexpression, mixed
param_scan__double_perturb_type_first_species="inhibition" 
# The number of intervals for the second variable to be perturbed (e.g. AMPK)
param_scan__double_perturb_intervals_second_species=9 
# The type of perturbation for the first species among: inhibition, overexpression, mixed
param_scan__double_perturb_type_second_species="inhibition" 
# A boolean (e.g. false)
param_scan__double_perturb_plots_3D=""
# A boolean (e.g. true)
param_scan__double_perturb_plots_2D_pub=""
# The folder containing the models
models_folder=""
# The folder containing the models simulations
simulations_folder=""
# The folder containing the temporary computations
tmp_folder=""
# The folder of the double perturbation data sets (e.g. double_perturb)
double_perturb_dir=""



# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("project") 						echo "$line"; project="${array[1]}" ;; 
    ("model") 							echo "$line"; model="${array[1]}" ;;    
    ("param_scan__double_perturb_copasi_model") 		echo "$line"; param_scan__double_perturb_copasi_model="${array[1]}" ;;    
    ("param_scan__double_perturb_subtasks_number") 		echo "$line"; param_scan__double_perturb_subtasks_number=${array[1]} ;;
    ("param_scan__double_perturb_simulation_length") 		echo "$line"; param_scan__double_perturb_simulation_length=${array[1]} ;;  
    ("double_perturb_dir") 					echo "$line"; double_perturb_dir="${array[1]}" ;;
    ("param_scan__double_perturb_copasi_species") 		echo "$line"; param_scan__double_perturb_copasi_species="${array[1]}" ;;    
    ("param_scan__double_perturb_suffix_dataset_folder") 	echo "$line"; param_scan__double_perturb_suffix_dataset_folder="${array[1]}" ;;
    ("param_scan__double_perturb_suffix_plots_folder") 		echo "$line"; param_scan__double_perturb_suffix_plots_folder="${array[1]}" ;; 
    ("param_scan__double_perturb_intervals_first_species") 	echo "$line"; param_scan__double_perturb_intervals_first_species=${array[1]} ;; 
    ("param_scan__double_perturb_type_first_species") 		echo "$line"; param_scan__double_perturb_type_first_species="${array[1]}" ;;     
    ("param_scan__double_perturb_intervals_second_species") 	echo "$line"; param_scan__double_perturb_intervals_second_species=${array[1]} ;; 
    ("param_scan__double_perturb_type_second_species") 		echo "$line"; param_scan__double_perturb_type_second_species="${array[1]}" ;;     
    ("param_scan__double_perturb_plots_3D") 			echo "$line"; param_scan__double_perturb_plots_3D="${array[1]}" ;;  
    ("param_scan__double_perturb_plots_2D_pub") 		echo "$line"; param_scan__double_perturb_plots_2D_pub="${array[1]}" ;;    
    ("models_folder") 						echo "$line"; models_folder="${array[1]}" ;;    
    ("simulations_folder") 					echo "$line"; simulations_folder="${array[1]}" ;;   
    ("tmp_folder") 						echo "$line"; tmp_folder="${array[1]}" ;;        
  esac
done
IFS=$old_IFS




models_dir="${project}/${models_folder}/"
tmp_dir="${project}/${tmp_folder}/"

# The double perturbation path
dp_dir="${project}/${simulations_folder}/${model%.*}/${double_perturb_dir}/"
# The path-directory containing the double perturbation dataset
dp_datasets_dir="${dp_dir}/${param_scan__double_perturb_copasi_species}${param_scan__double_perturb_suffix_dataset_folder}/"
# The path-directory containing the double perturbation plots
dp_plots_dir="${dp_dir}/${param_scan__double_perturb_copasi_species}${param_scan__double_perturb_suffix_plots_folder}/"






printf "\n\n\n<START PIPELINE>\n\n\n"
# Get the pipeline start time
tmr=$(timer)



printf "\n\n\n"
printf "##############################################################################\n"      
printf "##############################################################################\n"
printf "### Processing model: ${param_scan__double_perturb_copasi_model}\n"
printf "##############################################################################\n"
printf "##############################################################################\n"
printf "\n\n"



printf "\n\n\n"
printf "###############################\n"
printf "Cleaning folder ${dp_dir}:\n"
printf "###############################\n"
printf "\n"
rm -rf ${dp_datasets_dir}
rm -rf ${dp_plots_dir}
mkdir -p ${dp_datasets_dir} ${dp_plots_dir}


printf "\n\n\n"
printf "#####################################################\n"
if [ "${param_scan__double_perturb_subtasks_number}" -eq "1" ]; then
    # Use only one copasi for calculating the double perturbation
    printf "Perform double perturbation using Copasi:\n"
    printf "(Results in ${dp_datasets_dir})\n"
    printf "#####################################################\n"
    printf "\n"
    CopasiSE --nologo ${models_dir}/${param_scan__double_perturb_copasi_model}
    mv ${tmp_dir}/${param_scan__double_perturb_copasi_model%.*}.csv ${dp_datasets_dir}/
elif [ "${param_scan__double_perturb_subtasks_number}" -ge "1" ]; then 
    # Use ${param_scan__double_perturb_subtasks_number} copasi for calculating the double perturbation
    printf "Perform double perturbation using Copasi in parallel:\n"
    printf "(Results in ${dp_datasets_dir})\n"
    printf "#####################################################\n"
    printf "\n"
    bash ${SB_PIPE}/bin/run_generic__copasi_concur_local.sh ${models_dir} ${param_scan__double_perturb_copasi_model%.*}_ 1 ${param_scan__double_perturb_subtasks_number} 5 &
    # Wait until the routine is completed
    copasi_pid=$!
    wait ${copasi_pid}
    sleep 30s;
    mv ${tmp_dir}/${param_scan__double_perturb_copasi_model%.*}*.csv ${dp_datasets_dir}/    
    printf "\n\n\n"
    printf "##########################################################################################################################################\n"
    printf "Concatenates the parted files of a double perturbation experiment (${param_scan__double_perturb_subtasks_number} subfiles => 1 merged file):\n"
    printf "##########################################################################################################################################\n"
    printf "\n"
    bash ${SB_PIPE}/bin/sb_param_scan__double_perturb/param_scan__double_perturb_concat_files.sh ${dp_datasets_dir} ${param_scan__double_perturb_copasi_model} ${param_scan__double_perturb_subtasks_number}
fi



printf "\n\n\n"
printf "###########################################################################################################################################\n"
printf "Extract the single timepoints of the double perturbation (1 merged file => ${param_scan__double_perturb_simulation_length} time-point files):\n"
printf "###########################################################################################################################################\n"
printf "\n"
bash ${SB_PIPE}/bin/sb_param_scan__double_perturb/param_scan__double_perturb_extract_timepoints.sh ${dp_datasets_dir} ${param_scan__double_perturb_copasi_model} ${param_scan__double_perturb_simulation_length}



printf "\n\n\n"
printf "####################################\n"
printf "Generate plots for each time points:\n"
printf "####################################\n"
printf "\n"
# "-desktop" opens a matlab GUI ; "-r" passes a command to matlab (by command line).
matlab -desktop -r "try; SB_PIPE=getenv('SB_PIPE'); dp_dir='"${dp_dir}"'; dp_datasets_dir='"${dp_datasets_dir}"'; perturbed_species='"${param_scan__double_perturb_copasi_species}"'; param_scan__double_perturb_suffix_plots_folder='"${param_scan__double_perturb_suffix_plots_folder}"'; param_scan__double_perturb_intervals_first_species=${param_scan__double_perturb_intervals_first_species}; param_scan__double_perturb_type_first_species='"${param_scan__double_perturb_type_first_species}"'; param_scan__double_perturb_intervals_second_species=${param_scan__double_perturb_intervals_second_species}; param_scan__double_perturb_type_second_species='"${param_scan__double_perturb_type_second_species}"'; param_scan__double_perturb_plots_3D='"${param_scan__double_perturb_plots_3D}"'; param_scan__double_perturb_plots_2D_pub='"${param_scan__double_perturb_plots_2D_pub}"'; run([SB_PIPE,'/bin/sb_param_scan__double_perturb/param_scan__double_perturb_plot_surfaces.m']); catch; end; quit; "






# Print the pipeline elapsed time
printf '\n\n\nPipeline elapsed time: %s\n' $(timer $tmr) 
printf "\n<END PIPELINE>\n\n\n"
