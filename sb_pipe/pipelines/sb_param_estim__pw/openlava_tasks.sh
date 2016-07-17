#!/bin/bash
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $
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



