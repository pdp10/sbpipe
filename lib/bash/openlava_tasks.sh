#!/bin/bash

# Author:     Piero Dalle Pezze
# Email:      piero.dallepezze@ncl.ac.uk
# Creation:   20/04/2013
# Modified:   09/05/2013
#
#
# Execute tasks on an openlava cluster



# Creates the folders containing the fits sequences
# Input parameters:
# workdir:		The local working directory
# njobs:		The number of jobs to be executed (e.g. 40)
# folder_pattern:	The pattern name of the folder to store the n-th fits sequence (e.g. fitseq)
function create_job_folders()
{
  local workdir=$1
  local njobs=$2
  local folder_pattern=$3
  
  for (( i=1; ${i} <= ${njobs}; i++ ))
  do 
    mkdir -p ${workdir}/${folder_pattern}${i}
  done
}






# Starts a sequence of jobs located in a folder pattern name inclusive with a full path
# Input parameters:
# full_folder_pattern:	The folder pattern name inclusive with a full path
# job_name:		The job name
# njobs:		The number of jobs to be executed (e.g. 40)    
function start_jobs()
{
  local full_folder_pattern=$1
  local job_name=$2
  local njobs=$3
  
  for (( i=1; ${i} <= ${njobs}; i++ ))  
  do
      cd ${full_folder_pattern}${i}/
      # Invoke bsub. Command prints are suppressed, since we are inside a function (otherwise, they return as function output).
      # comment for testing
      bsub < ${job_name%.*}${i}.job  >/dev/null 2>/dev/null
  done
}



