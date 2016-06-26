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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 21:43:32 $

# This scripts provides the user with a complete pipeline of scripts for computing 
# a single parameter scan using copasi.



# for computing the pipeline elapsed time 
import time


import glob
import os
import os.path
import sys
import shutil
import subprocess

from ConfigParser import ConfigParser
from StringIO import StringIO

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + "/sb_pipe/pipelines/sb_param_scan__single_perturb/")
import param_scan__single_perturb_run_copasi
import param_scan__single_perturb_gen_report


# Input parameters
# The file containing the model configuration, usually in working_folder (e.g. model.conf)
def main(model_configuration):


  print("\nReading file " + model_configuration + " : \n")
  # import the model configuration data (project, model-name, association-pattern)
  parser = ConfigParser()
  with open(model_configuration) as stream:
    stream = StringIO("[top]\n" + stream.read())  # This line does the trick.
    parser.readfp(stream)  
    
  lines=parser.items('top')


  # NOTE: The idea is that 
  # (1) the parameters of model m are estimated 
  # (2) model m can be perturbed on n species (in copasi, it is better 1 species per model, since it must be configured in the .cps file)


  # read the project name
  project=""
  # read the main model name (e.g. mtor_mito_ros_model_v27_pw3.m
  model=""
  # Copasi models list (1 model per species to perturb) (e.g mtor_mito_ros_model_v27_copasi_scan_mTORC1.cps ...)
  param_scan__single_perturb_copasi_models_list=[] # a list separated by ','
  # list of species to knock-down (name of the species as in copasi) (e.g. mTORC1)
  param_scan__single_perturb_species_list=[]   # a list separated by ','
  # if Y then, plot only kd (blue), otherwise plot kd and overexpression
  param_scan__single_perturb_knock_down_only=""
  # The folder containing the models
  models_folder=""
  # The folder containing the models simulations
  simulations_folder=""
  # The folder containing the temporary computations
  tmp_folder=""
  # The starting time point of the simulation (e.g. 0)
  # This is required for plotting
  simulate__start=0
  # The ending time point of the simulation (e.g. 120)
  # This is required for plotting
  simulate__end=10
  # The size of an interval for the simulation
  simulate__interval_size=0.1
  # The number of intervals for one simulation
  simulate__intervals=100  
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"
  # The number of parameter scan intervals
  param_scan__single_perturb_intervals=10
  # The legend name for the single perturbation
  param_scan__single_perturb_legend=""
  # Single perturbation minimum inhibition level
  param_scan__single_perturb_min_inhibition_level=0
  # Single perturbation maximum overexpression level
  param_scan__single_perturb_max_overexpression_level=250
  # The prefix for the results filename (e.g. "report_single_perturb_")
  param_scan__single_perturb_prefix_results_filename=""
  # The number of single pertubation simulations (e.g. 1 for deterministic simulations, 500 for stochastic simulations)
  param_scan__single_perturb_simulations_number=1
  # The perturbation is performed on percent levels (true) or through a modelled inhibitor/expressor (false)
  param_scan__single_perturb_perturbation_in_percent_levels="true"
  # The number of levels of inhibition/over-expression
  param_scan__single_perturb_levels_number=10
  # The name of the folder containing the computed dataset of the parameter scanning (e.g. dataset_parameter_scan)
  dataset_parameter_scan_dir=""
  # The name of the folder containing the generated plots of the parameter scanning (e.g. tc_parameter_scan)
  tc_parameter_scan_dir=""


  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "project":
      project = line[1] 
    elif line[0] == "model":
      model = line[1]       
    elif line[0] == "param_scan__single_perturb_copasi_models_list": 
      param_scan__single_perturb_copasi_models_list = line[1] 
    elif line[0] == "param_scan__single_perturb_species_list": 
      param_scan__single_perturb_species_list = line[1]
    elif line[0] == "param_scan__single_perturb_knock_down_only": 
      param_scan__single_perturb_knock_down_only = line[1] 
    elif line[0] == "models_folder": 
      models_folder = line[1] 
    elif line[0] == "simulations_folder": 
      simulations_folder = line[1] 
    elif line[0] == "tmp_folder": 
      tmp_folder = line[1]      
    elif line[0] == "simulate__start": 
      simulate__start = line[1]       
    elif line[0] == "simulate__end": 
      simulate__end = line[1]       
    elif line[0] == "simulate__interval_size": 
      simulate__interval_size = line[1]
    elif line[0] == "simulate__intervals": 
      simulate__intervals = line[1]       
    elif line[0] == "simulate__xaxis_label": 
      simulate__xaxis_label = line[1]      
    elif line[0] == "param_scan__single_perturb_intervals": 
      param_scan__single_perturb_intervals = line[1]
    elif line[0] == "param_scan__single_perturb_legend": 
      param_scan__single_perturb_legend = line[1] 
    elif line[0] == "param_scan__single_perturb_min_inhibition_level": 
      param_scan__single_perturb_min_inhibition_level = line[1]       
    elif line[0] == "param_scan__single_perturb_max_overexpression_level": 
      param_scan__single_perturb_max_overexpression_level = line[1] 
    elif line[0] == "param_scan__single_perturb_prefix_results_filename": 
      param_scan__single_perturb_prefix_results_filename = line[1]       
    elif line[0] == "param_scan__single_perturb_simulations_number": 
      param_scan__single_perturb_simulations_number = line[1] 
    elif line[0] == "param_scan__single_perturb_perturbation_in_percent_levels": 
      param_scan__single_perturb_perturbation_in_percent_levels = line[1]       
    elif line[0] == "param_scan__single_perturb_levels_number": 
      param_scan__single_perturb_levels_number = line[1] 
    elif line[0] == "dataset_parameter_scan_dir": 
      dataset_parameter_scan_dir = line[1]       
    elif line[0] == "tc_parameter_scan_dir": 
      tc_parameter_scan_dir = line[1]
    elif line[0] == "param_scan__single_perturb_copasi_models_list":
      param_scan__single_perturb_copasi_models_list = line[1]
    elif line[0] == "param_scan__single_perturb_species_list":
      param_scan__single_perturb_species_list = line[1]


  param_scan__single_perturb_copasi_models_list = param_scan__single_perturb_copasi_models_list.split(',')
  param_scan__single_perturb_species_list = param_scan__single_perturb_species_list.split(',')


  # some control
  if int(simulate__start) >= int(simulate__end): 
    print("\n ERROR: simulate__start must be less than simulate__end \n\n")
    return

  if len(param_scan__single_perturb_copasi_models_list) != len(param_scan__single_perturb_species_list): 
    print("\n ERROR: One model MUST BE defined for each species to perturb! "+
	  str(len(param_scan__single_perturb_copasi_models_list))+"!="+
	  str(len(param_scan__single_perturb_species_list))+"\n\n")
    return

  if int(param_scan__single_perturb_min_inhibition_level) < 0: 
    print("\n ERROR: param_scan__single_perturb_min_inhibition_level MUST BE non negative \n\n")
    return
  
  if int(param_scan__single_perturb_max_overexpression_level) < 100: 
    print("\n ERROR: param_scan__single_perturb_max_overexpression_level MUST BE greater than 100 \n\n")
    return  


  models_dir=project+"/"+models_folder+"/"
  results_dir=project+"/"+simulations_folder+"/"+model+"/"
  tmp_dir=project+"/"+tmp_folder




  print("\n\n\n<START PIPELINE>\n\n\n")
  # Get the pipeline start time
  start = time.clock()


  for i in range(0, len(param_scan__single_perturb_species_list)):
      
    sp_species=param_scan__single_perturb_species_list[i]
    sp_model=param_scan__single_perturb_copasi_models_list[i]
               
    if not os.path.isfile(models_dir+"/"+sp_model):
      print(models_dir+"/"+sp_model + " does not exist.") 
      return
      
    
    print("\n\n\n")
    print("##############################################################\n")     
    print("##############################################################\n")
    print("### Processing model "+ sp_model+"\n")
    print("##############################################################\n")
    print("##############################################################\n")
    print("\n\n")    


    print("\n\n\n")
    print("###############################\n")
    print("Preparing folder "+results_dir +":\n")
    print("###############################\n")
    print("\n")
    filesToDelete = glob.glob(results_dir+"/"+dataset_parameter_scan_dir+"/"+sp_model[:-4]+"*")
    for f in filesToDelete:
      os.remove(f)
    filesToDelete = glob.glob(results_dir+"/"+tc_parameter_scan_dir+"/"+sp_model[:-4]+"*")
    for f in filesToDelete:
      os.remove(f)
    filesToDelete = glob.glob(results_dir+"/"+tc_parameter_scan_dir+"/"+param_scan__single_perturb_legend+"_"+sp_species+"*")
    for f in filesToDelete:
      os.remove(f)
    filesToDelete = glob.glob(results_dir+"/"+param_scan__single_perturb_prefix_results_filename+"*"+sp_model[:-4]+"*")
    for f in filesToDelete:
      os.remove(f)    
   
    if not os.path.exists(tmp_dir):
      os.mkdir(tmp_dir)
    if not os.path.exists(results_dir):
      os.makedirs(results_dir)
    if not os.path.exists(results_dir+"/"+dataset_parameter_scan_dir):
      os.mkdir(results_dir+"/"+dataset_parameter_scan_dir)
    if not os.path.exists(results_dir+"/"+tc_parameter_scan_dir):
      os.mkdir(results_dir+"/"+tc_parameter_scan_dir) 



    print("\n\n\n")
    print("######################\n")
    print("Executing simulations:\n")
    print("######################\n")
    print("\n")
    param_scan__single_perturb_run_copasi.main(sp_model, 
					       sp_species, 
					       param_scan__single_perturb_simulations_number, 
					       simulate__intervals,
					       param_scan__single_perturb_intervals,
					       models_dir, 
					       results_dir+"/"+dataset_parameter_scan_dir, 
					       tmp_dir)



    # Comment if you want to have the knockdown. If so, you must edit plot colours in param_scan__single_perturb_plot.R 
    if param_scan__single_perturb_perturbation_in_percent_levels == "true":
      print("\n\n\n")
      print("########################\n")
      print("Removing knock out data:\n")
      print("########################\n") 
      print("\n")
      map(os.remove, glob.glob(results_dir+"/"+dataset_parameter_scan_dir+"/"+sp_model[:-4]+"*__level_0.csv"))    
    
    
    
    print("\n\n\n")
    print("#################\n")
    print("Generating plots:\n")
    print("#################\n")
    print("\n")
    process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_plot.R", 
				sp_model[:-4], sp_species, param_scan__single_perturb_knock_down_only, results_dir, dataset_parameter_scan_dir, 
				tc_parameter_scan_dir, simulate__start, simulate__end, simulate__interval_size, simulate__xaxis_label, 
				param_scan__single_perturb_simulations_number, param_scan__single_perturb_perturbation_in_percent_levels])
    process.wait() 
    # Prepare the legend
    if param_scan__single_perturb_knock_down_only == "true":
      process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_make_legend.R",       
	    results_dir+"/"+tc_parameter_scan_dir+"/", 
	    param_scan__single_perturb_legend, 
	    param_scan__single_perturb_min_inhibition_level, 
	    "100", 
	    param_scan__single_perturb_knock_down_only, 
	    param_scan__single_perturb_perturbation_in_percent_levels, 
	    str(param_scan__single_perturb_levels_number)])
    else:
      # TODO TEST THIS
      process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_plot.R", 
	    results_dir+"/"+tc_parameter_scan_dir+"/", 
	    param_scan__single_perturb_legend, 
	    param_scan__single_perturb_min_inhibition_level, 
	    param_scan__single_perturb_max_overexpression_level, 
	    param_scan__single_perturb_knock_down_only, 
	    param_scan__single_perturb_perturbation_in_percent_levels,
	    str(param_scan__single_perturb_levels_number)])
    process.wait() 
    
    
    
    print("\n\n\n")
    print("###################\n")
    print("Generating reports:\n")
    print("###################\n")
    print("\n")
    param_scan__single_perturb_gen_report.main(sp_model[:-4], sp_species, results_dir+"/", tc_parameter_scan_dir, 
					       param_scan__single_perturb_prefix_results_filename, param_scan__single_perturb_legend)
    

    # Print the pipeline elapsed time
    end = time.clock()
    print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
    print("\n<END PIPELINE>\n\n\n")

