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
   exec >&2; echo "error: round number not defined. Please, add the round number as parameter"; exit 1
fi




printf "\nReading file ${model_configuration} : \n"
# import the model configuration data (project, model-name, association-pattern)
old_IFS=$IFS
IFS=$'\n'
lines=($(cat ${model_configuration}))  # array
IFS=$old_IFS
printf "\n\n"

# The user name
user="user"
# The server to connect (e.g. localhost,my-node.abc.ac.uk)
server_list="localhost"
# The port to connect for the above server (e.g. 65000,24000)
port_list="65000"
# The secret key to communicate for the above server
secret="donald_duck"
# read the project name
project="my_project"
# The number of jobs to be executed
nfits=10
# The number of cpus to use locally (if ncpus=0, it should run on a cluster).
local_cpus=2
# read the copasi model name 
param_estim__copasi_model="mymodel.cps"
# The folder containing the models
models_folder="Models"
# The folder containing the data
data_folder="Data"
# The folder containing the working results
working_folder="Working_Folder"
# The folder containing the temporary computations
tmp_folder="tmp"
# The remote folder containing the models
remote_models_folder="Models"
# The remote folder containing the data
remote_data_folder="Data"
# The remote folder containing the working results
remote_working_folder="Working_Folder"
# The remote folder containing the temporary computations
remote_tmp_folder="tmp"




# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("user")    			echo "$line"; user="${array[1]}" ;;
    ("server_list")    			echo "$line"; server_list="${array[1]}" ;;
    ("port_list")    			echo "$line"; port_list="${array[1]}" ;;    
    ("secret")    			echo "$line"; secret="${array[1]}" ;;    
    ("project") 			echo "$line"; project="${array[1]}" ;; 
    ("nfits")				echo "$line"; nfits=${array[1]} ;;
    ("local_cpus")			echo "$line"; local_cpus=${array[1]} ;;
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


models_dir="${project}/${models_folder}/"
data_dir="${project}/${data_folder}/"
tmp_dir="${project}/${tmp_folder}/"
working_dir="${project}/${working_folder}/"

output_folder=${param_estim__copasi_model%.*}_round${round}



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
# remove the folder containing the parameter estimation for this round
rm -rf ${working_dir}/${output_folder}
mkdir -p ${model_dir} ${data_dir} ${tmp_dir} ${working_dir} ${working_dir}/${output_folder}


printf "\n\n\n"
printf "#######################\n"
printf "Configure jobs locally:\n"
printf "#######################\n"
python ${SB_PIPE}/bin/sb_param_estim__copasi/param_estim__copasi_utils_randomise_start_values.py ${models_dir} ${param_estim__copasi_model} ${nfits}




printf "\n\n\n"
printf "################################\n"
printf "Concurrent parameter estimation:\n"
printf "################################\n"
# for some reason, CopasiSE ignores the "../" for the data file and assumes that the Data folder is inside the Models folder..
# Let's temporarily copy this folder and then delete it. 
cp -R ${data_dir} ${models_dir}/

# Perform this task using python-pp (parallel python dependency). 
# If this computation is performed on a cluster, start this on each node of the cluster. 
# The list of servers and ports must be updated in the configuration file
# (NOTE: It requires the installation of python-pp)
#ppserver -p 65000 -i my-node.abc.ac.uk -s "donald_duck" -w 5 &

# Perform this task using python-pp (parallel python dependency)
python ${SB_PIPE}/bin/sb_param_estim__copasi/param_estim__copasi_parallel.py ${server_list} ${port_list} ${secret} ${models_dir} ${param_estim__copasi_model%.*} ${nfits} ${local_cpus}

# Perform this task directly (no parallel python dependency).
#bash ${SB_PIPE}/bin/sb_param_estim__copasi/run_generic__copasi_concur_local.sh ${models_dir} ${param_estim__copasi_model%.*} 1 ${nfits} ${local_cpus}

# remove the previously copied Data folder
#rm -rf ${models_dir}/${data_folder}




printf "\n\n\n"
printf "################\n"
printf "Collect results:\n"
printf "################\n"
printf "\n"
# Collect and summarises the parameter estimation results
python ${SB_PIPE}/bin/sb_param_estim__copasi/param_estim__copasi_utils_collect_results.py ${tmp_dir}

# plot the fitting curve using data from the fit sequence 
# This requires extraction of a couple of fields from the Copasi output file for parameter estimation.
#python ${SB_PIPE}/bin/sb_param_estim__copasi/param_estim__copasi_utils_plot_calibration.py ${tmp_dir} ${tmp_dir}




printf "\n\n\n"
printf "######################################\n"
printf "Store the fits sequences in a tarball:\n"
printf "######################################\n"
printf "\n"
mv ${tmp_dir}/*.csv ${working_dir}/${output_folder}
cd ${working_dir}
tar cvzf ${output_folder}.tgz ${output_folder}
cd -



# Print the pipeline elapsed time
printf '\n\n\nPipeline elapsed time: %s\n' $(timer $tmr) 
printf "\n<END PIPELINE>\n\n\n"


