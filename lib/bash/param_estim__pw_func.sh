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
#
# Library of functions integrating openlava and potterswheel.






# Cleans the previous computed results, if any
# Input parameters:
# user:			The user name (e.g. npdp2)
# hosts: 		A list of servers that do not share /home (e.g. "iah372.ncl.ac.uk")
# main_folder:		The main folder containing the fits sequences folders
# workdir:		The local working directory containing the parameter estimation output
# remote_workdir:	The remote working directory containing the parameter estimation output
function clean() 
{
  local user=$1
  declare -a hosts=("${!2}")
  local main_folder=$3
  local workdir=$4
  local remote_workdir=$5

  # locally
  rm -rf ${workdir}/${main_folder}

  # remotely
  for host in ${hosts[@]}
  do
    ssh ${user}@${host} "rm -rf ${remote_workdir}/${main_folder} ; "
  done
}





# Creates the job configuration files
# Input parameters:
# workdir:		The local working directory containing the parameter estimation output
# njobs:		The number of jobs to be executed
# job_name:		The job name (e.g. fitseq)
# model:		The model name
# dataset:		The association model-data file (e.g. modelname_dataset)
# optim_algo:		The optimisation algorithm (e.g. 2  [Trust Region])
# nfits:		The number of fits for each job (e.g. 500)
# noise:		The noise to be applied to each fit (e.g. 0.4)
# setup_file:		Matlab setup file (e.g. setup_mixed_pop_distrib.m)
function create_job_files()
{
  local workdir=$1
  local njobs=$2
  local job_name=$3
  local model=$4
  local dataset=$5
  local optim_algo=$6
  local nfits=$7
  local noise=$8
  local setup_file=$9
  
  for (( i=1; ${i} <= ${njobs}; i++ ))
  do 
      jobfile_i="${workdir}/${job_name%.*}${i}.job"
      cp ${job_name} ${jobfile_i}
      sed -i "s/${job_name%.*}/${job_name%.*}${i}/g" ${jobfile_i}
      sed -i "s/MODEL_FILE.m/${model}/g" ${jobfile_i}
      sed -i "s/DATASET_FILE.xls/${dataset}/g" ${jobfile_i}
      sed -i "s/OPTIM_ALGO/${optim_algo}/g" ${jobfile_i}
      sed -i "s/NFITS/${nfits}/g" ${jobfile_i}
      sed -i "s/NOISE/${noise}/g" ${jobfile_i}   
      sed -i "s/SETUP_FILE.m/${setup_file}/g" ${jobfile_i}
  done
}





# Copy job configurations and dependencies files to each folder_pattern
# Input parameters:
# workdir:		The local working directory containing the parameter estimation output
# njobs:		The number of jobs to be executed
# job_name:		The job name (e.g. fitseq)
# configuration_file:	Matlab configuration file (e.g. pwConfigurationFile.mat)
# setup_file:		Matlab setup file (e.g. setup_mixed_pop_distrib.m)
# dataset:		The association model-data file (e.g. modelname_dataset)
# folder_pattern:	The pattern name of the folder to store the n-th fits sequence (e.g. fitseq - WITHOUT 'X', which will be replaced by a number)
function copy_config()
{
  local workdir=$1
  local njobs=$2
  local job_name=$3
  local configuration_file=$4
  local setup_file=$5
  local dataset=$6
  local folder_pattern=$7
  
  for (( i=1; ${i} <= ${njobs}; i++ ))
  do
    full_folder_pattern_i="${workdir}/${folder_pattern}${i}/"
    mv ${job_name%.*}${i}.job ${full_folder_pattern_i}
    cp ${configuration_file} ${full_folder_pattern_i}/
    cp ${setup_file} ${full_folder_pattern_i}/
    cp ${dataset%.*}*.mat ${full_folder_pattern_i}/
  done
}





