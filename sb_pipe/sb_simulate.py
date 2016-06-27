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
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 16:14:32 $




# for computing the pipeline elapsed time 
import time

import os
import sys
import glob
import shutil
import subprocess

from ConfigParser import ConfigParser
from StringIO import StringIO

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + "/sb_pipe/pipelines/sb_simulate/")
import simulate__run_copasi
import simulate__gen_report




"""
This module provides the user with a complete pipeline of scripts for running 
a model simulation using copasi
"""

def main(model_configuration):
  """
  Execute and collect results for a model simulation using Copasi
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
  
  # read the project name
  project=""
  # read the main model name (e.g. mtor_mito_ros_model_v27_pw3.m)
  model=""
  # Copasi models list (1 model per species to perturb) (e.g mtor_mito_ros_model_v27_copasi_scan_mTORC1.cps ...)
  simulate__copasi_model=""
  # the number of simulation to be run.
  # minimum 2 (required for plotCI, otherwise, ci95 and sderr are NA -> error in ylim)
  # For stochastic simulations, run 500
  # For testing, run 5
  simulate__model_simulations_number=2
  # The inteval size of each simulation step (e.g. 0.01)
  # This is required for plotting
  simulate__interval_size=0.1
  # The starting time point of the simulation (e.g. 0)
  # This is required for plotting
  simulate__start=0
  # The ending time point of the simulation (e.g. 10)
  # This is required for plotting
  simulate__end=10
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"
  # The folder containing the models
  models_folder=""
  # The folder containing the models simulations
  simulations_folder=""
  # The folder containing the temporary computations
  tmp_folder=""
  # The dataset simulation dir (e.g. dataset)
  dataset_simulation_dir=""
  # The dataset short simulation dir (e.g. dataset_short)
  dataset_short_simulation_dir=""
  # The dataset timecourses dir (e.g. tc)
  tc_dir=""
  # The dataset mean timecourses dir (e.g. tc_mean)
  tc_mean_dir=""
  # The dataset mean timecourses with experimental data dir (e.g. tc_mean_with_exp)
  tc_mean_with_exp_dir=""
  # The prefix name of the report of the simulation (e.g. report_simulation__)
  simulate__prefix_results_filename=""
  # The prefix name of the statistics report of the simulation (e.g. stats_simulation__)
  simulate__prefix_stats_filename=""
  # The prefix name of the statistics report of the simulation (e.g. stats_experiments__)
  simulate__prefix_exp_stats_filename=""


  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "project":
      project = line[1] 
    elif line[0] == "model":
      model = line[1] 
    elif line[0] == "simulate__copasi_model": 
      simulate__copasi_model = line[1] 
    elif line[0] == "simulate__model_simulations_number": 
      simulate__model_simulations_number = line[1]
    elif line[0] == "simulate__start": 
      simulate__start = line[1] 
    elif line[0] == "simulate__end":
      simulate__end = line[1] 
    elif line[0] == "simulate__interval_size": 
      simulate__interval_size = line[1]    
    elif line[0] == "simulate__xaxis_label":
      simulate__xaxis_label = line[1]     
    elif line[0] == "models_folder": 
      models_folder = line[1] 
    elif line[0] == "data_folder":
      data_folder = line[1] 
    elif line[0] == "simulations_folder": 
      simulations_folder = line[1] 
    elif line[0] == "tmp_folder": 
      tmp_folder = line[1]       
    elif line[0] == "dataset_simulation_dir": 
      dataset_simulation_dir = line[1]       
    elif line[0] == "tc_dir": 
      tc_dir = line[1]       
    elif line[0] == "tc_mean_dir": 
      tc_mean_dir = line[1] 
    elif line[0] == "tc_mean_with_exp_dir": 
      tc_mean_with_exp_dir = line[1]   
    elif line[0] == "simulate__prefix_results_filename": 
      simulate__prefix_results_filename = line[1] 
    elif line[0] == "simulate__prefix_stats_filename": 
      simulate__prefix_stats_filename = line[1]       
    elif line[0] == "simulate__prefix_exp_stats_filename": 
      simulate__prefix_exp_stats_filename = line[1] 
    
    

  if int(simulate__start) >= int(simulate__end): 
    print("\n ERROR: simulate__start must be less than simulate__end ")
    return



  models_dir=project+"/"+models_folder+"/"
  results_dir=project+"/"+simulations_folder+"/"+model+"/"
  data_dir=project+"/"+data_folder+"/"
  tmp_dir=project+"/"+tmp_folder




  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()


      
  print("\n")
  print("#############################################################")     
  print("#############################################################")
  print("### Processing model "+ simulate__copasi_model)
  print("#############################################################")
  print("#############################################################")
  print("")
	

	
  print("\n")
  print("##############################")
  print("Preparing folder "+results_dir)
  print("##############################")
  print("\n")
  # remove the folder the previous results if any
  filesToDelete = glob.glob(results_dir+"/"+dataset_simulation_dir+"/"+simulate__copasi_model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(results_dir+"/"+tc_dir+"/"+simulate__copasi_model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(results_dir+"/"+tc_mean_dir+"/"+simulate__copasi_model[:-4]+"*")    
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(results_dir+"/"+tc_mean_with_exp_dir+"/"+simulate__copasi_model[:-4]+"*")    
  for f in filesToDelete:
    os.remove(f)    
  filesToDelete = glob.glob(results_dir+"/"+simulate__prefix_results_filename+simulate__copasi_model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)    
  filesToDelete = glob.glob(results_dir+"/"+simulate__prefix_stats_filename+simulate__copasi_model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)    

  
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)
  if not os.path.exists(results_dir+"/"+dataset_simulation_dir):  
    os.mkdir(results_dir+"/"+dataset_simulation_dir)
  if not os.path.exists(results_dir+"/"+tc_dir):  
    os.mkdir(results_dir+"/"+tc_dir) 
  if not os.path.exists(results_dir+"/"+tc_mean_dir):  
    os.mkdir(results_dir+"/"+tc_mean_dir)
  if not os.path.exists(results_dir+"/"+tc_mean_with_exp_dir):  
    os.mkdir(results_dir+"/"+tc_mean_with_exp_dir)  
 
 

  print("\n")
  print("#####################")
  print("Executing simulations:")
  print("#####################")
  print("\n")
  simulate__run_copasi.main(simulate__copasi_model, models_dir, results_dir+"/"+dataset_simulation_dir+"/", tmp_dir+"/", simulate__model_simulations_number)


  print("\n")
  print("######################################")
  print("Generating statistics from simulations:")
  print("######################################")
  print("\n")
  process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_simulate/simulate__plot_error_bars.R", simulate__copasi_model[:-4], results_dir+"/"+dataset_simulation_dir+"/", results_dir+"/"+tc_mean_dir+"/", results_dir+"/"+simulate__prefix_stats_filename+simulate__copasi_model[:-4]+".csv", simulate__start, simulate__end, simulate__interval_size, simulate__xaxis_label])
  process.wait() 


  print("\n")
  print("######################################")
  print("Generating statistics from experiments (SKIP):")
  print("######################################")
  print("\n")
  #process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_simulate/simulate__plot_exp_error_bars.R", data_dir+"/"+dataset_exp+"/", results_dir+"/"+tc_mean_exp}+"/", results_dir+"/"+simulate__prefix_exp_stats_filename+simulate__copasi_model[:-4]+".csv"])
  #process.wait() 


  print("\n")
  print("########################################")
  print("Generating overlapping plots (sim + exp) (SKIP):")
  print("########################################")
  print("\n")
  #process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_simulate/simulate__plot_sim_exp_error_bars.R", simulate__copasi_model[:-4], results_dir+"/"+tc_mean_dir+"/", results_dir+"/"+tc_mean_exp_dir+"/", results_dir+"/"+tc_mean_with_exp_dir+"/", results_dir+"/"+simulate__prefix_stats_filename+simulate__copasi_model[:-4]+".csv",  results_dir+"/"+simulate__prefix_exp_stats_filename+simulate__copasi_model[:-4]+".csv"])
  #process.wait() 


  print("\n")
  print("##################")
  print("Generating reports:")
  print("##################")
  print("\n")
  simulate__gen_report.main(simulate__copasi_model[:-4], results_dir+"/", tc_mean_dir, simulate__prefix_results_filename)


  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n")

