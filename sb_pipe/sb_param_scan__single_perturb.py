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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 21:43:32 $




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
sys.path.append(os.path.join(SB_PIPE, 'sb_pipe','pipelines','sb_param_scan__single_perturb'))
import param_scan__single_perturb_run_copasi
import param_scan__single_perturb_gen_report


"""
This module provides the user with a complete pipeline of scripts for computing 
a single parameter scan using copasi.
"""

def main(model_configuration):
  """
  Execute and collect results from a parameter scan using Copasi
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


  # NOTE: The idea is that 
  # (1) the parameters of model m are estimated 
  # (2) model m can be perturbed on n species (in copasi, it is better 1 species per model, since it must be configured in the .cps file)


  # the project directory
  project_dir=".."
  # Copasi model (e.g mtor_model_scan_mTORC1.cps ...)
  model=""
  # The model species to scan (e.g. mTORC1)
  scanned_species=""  
  # The path to Copasi reports
  copasi_reports_path="tmp"  
  # if Y then, plot only kd (blue), otherwise plot kd and overexpression
  param_scan__single_perturb_knock_down_only=""
  # The number of intervals for one simulation
  simulate__intervals=100  
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"
  # The number of single pertubation simulations (e.g. 1 for deterministic simulations, n for stochastic simulations)
  param_scan__single_perturb_simulations_number=1
  # The perturbation is performed on percent levels (true) or through a modelled inhibitor/expressor (false)
  param_scan__single_perturb_perturbation_in_percent_levels="true"  
  # The number of levels of inhibition/over-expression
  levels_number=10  
  # Single perturbation minimum inhibition level
  min_level=0
  # Single perturbation maximum overexpression level
  max_level=250




  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "project_dir":
      project_dir = line[1]   
    elif line[0] == "model": 
      model = line[1] 
    elif line[0] == "scanned_species": 
      scanned_species = line[1]
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]            
    elif line[0] == "param_scan__single_perturb_knock_down_only": 
      param_scan__single_perturb_knock_down_only = line[1] 
    elif line[0] == "simulate__intervals": 
      simulate__intervals = line[1]       
    elif line[0] == "simulate__xaxis_label": 
      simulate__xaxis_label = line[1]
    elif line[0] == "param_scan__single_perturb_simulations_number": 
      param_scan__single_perturb_simulations_number = line[1] 
    elif line[0] == "param_scan__single_perturb_perturbation_in_percent_levels": 
      param_scan__single_perturb_perturbation_in_percent_levels = line[1]      
    elif line[0] == "min_level": 
      min_level = line[1]       
    elif line[0] == "max_level": 
      max_level = line[1]
    elif line[0] == "levels_number": 
      levels_number = line[1]          



  # some control
  if int(min_level) < 0: 
    print("\n ERROR: min_level MUST BE non negative ")
    return
  
  if int(max_level) < 100: 
    print("\n ERROR: max_level MUST BE greater than 100 ")
    return  


  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The folder containing the results
  working_folder="Working_Folder"
  # The name of the folder containing the computed dataset of the parameter scanning
  dataset_parameter_scan_dir="param_scan_data"
  # The name of the folder containing the generated plots of the parameter scanning
  tc_parameter_scan_dir="tc_param_scan"  

  models_dir = os.path.join(project_dir, models_folder)
  results_dir = os.path.join(project_dir, working_folder, model[:-4])
  tmp_dir = os.path.join(copasi_reports_path)




  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()

      
  if not os.path.isfile(os.path.join(models_dir,model)):
    print(os.path.join(models_dir, model) + " does not exist.") 
    return
    
  
  print("\n")
  print("#############################################################")     
  print("#############################################################")
  print("### Processing model " + model)
  print("#############################################################")
  print("#############################################################")
  print("")    


  print("\n")
  print("##############################")
  print("Preparing folder " + results_dir +":")
  print("##############################")
  print("\n")
  filesToDelete = glob.glob(os.path.join(results_dir,dataset_parameter_scan_dir,model[:-4]+"*"))
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(os.path.join(results_dir,tc_parameter_scan_dir,model[:-4]+"*"))
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(os.path.join(results_dir,"*"+model[:-4]+"*"))
  for f in filesToDelete:
    os.remove(f)    
  
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)
  if not os.path.exists(os.path.join(results_dir, dataset_parameter_scan_dir)):
    os.mkdir(os.path.join(results_dir, dataset_parameter_scan_dir))
  if not os.path.exists(os.path.join(results_dir, tc_parameter_scan_dir)):
    os.mkdir(os.path.join(results_dir, tc_parameter_scan_dir)) 



  print("\n")
  print("#####################")
  print("Executing simulations:")
  print("#####################")
  print("\n")
  param_scan__single_perturb_run_copasi.main(model, 
					      scanned_species, 
					      param_scan__single_perturb_simulations_number, 
					      simulate__intervals,
					      levels_number,
					      models_dir, 
					      os.path.join(results_dir, dataset_parameter_scan_dir), 
					      tmp_dir)
  
  
  print("\n")
  print("################")
  print("Generating plots:")
  print("################")
  print("\n")
  process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE, 'sb_pipe','pipelines','sb_param_scan__single_perturb','param_scan__single_perturb_plot.R'), 
			      model[:-4], scanned_species, param_scan__single_perturb_knock_down_only, results_dir, dataset_parameter_scan_dir, tc_parameter_scan_dir, simulate__xaxis_label, 
			      param_scan__single_perturb_simulations_number, param_scan__single_perturb_perturbation_in_percent_levels, 
			      str(min_level), str(max_level), str(levels_number)])    
  process.wait()
  
  
  
  print("\n")
  print("##################")
  print("Generating reports:")
  print("##################")
  print("\n")
  param_scan__single_perturb_gen_report.main(model[:-4], scanned_species, results_dir, tc_parameter_scan_dir)
  


  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n")


  if len(glob.glob(os.path.join(results_dir, "*"+model[:-4]+"*.pdf"))) == 1 and len(glob.glob(os.path.join(results_dir, tc_parameter_scan_dir, model[:-4]+"*.png"))) > 0:
    return 0
  return 1
     