#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 19:14:32 $





# for computing the pipeline elapsed time 
import time

import os
import sys
import glob
import shutil
import subprocess
import tarfile
# for generating a timestamp
import datetime

from ConfigParser import ConfigParser
from StringIO import StringIO

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + "/sb_pipe/pipelines/sb_param_estim__copasi/")
import param_estim__copasi_parallel
import param_estim__copasi_utils_randomise_start_values
import param_estim__copasi_utils_collect_results
import param_estim__copasi_utils_plot_calibration



"""
This module provides the user with a complete pipeline of scripts comprising the configuration 
and execution of jobs on the cluster, results retrieval and concatenation, parameter estimation 
analyses and finally results storing. This pipeline uses CopasiSE
"""
def main(model_configuration):
  """
  Execute and collect results from parameter estimation using Copasi
  Keyword arguments:
      model_configuration -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """  

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
  # The parameter estimation round 
  round=1
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
    elif line[0] == "round":
      round = line[1]       
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


  nfits = int(nfits)
  local_cpus = int(local_cpus)

  models_dir=project+"/"+models_folder+"/"
  working_dir=project+"/"+working_folder+"/"
  data_dir=project+"/"+data_folder+"/"
  tmp_dir=project+"/"+tmp_folder+"/"

  output_folder=param_estim__copasi_model[:-4]+"_round"+round



  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()

    
    
  print("\n")
  print("#############################################################")
  print("#############################################################")
  print("### Parameter estimation for model "+param_estim__copasi_model)
  print("#############################################################")
  print("#############################################################")
  print("")


      
  print("\n")
  print("#################")
  print("Preparing folders:")
  print("#################")
  print("\n")
  shutil.rmtree(output_folder, ignore_errors=True)
  if not os.path.exists(models_dir):
    os.mkdir(model_dir)
  if not os.path.exists(data_dir):
    os.mkdir(data_dir)    
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)  
  os.makedirs(working_dir+"/"+output_folder)



  print("\n")
  print("######################")
  print("Configure jobs locally:")
  print("######################")
  param_estim__copasi_utils_randomise_start_values.main(models_dir, param_estim__copasi_model, nfits)




  print("\n")
  print("###############################")
  print("Concurrent parameter estimation:")
  print("###############################")
  # for some reason, CopasiSE ignores the "../" for the data file and assumes that the Data folder is inside the Models folder..
  # Let's temporarily copy this folder and then delete it.
  if os.path.exists(models_dir+"/"+data_folder):
    os.rename(models_dir+"/"+data_folder, models_dir+"/"+data_folder+"_{:%Y%m%d%H%M%S}".format(datetime.datetime.now()))
  shutil.copytree(data_dir, models_dir+"/"+data_folder)

  # Perform this task using python-pp (parallel python dependency). 
  # If this computation is performed on a cluster, start this on each node of the cluster. 
  # The list of servers and ports must be updated in the configuration file
  # (NOTE: It requires the installation of python-pp)
  #ppserver -p 65000 -i my-node.abc.ac.uk -s "donald_duck" -w 5 &

  # Perform this task using python-pp (parallel python dependency)
  param_estim__copasi_parallel.main(server_list, port_list, secret, models_dir, param_estim__copasi_model[:-4], nfits, local_cpus)

  # remove the previously copied Data folder
  shutil.rmtree(models_dir+"/"+data_folder, ignore_errors=True) 



  print("\n")
  print("###############")
  print("Collect results:")
  print("###############")
  print("\n")
  # Collect and summarises the parameter estimation results
  param_estim__copasi_utils_collect_results.main(tmp_dir)

  # plot the fitting curve using data from the fit sequence 
  # This requires extraction of a couple of fields from the Copasi output file for parameter estimation.
  #param_estim__copasi_utils_plot_calibration.main(tmp_dir, tmp_dir)



  print("\n")
  print("#####################################")
  print("Store the fits sequences in a tarball:")
  print("#####################################")
  print("\n")
  tmpFiles = os.listdir(tmp_dir)
  for file in tmpFiles:
    shutil.move(tmp_dir+"/"+file, working_dir+"/"+output_folder+"/")
  # Create a gz tarball   
  origWD = os.getcwd() # remember our original working directory
  os.chdir(working_dir) # change folder
  with tarfile.open(output_folder+".tgz", "w:gz") as tar:
    tar.add(output_folder, arcname=os.path.basename(output_folder))
  os.chdir(origWD) # get back to our original working directory
    


  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n")


  if len(glob.glob(working_dir+"/"+output_folder+"/"+param_estim__copasi_model[:-4]+"*.csv")) > 0 and os.path.isfile(working_dir+"/"+output_folder+"/parameter_estimation_collected_results.csv"):
      return True
  else:
      return False
    
    