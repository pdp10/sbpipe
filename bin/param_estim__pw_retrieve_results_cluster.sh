#!/bin/bash

# Author:     Piero Dalle Pezze
# Email:      piero.dallepezze@ncl.ac.uk
# Creation:   20/04/2013
# Modified:   09/05/2013
#
# This script imports the computed fits sequences from the cluster server to this local machine.m'



# Import the libraries
. ${PROJ_LIB}/bash/param_estim__pw_func.sh





# Input parameters
# The file containing the model configuration, usually in working_folder (e.g. model.conf)
model_configuration=$1



printf "Reading file ${model_configuration} : \n"
# import the model configuration data (project, model-name, association-pattern)
old_IFS=$IFS
IFS=$'\n'
lines=($(cat ${model_configuration}))  # array
IFS=$old_IFS
printf "\n"




# The user name (e.g. "npdp2")
user=""
# A list of servers that do not share /home (e.g. "iah372.ncl.ac.uk")
hosts=()
# The project name (e.g. "p3__mtor_foxo_ros")
project=""
# The model name  
model=""
# The folder pattern suffix (e.g. _cluster)
folder_pattern_suffix=""
# The work folder (e.g. working_folder)
work_folder=""
# The remote work folder (e.g. working_folder)
remote_work_folder=""


# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("user")    		echo "$line"; user="${array[1]}" ;;
    ("hosts")			echo "$line"; hosts=("${array[1]}") ;;     
    ("project") 		echo "$line"; project="${array[1]}" ;; 
    ("model") 			echo "$line"; model="${array[1]}" ;;
    ("folder_pattern_suffix") 	echo "$line"; folder_pattern_suffix="${array[1]}" ;;
    ("work_folder") 		echo "$line"; work_folder="${array[1]}" ;;
    ("remote_work_folder") 	echo "$line"; remote_work_folder="${array[1]}" ;;      
  esac  
done
IFS=$old_IFS



# main folder
main_folder="${model%.*}${folder_pattern_suffix}"

# the local working directory
# the dir containing the parameter estimation output
workdir="${PROJ_DIR}/${project}/${work_folder}"
# the remote working directory
# \ ahead of ${HOME} avoids the interpretation of the variable $HOME. This 
# is crucial since the variables $HOME on iah522 and iah372 (cluster) are different.
remote_workdir="\${PROJ_DIR}/${project}/${remote_work_folder}"




printf "\nImporting files from ${hosts[@]} ... "
`download_data_to_remote_hosts "${user}" hosts[@] "${main_folder}" "${workdir}" "${remote_workdir}"`
printf "DONE\n"
