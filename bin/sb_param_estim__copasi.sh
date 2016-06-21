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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-05-30 16:14:32 $

# This scripts provides the user with a complete pipeline of scripts comprising the configuration 
# and execution of jobs on the cluster, results retrieval and concatenation, parameter estimation 
# analyses and finally results storing. This pipeline uses CopasiSE



# Import the library timer.sh for computing the pipeline elapsed time 
. ${SB_PIPE_LIB}/bash/timer.sh




# Input parameters
# The file containing the model configuration, usually in workinging_folder (e.g. model.conf)
model_configuration=$1
# The current round number
round=$2


if ! [[ "$round" =~ ^[0-9]+$ ]] ; then
   exec >&2; echo "error: round must be a number"; exit 1
fi




printf "\nReading file ${model_configuration} : \n"
# import the model configuration data (project, model-name, association-pattern)
old_IFS=$IFS
IFS=$'\n'
lines=($(cat ${model_configuration}))  # array
IFS=$old_IFS
printf "\n\n"

# The user name (e.g. "npdp2")
user=""
# read the project name
project=""
# The working folder (e.g. workinging_folder)
working_folder=""
# The number of jobs to be executed
nfits=0

# read the copasi model name 
param_estim__copasi_model=""
# The folder containing the models
models_folder=""
# The folder containing the data
data_folder=""
# The folder containing the working results
working_folder=""
# The folder containing the temporary computations
tmp_folder=""
# The remote folder containing the models
remote_models_folder=""
# The remote folder containing the data
remote_data_folder=""
# The remote folder containing the working results
remote_working_folder=""
# The remote folder containing the temporary computations
remote_tmp_folder=""




# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("user")    			echo "$line"; user="${array[1]}" ;;
    ("project") 			echo "$line"; project="${array[1]}" ;; 
    ("working_folder") 			echo "$line"; working_folder="${array[1]}" ;;
    ("nfits")				echo "$line"; nfits=${array[1]} ;;
    
    ("param_estim__copasi_model") 	echo "$line"; param_estim__copasi_model="${array[1]}" ;;
    ("models_folder") 			echo "$line"; models_folder="${array[1]}" ;;
    ("data_folder") 			echo "$line"; data_folder="${array[1]}" ;;
    ("working_folder") 			echo "$line"; working_folder="${array[1]}" ;;
    ("tmp_folder") 			echo "$line"; tmp_folder="${array[1]}" ;;
    ("remote_models_folder") 		echo "$line"; remote_models_folder="${array[1]}" ;;
    ("remote_data_folder") 		echo "$line"; remote_data_folder="${array[1]}" ;;
    ("remote_working_folder") 		echo "$line"; remote_working_folder="${array[1]}" ;;
    ("remote_tmp_folder") 		echo "$line"; remote_tmp_folder="${array[1]}" ;;    
  esac
done
IFS=$old_IFS





# remove the path in case this was specified.
#model_configuration=$(basename ${model_configuration})
#model_configuration_with_path="${SB_PIPE}/${project}/${working_folder}/${model_configuration}"


models_dir="${SB_PIPE}/${project}/${models_folder}/"
data_dir="${SB_PIPE}/${project}/${data_folder}/"
tmp_dir="${SB_PIPE}/${project}/${tmp_folder}/"
working_dir="${SB_PIPE}/${project}/${working_folder}/"




printf "\n\n\n<START PIPELINE>\n\n\n"
# Get the pipeline start time
tmr=$(timer)

    
printf "\n\n\n"
printf "##############################################################\n"      
printf "##############################################################\n"
printf "### Parameter estimation for model ${param_estim__copasi_model} \n"
printf "##############################################################\n"
printf "##############################################################\n"
printf "\n\n"
      

      
printf "\n\n\n"
printf "##################\n"
printf "Preparing folders:\n"
printf "##################\n"
printf "\n"
mkdir -p ${model_dir} ${data_dir} ${tmp_dir} ${working_dir}


printf "\n\n\n"
printf "#######################\n"
printf "Configure jobs locally:\n"
printf "#######################\n"
python ${SB_PIPE}/bin/sb_param_estim__copasi/param_estim__copasi_utils_randomise_start_values.py ${models_dir} ${param_estim__copasi_model} ${nfits}








# 
# 
# 
# printf "\n\n\n"
# printf "########################################\n"
# printf "Configure and start jobs on the cluster:\n"
# printf "########################################\n"
# ${SB_PIPE}/bin/sb_param_estim__pw/param_estim__pw_run_jobs_cluster.sh ${model_configuration_with_path}
# # Check jobs are running
# while ((scheduled_jobs)); do
#       sleep 2m
#       scheduled_jobs=($(bjobs -u ${user} | wc -l))
# done
# # Let NFS transferring all data (in case of delays).
# sleep 2m;
# 
# 
# 
# printf "\n\n\n"
# printf "######################################\n"
# printf "Retrieve the results from the cluster:\n"
# printf "######################################\n"
# printf "\n"
# ${SB_PIPE}/bin/sb_param_estim__pw/param_estim__pw_retrieve_results_cluster.sh ${model_configuration_with_path}
# sleep 30s;
# 
# 
# 
# printf "\n\n\n"
# printf "###############################################\n"
# printf "Combine fits sequences computed on the cluster:\n"
# printf "###############################################\n"
# printf "\n"
# ${SB_PIPE}/bin/sb_param_estim__pw/param_estim__pw_combine_fitseqs_wrapper.sh ${model_configuration_with_path}
# sleep 30s;
# 
# 
# 
# printf "\n\n\n"
# printf "#################################\n"
# printf "Executes model analyses (matlab):\n"
# printf "#################################\n"
# printf "\n"
# # "-desktop" opens a matlab GUI ; "-r" passes a command to matlab (by command line).
# matlab -desktop -r "try; SB_PIPE=getenv('SB_PIPE'); model_configuration=${model_configuration_with_path__matlab}; run([SB_PIPE,'/bin/sb_param_estim__pw/param_estim__pw_analyses_full_repository.m']); catch; end; quit; " &
# # Wait until analyses are completed
# matlab_pid=$!
# wait ${matlab_pid}
# sleep 30s;
# 
# 
# 
# printf "\n\n\n"
# printf "######################################\n"
# printf "Store the fits sequences in a tarball:\n"
# printf "######################################\n"
# printf "\n"
# ${SB_PIPE}/bin/sb_param_estim__pw/param_estim__pw_tarball_fitseqs.sh ${model_configuration_with_path} ${round}
# 
# 
# 
# # Print the pipeline elapsed time
# printf '\n\n\nPipeline elapsed time: %s\n' $(timer $tmr) 
# printf "\n<END PIPELINE>\n\n\n"
# 
# 
