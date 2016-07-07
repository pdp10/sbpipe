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
  
  # the project directory
  project_dir=""
  # the model class. This represents a group of models. It can also be the version.
  model_class=""
  # The Copasi model
  model="mymodel.cps"
  # the number of simulation to be run.
  # For deterministic simulation, 1
  # For stochastic simulations, n >=1
  simulate__model_simulations_number=1
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"
  # The data folder containing the dataset
  data_folder="Data"  
  # The folder containing the models
  models_folder="Models"
  # The folder containing the working results
  working_folder="Working_Folder"  
  # The folder containing the temporary computations
  tmp_folder="tmp"
  # The dataset working folder (e.g. dataset)
  dataset_working_folder=""
  # The dataset timecourses dir (e.g. tc)
  tc_dir="tc"
  # The dataset mean timecourses dir (e.g. tc_mean)
  tc_mean_dir="tc_mean"
  # The dataset mean timecourses with experimental data dir (e.g. tc_mean_with_exp)
  tc_mean_with_exp_dir="tc_mean_with_exp_dir"
  # The prefix name of the report of the simulation (e.g. report_simulation__)
  simulate__prefix_results_filename=""
  # The prefix name of the statistics report of the simulation (e.g. stats_simulation__)
  simulate__prefix_stats_filename=""
  # The prefix name of the statistics report of the simulation (e.g. stats_experiments__)
  simulate__prefix_exp_stats_filename=""


  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "project_dir":
      project_dir = line[1] 
    elif line[0] == "model_class":
      model_class = line[1] 
    elif line[0] == "model": 
      model = line[1] 
    elif line[0] == "simulate__model_simulations_number": 
      simulate__model_simulations_number = line[1]
    elif line[0] == "simulate__xaxis_label":
      simulate__xaxis_label = line[1]     
    elif line[0] == "models_folder": 
      models_folder = line[1] 
    elif line[0] == "data_folder":
      data_folder = line[1] 
    elif line[0] == "working_folder": 
      working_folder = line[1] 
    elif line[0] == "tmp_folder": 
      tmp_folder = line[1]       
    elif line[0] == "dataset_working_folder": 
      dataset_working_folder = line[1]       
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


  # Some controls
  if int(simulate__model_simulations_number) < 1: 
    print("ERROR: variable `simulate__model_simulations_number` must be greater than 0. Please, check your configuration file.");
    return False



  models_dir=project_dir+"/"+models_folder+"/"
  results_dir=project_dir+"/"+working_folder+"/"+model_class+"/"
  data_dir=project_dir+"/"+data_folder+"/"
  tmp_dir=project_dir+"/"+tmp_folder



  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()


      
  print("\n")
  print("#############################################################")     
  print("#############################################################")
  print("### Processing model "+ model)
  print("#############################################################")
  print("#############################################################")
  print("")
	

	
  print("\n")
  print("##############################")
  print("Preparing folder "+results_dir)
  print("##############################")
  print("\n")
  # remove the folder the previous results if any
  filesToDelete = glob.glob(results_dir+"/"+dataset_working_folder+"/"+model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(results_dir+"/"+tc_dir+"/"+model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(results_dir+"/"+tc_mean_dir+"/"+model[:-4]+"*")    
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(results_dir+"/"+tc_mean_with_exp_dir+"/"+model[:-4]+"*")    
  for f in filesToDelete:
    os.remove(f)    
  filesToDelete = glob.glob(results_dir+"/"+simulate__prefix_results_filename+model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)    
  filesToDelete = glob.glob(results_dir+"/"+simulate__prefix_stats_filename+model[:-4]+"*")
  for f in filesToDelete:
    os.remove(f)    

  
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)
  if not os.path.exists(results_dir+"/"+dataset_working_folder):  
    os.mkdir(results_dir+"/"+dataset_working_folder)
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
  simulate__run_copasi.main(model, models_dir, results_dir+"/"+dataset_working_folder+"/", tmp_dir+"/", simulate__model_simulations_number)


  print("\n")
  print("######################################")
  print("Generating statistics from simulations:")
  print("######################################")
  print("\n")
  process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_simulate/simulate__plot_error_bars.R", model[:-4], results_dir+"/"+dataset_working_folder+"/", results_dir+"/"+tc_mean_dir+"/", results_dir+"/"+simulate__prefix_stats_filename+model[:-4]+".csv", simulate__xaxis_label])
  process.wait() 


  print("\n")
  print("########################################")
  print("Generating overlapping plots (sim + exp) (SKIP):")
  print("########################################")
  print("\n")
  #process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_simulate/simulate__plot_sim_exp_error_bars.R", model[:-4], results_dir+"/"+tc_mean_dir+"/", results_dir+"/"+tc_mean_exp_dir+"/", results_dir+"/"+tc_mean_with_exp_dir+"/", results_dir+"/"+simulate__prefix_stats_filename+model[:-4]+".csv",  results_dir+"/"+simulate__prefix_exp_stats_filename+model[:-4]+".csv"])
  #process.wait() 


  print("\n")
  print("##################")
  print("Generating reports:")
  print("##################")
  print("\n")
  simulate__gen_report.main(model[:-4], results_dir+"/", tc_mean_dir, simulate__prefix_results_filename)


  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n")


  if os.path.isfile(results_dir+"/"+simulate__prefix_results_filename+model[:-4]+".pdf") and len(glob.glob(results_dir+"/"+tc_mean_dir+"/"+model[:-4]+"*.png")) > 0:
       return True
  else:
       return False

