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

# This scripts provides the user with a complete pipeline of scripts comprising the configuration 
# and execution of jobs on the cluster, results retrieval and concatenation, parameter estimation 
# analyses and finally results storing.



# Import the library timer.sh for computing the pipeline elapsed time 
. ${PROJ_LIB}/bash/timer.sh




# Input parameters
# The file containing the model configuration, usually in working_folder (e.g. model.conf)
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
# The project name (e.g. "p3__mtor_foxo_ros")
project=""
# The work folder (e.g. working_folder)
work_folder=""
# The number of jobs to be executed
# THIS IS A LIMIT FOR MATLAB/PottersWheelToolbox . It is impossible to 
# save/load a pw-repository bigger than 40,000 fits. (e.g. 40)
njobs=0


# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("user")    	echo "$line"; user="${array[1]}" ;;
    ("project") 	echo "$line"; project="${array[1]}" ;; 
    ("work_folder") 	echo "$line"; work_folder="${array[1]}" ;;
    ("njobs")		echo "$line"; njobs=${array[1]} ;;
  esac
done
IFS=$old_IFS



# remove the path in case this was specified.
model_configuration=$(basename ${model_configuration})

model_configuration_with_path="${PROJ_DIR}/${project}/${work_folder}/${model_configuration}"
model_configuration_with_path__matlab="'${model_configuration_with_path}'"
scheduled_jobs=${njobs}




printf "\n\n\n<START PIPELINE>\n\n\n"
# Get the pipeline start time
tmr=$(timer)




printf "\n\n\n"
printf "########################################\n"
printf "Configure and start jobs on the cluster:\n"
printf "########################################\n"
${PROJ_DIR}/bin/param_estim__pw_run_jobs_cluster.sh ${model_configuration_with_path}
# Check jobs are running
while ((scheduled_jobs)); do
      sleep 2m
      scheduled_jobs=($(bjobs -u ${user} | wc -l))
done
# Let NFS transferring all data (in case of delays).
sleep 2m;



printf "\n\n\n"
printf "######################################\n"
printf "Retrieve the results from the cluster:\n"
printf "######################################\n"
printf "\n"
${PROJ_DIR}/bin/param_estim__pw_retrieve_results_cluster.sh ${model_configuration_with_path}
sleep 30s;



printf "\n\n\n"
printf "###############################################\n"
printf "Combine fits sequences computed on the cluster:\n"
printf "###############################################\n"
printf "\n"
${PROJ_DIR}/bin/param_estim__pw_combine_fitseqs_wrapper.sh ${model_configuration_with_path}
sleep 30s;



printf "\n\n\n"
printf "#################################\n"
printf "Executes model analyses (matlab):\n"
printf "#################################\n"
printf "\n"
# "-desktop" opens a matlab GUI ; "-r" passes a command to matlab (by command line).
matlab -desktop -r "try; PROJ_DIR=getenv('PROJ_DIR'); model_configuration=${model_configuration_with_path__matlab}; run([PROJ_DIR,'/bin/param_estim__pw_analyses_full_repository.m']); catch; end; quit; " &
# Wait until analyses are completed
matlab_pid=$!
wait ${matlab_pid}
sleep 30s;



printf "\n\n\n"
printf "######################################\n"
printf "Store the fits sequences in a tarball:\n"
printf "######################################\n"
printf "\n"
${PROJ_DIR}/bin/param_estim__pw_tarball_fitseqs.sh ${model_configuration_with_path} ${round}



# Print the pipeline elapsed time
printf '\n\n\nPipeline elapsed time: %s\n' $(timer $tmr) 
printf "\n<END PIPELINE>\n\n\n"


