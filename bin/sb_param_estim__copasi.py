#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
# $Date: 2016-06-23 19:14:32 $

# This scripts provides the user with a complete pipeline of scripts comprising the configuration 
# and execution of jobs on the cluster, results retrieval and concatenation, parameter estimation 
# analyses and finally results storing. This pipeline uses CopasiSE



# for computing the pipeline elapsed time 
import time

import os
import sys
import shutil
import subprocess

from ConfigParser import ConfigParser
from StringIO import StringIO

SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/pipelines/sb_param_estim__copasi/")



def main(args):


  # Input parameters
  # The file containing the model configuration, usually in working_folder (e.g. model.conf)
  model_configuration = args[1]
  # The current round number
  round = args[2]

  print("\nReading file " + model_configuration + " : \n")
  # import the model configuration data (project, model-name, association-pattern)
  parser = ConfigParser()
  with open(model_configuration) as stream:
    stream = StringIO("[top]\n" + stream.read())  # This line does the trick.
    parser.readfp(stream)  
    
  lines=parser.items('top')


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



  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "user":
      user = line[1] 
    elif line[0] == "server_list":
      server_list = line[1] 
    elif line[0] == "port_list": 
      port_list = line[1] 
    elif line[0] == "secret": 
      secret = line[1]
    elif line[0] == "project": 
      project = line[1] 
    elif line[0] == "nfits":
      nfits = line[1] 
    elif line[0] == "local_cpus": 
      local_cpus = line[1]
    elif line[0] == "param_estim__copasi_model":
      param_estim__copasi_model = line[1]     
    elif line[0] == "models_folder": 
      models_folder = line[1] 
    elif line[0] == "data_folder":
      data_folder = line[1]
    elif line[0] == "working_folder": 
      working_folder = line[1] 
    elif line[0] == "tmp_folder": 
      tmp_folder = line[1] 
    elif line[0] == "remote_models_folder": 
      remote_models_folder = line[1] 
    elif line[0] == "remote_data_folder":
      remote_data_folder = line[1]
    elif line[0] == "remote_working_folder": 
      remote_working_folder = line[1] 
    elif line[0] == "remote_tmp_folder": 
      remote_tmp_folder = line[1]



  models_dir=project+"/"+models_folder+"/"
  working_dir=project+"/"+working_folder+"/"
  data_dir=project+"/"+data_folder+"/"
  tmp_dir=project+"/"+tmp_folder+"/"

  output_folder=param_estim__copasi_model[:-4]+"_round"+round



  print("\n\n\n<START PIPELINE>\n\n\n")
  # Get the pipeline start time
  start = time.clock()

    
    
  print("\n\n\n")
  print("##############################################################\n")
  print("##############################################################\n")
  print("### Parameter estimation for model "+param_estim__copasi_model+" \n")
  print("##############################################################\n")
  print("##############################################################\n")
  print("\n\n")


      
  print("\n\n\n")
  print("##################\n")
  print("Preparing folders:\n")
  print("##################\n")
  print("\n")
  
  
  

# remove the folder containing the parameter estimation for this round
rm -rf ${working_dir}/${output_folder}
mkdir -p ${model_dir} ${data_dir} ${tmp_dir} ${working_dir} ${working_dir}/${output_folder}


print("\n\n\n")
print("#######################\n")
print("Configure jobs locally:\n")
print("#######################\n")
python ${SB_PIPE_LIB}/pipelines//sb_param_estim__copasi/param_estim__copasi_utils_randomise_start_values.py ${models_dir} ${param_estim__copasi_model} ${nfits}




print("\n\n\n")
print("################################\n")
print("Concurrent parameter estimation:\n")
print("################################\n")
# for some reason, CopasiSE ignores the "../" for the data file and assumes that the Data folder is inside the Models folder..
# Let's temporarily copy this folder and then delete it. 
cp -R ${data_dir} ${models_dir}/

# Perform this task using python-pp (parallel python dependency). 
# If this computation is performed on a cluster, start this on each node of the cluster. 
# The list of servers and ports must be updated in the configuration file
# (NOTE: It requires the installation of python-pp)
#ppserver -p 65000 -i my-node.abc.ac.uk -s "donald_duck" -w 5 &

# Perform this task using python-pp (parallel python dependency)
python ${SB_PIPE_LIB}/pipelines//sb_param_estim__copasi/param_estim__copasi_parallel.py ${server_list} ${port_list} ${secret} ${models_dir} ${param_estim__copasi_model%.*} ${nfits} ${local_cpus}

# Perform this task directly (no parallel python dependency).
#bash ${SB_PIPE_LIB}/pipelines//sb_param_estim__copasi/run_generic__copasi_concur_local.sh ${models_dir} ${param_estim__copasi_model%.*} 1 ${nfits} ${local_cpus}

# remove the previously copied Data folder
rm -rf ${models_dir}/${data_folder}




print("\n\n\n")
print("################\n")
print("Collect results:\n")
print("################\n")
print("\n")
# Collect and summarises the parameter estimation results
python ${SB_PIPE_LIB}/pipelines//sb_param_estim__copasi/param_estim__copasi_utils_collect_results.py ${tmp_dir}

# plot the fitting curve using data from the fit sequence 
# This requires extraction of a couple of fields from the Copasi output file for parameter estimation.
#python ${SB_PIPE_LIB}/pipelines//sb_param_estim__copasi/param_estim__copasi_utils_plot_calibration.py ${tmp_dir} ${tmp_dir}




print("\n\n\n")
print("######################################\n")
print("Store the fits sequences in a tarball:\n")
print("######################################\n")
print("\n")
mv ${tmp_dir}/*.csv ${working_dir}/${output_folder}
cd ${working_dir}
tar cvzf ${output_folder}.tgz ${output_folder}
cd -



  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n\n\n")


