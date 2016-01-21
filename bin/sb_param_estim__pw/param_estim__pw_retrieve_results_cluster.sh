#!/bin/bash
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $
#
# This script imports the computed fits sequences from the cluster server to this local machine.m'



# Import the libraries
. ${SB_PIPE_LIB}/bash/param_estim__pw_func.sh





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
workdir="${SB_PIPE}/${project}/${work_folder}"
# the remote working directory
# \ ahead of ${HOME} avoids the interpretation of the variable $HOME. This 
# is crucial since the variables $HOME on iah522 and iah372 (cluster) are different.
remote_workdir="\${SB_PIPE}/${project}/${remote_work_folder}"




printf "\nImporting files from ${hosts[@]} ... "
`download_data_to_remote_hosts "${user}" hosts[@] "${main_folder}" "${workdir}" "${remote_workdir}"`
printf "DONE\n"
