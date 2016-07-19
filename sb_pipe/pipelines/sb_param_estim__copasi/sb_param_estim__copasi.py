#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

from ConfigParser import ConfigParser
from StringIO import StringIO

import sb_param_estim__generate_data
import sb_param_estim__analyse_data
import sb_param_estim__generate_report


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


  # Boolean
  generate_data=True
  # Boolean
  analyse_data=True
  # Boolean
  generate_report=True
  # Boolean
  generate_tarball=True  
  # The project dir
  project_dir=""
  # read the copasi model name 
  model="mymodel.cps"
  # The path to Copasi reports
  copasi_reports_path="tmp"  
  # The parallel mechanism to use (pp | sge | lsf).
  cluster="pp"
  # The number of cpus for pp
  pp_cpus=1
  # The parameter estimation round 
  round=1
  # The number of jobs to be executed
  runs=25
  # The percent of best fits to consider
  best_fits_percent=100
  # The number of available data points
  data_point_num=10



  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "generate_data":
      generate_data = {'True': True, 'False': False}.get(line[1], False)     
    if line[0] == "analyse_data":
      analyse_data = {'True': True, 'False': False}.get(line[1], False)     
    if line[0] == "generate_report":
      generate_report = {'True': True, 'False': False}.get(line[1], False)        
    if line[0] == "generate_tarball":
      generate_tarball = {'True': True, 'False': False}.get(line[1], False)        
    if line[0] == "project_dir": 
      project_dir = line[1]
    elif line[0] == "model":
      model = line[1]     
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]
    elif line[0] == "cluster":
      cluster = line[1]      
    elif line[0] == "round":
      round = line[1]       
    elif line[0] == "runs":
      runs = line[1] 
    elif line[0] == "pp_cpus": 
      pp_cpus = line[1]
    elif line[0] == "best_fits_percent": 
      best_fits_percent = line[1]
    elif line[0] == "data_point_num": 
      data_point_num = line[1]
      

  runs = int(runs)
  pp_cpus = int(pp_cpus)
  best_fits_percent = int(best_fits_percent)
  data_point_num = int(data_point_num)

  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The folder containing the data
  data_folder="Data"
  # The folder containing the working results
  working_folder="Working_Folder"
  # The dataset working folder
  sim_raw_data="sim_raw_data"  
  
  models_dir = os.path.join(project_dir,models_folder)
  working_dir = os.path.join(project_dir, working_folder)
  data_dir = os.path.join(project_dir, data_folder)
  tmp_dir = copasi_reports_path

  output_folder = model[:-4]+"_round"+round
  plots_folder = "plots"
  results_dir = os.path.join(working_dir, output_folder)
  plots_dir = os.path.join(results_dir, plots_folder)
  fileout_final_estims = "final_estim_collection.csv"
  fileout_all_estims = "all_estim_collection.csv"
  fileout_approx_ple_stats = "approx_ple_stats.csv"
  fileout_conf_levels = "conf_levels.csv"
  

  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()

    
    
  print("\n")
  print("#############################################################")
  print("### Parameter estimation for model "+model)
  print("#############################################################")
  print("")

  # preprocessing
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)


  if generate_data == True:
    print("\n")
    print("Generate data:")
    print("##############")
    sb_param_estim__generate_data.main(model, 
				       models_dir, 
				       data_dir, 
				       data_folder, 
				       cluster, 
				       pp_cpus, 
				       runs, 
				       results_dir, 
				       sim_raw_data, 
				       tmp_dir)
    

  if analyse_data == True:
    print("\n")
    print("Analyse data:")
    print("#############")
    sb_param_estim__analyse_data.main(os.path.join(results_dir, sim_raw_data), 
				      results_dir, 
				      fileout_final_estims, 
				      fileout_all_estims,
				      fileout_approx_ple_stats,
				      fileout_conf_levels,
				      plots_dir, 
				      best_fits_percent,
				      data_point_num)


  if generate_report == True:
    print("\n")
    print("Report generation:")
    print("##################")
    sb_param_estim__generate_report.main(model[:-4], results_dir, plots_folder)
  


  if generate_tarball == True:
    print("\n")
    print("Store the fits sequences in a tarball:")
    print("#####################################")
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


  if os.path.isfile(os.path.join(results_dir,fileout_final_estims)) and \
     os.path.isfile(os.path.join(results_dir,fileout_all_estims)) and \
     len(glob.glob(os.path.join(results_dir,'*'+model[:-4]+'*.pdf'))) == 1:
      return 0
  return 1
    
    
