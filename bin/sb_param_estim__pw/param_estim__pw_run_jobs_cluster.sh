#!/bin/bash

# Author:     Piero Dalle Pezze
# Email:      piero.dallepezze@ncl.ac.uk
# Creation:   20/04/2013
# Modified:   09/05/2013
#
#
# This script aims at separating a long fits sequence of a model 
# into multiple short fits sequences (for the same model). 
# Therefore, it takes benefits of parallel computation.



# Import the libraries
. ${SB_PIPE_LIB}/bash/param_estim__pw_func.sh
. ${SB_PIPE_LIB}/bash/openlava_tasks.sh




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


# The user name (e.g. "npdp2")
user=""
# A list of servers that do not share /home (e.g. "iah372.ncl.ac.uk")
hosts=()   # a list separated by blanks
# The project name (e.g. "p3__mtor_foxo_ros")
project=""
# The model name  
model=""
# The association model-data file (e.g. modelname_dataset)
dataset=""
# Matlab setup file (e.g. setup_mixed_pop_distrib.m)
setup_file=""
# Matlab configuration file (e.g. pwConfigurationFile.mat)
configuration_file=""
# The number of jobs to be executed
# THIS IS A LIMIT FOR MATLAB/PottersWheelToolbox . It is impossible to 
# save/load a pw-repository bigger than 40,000 fits. (e.g. 40)
njobs=0
# The number of fits for each job (e.g. 500)
nfits=0
# The noise to be applied to each fit (e.g. 0.4)
noise=0
# The optimisation algorithm (e.g. 2  [Trust Region])
optim_algo=0
# Job name (e.g. fitseq)
job_name=""
# The folder pattern suffix (e.g. _cluster)
folder_pattern_suffix=""
# The work folder (e.g. working_folder)
work_folder=""
# The remote work folder (e.g. working_folder)
remote_work_folder=""
# The models folder (e.g. Models)
models_folder=""
# The remote models folder (e.g. Models)
remote_models_folder=""
# The data folder (e.g. data_folder)
data_folder=""
# The remote data folder (e.g. data_folder)
remote_data_folder=""


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
    ("dataset") 		echo "$line"; dataset="${array[1]}" ;;
    ("setup_file") 		echo "$line"; setup_file="${array[1]}" ;;
    ("configuration_file") 	echo "$line"; configuration_file="${array[1]}" ;;
    ("njobs") 			echo "$line"; njobs=${array[1]} ;;
    ("job_name") 		echo "$line"; job_name="${array[1]}" ;;       
    ("folder_pattern_suffix") 	echo "$line"; folder_pattern_suffix="${array[1]}" ;;
    ("optim_algo") 		echo "$line"; optim_algo=${array[1]} ;;
    ("nfits") 			echo "$line"; nfits=${array[1]} ;;
    ("noise") 			echo "$line"; noise=${array[1]} ;;    
    ("work_folder") 		echo "$line"; work_folder="${array[1]}" ;;
    ("remote_work_folder") 	echo "$line"; remote_work_folder="${array[1]}" ;;      
    ("models_folder") 		echo "$line"; models_folder="${array[1]}" ;;
    ("remote_models_folder") 	echo "$line"; remote_models_folder="${array[1]}" ;;      
    ("data_folder") 		echo "$line"; data_folder="${array[1]}" ;;
    ("remote_data_folder") 	echo "$line"; remote_data_folder="${array[1]}" ;;
  esac
done
IFS=$old_IFS



# main folder
main_folder="${model%.*}${folder_pattern_suffix}"

# pattern name of the folder to store the n-th fits sequence (e.g. fitseq - WITHOUT 'X', which will be replaced by a number)
folder_pattern="${main_folder}/${job_name%.*}"


# the local working directory
# the dir containing the parameter estimation output
workdir="${SB_PIPE}/${project}/${work_folder}"
# the remote working directory
# \ ahead of ${HOME} avoids the interpretation of the variable $HOME. This 
# is crucial since the variables $HOME on iah522 and iah372 (cluster) are different.
remote_workdir="\${SB_PIPE}/${project}/${remote_work_folder}"

# the local Models directory
# the dir containing the Models
modelsdir="${SB_PIPE}/${project}/${models_folder}"
# the remote Models directory
remote_modelsdir="\${SB_PIPE}/${project}/${remote_models_folder}"

# the local Data directory
# the dir containing the Data
datadir="${SB_PIPE}/${project}/${data_folder}"
# the remote Data directory
remote_datadir="\${SB_PIPE}/${project}/${remote_data_folder}"











printf "\nCleaning previous fits sequence folders locally and remotely ... "
`clean "${user}" hosts[@] "${main_folder}" "${workdir}" "${remote_workdir}"`
printf "DONE\n"


printf "\nCreating new fits sequence folders ... "
`create_job_folders "${workdir}" ${njobs} "${folder_pattern}"`
printf "DONE\n"


printf "\nCreating job files ... "
`create_job_files "${workdir}" ${njobs} "${job_name}" "${model}" "${dataset}" "${optim_algo}" "${nfits}" "${noise}" "${setup_file}"`
printf "DONE\n"


printf "\nCopying configuration ... "
`copy_config "${workdir}" ${njobs} "${job_name}" "${configuration_file}" "${setup_file}" "${dataset}" "${folder_pattern}"`
printf "DONE\n"


printf "\nUploading data ... "
`upload_data_to_remote_hosts "${user}" hosts[@] "${main_folder}" "${model}" "${modeldir}" "${remote_modelsdir}" "${datadir}" "${remote_datadir}" "${workdir}" "${remote_workdir}"`
printf "DONE\n"


printf "\nStarting Jobs ... "
`start_jobs "${workdir}/${folder_pattern}" "${job_name}" ${njobs}`
printf "DONE\n"







# INVOCATION OF SED REMOTELY ! THIS IS QUITE COOL !
# printf "Creating job files ..."
# for host in ${hosts[@]}
# do
#   ssh ${user}@${host} "cd ${remote_workdir} ; \
#                        for (( i=1; \${i} <= ${njobs}; i++ )) ; \
# 		       do  \
# 			  cp ${job_name} ${job_name%.*}\${i}.job ; \
# 			  pattern=\"s/${job_name%.*}/${job_name%.*}\${i}/g\" ; \
# 			  sed -i \$pattern ${job_name%.*}\${i}.job ; \
# 			  pattern=\"s/MODEL_FILE.m/${model}/g\" ; \
# 			  sed -i \$pattern ${job_name%.*}\${i}.job ; \
# 			  pattern=\"s/DATASET_FILE.xls/${dataset}/g\" ; \
# 			  sed -i \$pattern ${job_name%.*}\${i}.job ; \
# 			  pattern=\"s/SETUP_FILE.m/${setup_file}/g\" ; \
# 			  sed -i \$pattern ${job_name%.*}\${i}.job ; \
# 		       done "
# done
# printf "DONE\n"