# Upload model, dataset and jobs folders containing the job configurations to each remote host.
# Input parameters:
# user:			The user name (e.g. npdp2)
# hosts: 		A list of servers that do not share /home (e.g. "iah372.ncl.ac.uk")
# main_folder:		The main folder containing the fits sequences folders
# model:		The model name
# modeldir:		The local Models directory containing the Models
# remote_modeldir:	The remote Models directory containing the Models
# datadir:		The local Data directory containing the Data
# remote_datadir:	The remote Data directory containing the Data
# workdir:		The local working directory containing the parameter estimation output
# remote_workdir:	The remote working directory containing the parameter estimation output
function upload_data_to_remote_hosts()
{
  local user=$1
  declare -a hosts=("${!2}")
  local main_folder=$3
  local model=$4
  local modeldir=$5
  local remote_modelsdir=$6
  local datadir=$7
  local remote_datadir=$8
  local workdir=$9
  local remote_workdir=${10}
  
  #printf "$user@${hosts[0]}"
  #print "remote models_dir: ${remote_modelsdir}"
  for host in ${hosts[@]}
  do
    #printf "Uploading data to remote host ${host} ... "
    #printf "\nUploading ${model} ... "
    scp ${modelsdir}/${model} ${user}@${host}:/${remote_modelsdir}/
    # # Send the dataset file
    # printf "\nUploading ${dataset} ... "
    scp ${datadir}/${dataset} ${user}@${host}:/${remote_datadir}/
    # printf "\nUploading job folders ... "
    scp -r ${workdir}/${main_folder} ${user}@${host}:/${remote_workdir}/
  done
}





# Upload model, dataset and jobs folders containing the job configurations to each remote host.
# Input parameters:
# user:			The user name (e.g. npdp2)
# hosts: 		A list of servers that do not share /home (e.g. "iah372.ncl.ac.uk")
# main_folder:		The main folder containing the fits sequences folders
# workdir:		The local working directory containing the parameter estimation output
# remote_workdir:	The remote working directory containing the parameter estimation output
function download_data_to_remote_hosts()
{
  local user=$1
  declare -a hosts=("${!2}")
  local main_folder=$3
  local workdir=$4
  local remote_workdir=$5
  
  for host in ${hosts[@]}
  do
    #printf "${host} "
    rsync -auz --rsh=ssh --stats --progress ${user}@${host}:${remote_workdir}/${main_folder} ${workdir}/   >/dev/null 2>/dev/null
  done
}




# Delete previous repositories created using parallel parameter estimation based on potterswheel and openlava, 
# and create a tarball tar.bz2 of the fits sequence folders.
# Input parameters:
# workdir:			The local working directory containing the parameter estimation outputdir
# model:			The model name
# round:			The current round number of parameter estimation
# main_folder:			The main folder containing the fits sequences folders
# folder_pattern:		The pattern name of the folder to store the n-th fits sequence (e.g. fitseq - WITHOUT 'X', which will be replaced by a number)
# tarball:			The tarball file pattern name
# full_repository:		The name of the full repository
# summary_folder_suffix:	The summary folder suffix (e.g. _all_fits) 
function create_tarball() 
{
  local workdir=$1
  local model=$2
  local round=$3
  local main_folder=$4
  local folder_pattern=$5
  local tarball=$6
  local full_repository=$7
  local summary_folder_suffix=$8

 
  round_folder_name=${workdir}/${model%.*}${summary_folder_suffix}_round${round}
  round_tarball_name=${workdir}/${tarball}${round}.tar.bz2
  now=`date +%y%m%d_%H%M%S`  
  
  # Backup previous folder, if any  
  if [ -d ${round_folder_name} ]; then    
    mv ${round_folder_name} ${round_folder_name}__${now}
  fi
  # Backup previous tarball, if any    
  if [ -f ${round_tarball_name} ]; then
    mv ${round_tarball_name} ${round_tarball_name%%.*}__${now}.tar.bz2
  fi
  
  
  # Add the round number
  mv ${workdir}/${model%.*}${summary_folder_suffix} ${round_folder_name}
  # Check whether the repositories has already been merged.
  if [ -e "${workdir}/${full_repository}" ]; then
    ### Delete the repositories of each fits sequence 
    # to save space (~35MiB each!).
    #printf "Removing repositories ..."
    rm ${workdir}/${folder_pattern}*/${model%.*}_repository.mat
    #printf "DONE\n"
    ### Create an archieve using bzip2 for saving more space.
    #printf "Tar ball creation ..."
    tar cjf ${round_tarball_name} ${workdir}/${main_folder}  >/dev/null 2>/dev/null
    #printf "DONE\n"
    ### Remove fits sequences
    #printf "Removing fits sequences ..."
    rm -rf ${workdir}/${main_folder}
    #printf "DONE\n"
  else 
    echo "${workdir}/${full_repository} does not exist!\n THIS IS A WARNING MESSAGE: \nBefore using this script you must run the matlab script: param_estim__pw_combine_fitseqs.m and then rename the outputdir with outputdir_round${round}  \n\n";
  fi
}






