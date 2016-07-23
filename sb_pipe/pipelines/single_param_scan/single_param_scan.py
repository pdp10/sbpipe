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
import logging
logger = logging.getLogger('sbpipe')

from ConfigParser import ConfigParser
from StringIO import StringIO

import single_param_scan__generate_data
import single_param_scan__analyse_data
import single_param_scan__generate_report


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

  logger.info("Reading file " + model_configuration + " : \n")
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
  # the project directory
  project_dir=".."
  # Copasi model (e.g mtor_model_scan_mTORC1.cps ...)
  model=""
  # The model species to scan (e.g. mTORC1)
  scanned_species=""  
  # The path to Copasi reports
  copasi_reports_path="tmp"  
  # The number of intervals for one simulation
  simulate__intervals=100  
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"
  # The number of simulations (e.g. 1 for deterministic simulations, n for stochastic simulations)
  single_param_scan_simulations_number=1
  # The scanning is performed on percent levels (true) or through a modelled inhibitor/expressor (false)
  single_param_scan_percent_levels=False
  # if True then, plot only kd (blue), otherwise plot kd and overexpression
  single_param_scan_knock_down_only=True
  # The number of levels of inhibition/over-expression
  levels_number=10  
  # minimum level
  min_level=0
  # maximum level
  max_level=250
  # True if lines should have the same colour, no linetype, no legend. 
  # Useful for scanning from a confidence interval
  # If this is true, it overrides:
  # - single_param_scan_percent_levels and 
  # - single_param_scan_knock_down_only
  homogeneous_lines=False


  # Initialises the variables
  for line in lines:
    logger.info(line)
    if line[0] == "generate_data":
      generate_data = {'True': True, 'False': False}.get(line[1], False)     
    if line[0] == "analyse_data":
      analyse_data = {'True': True, 'False': False}.get(line[1], False)     
    if line[0] == "generate_report":
      generate_report = {'True': True, 'False': False}.get(line[1], False)        
    if line[0] == "project_dir":
      project_dir = line[1]   
    elif line[0] == "model": 
      model = line[1] 
    elif line[0] == "scanned_species": 
      scanned_species = line[1]
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]
    elif line[0] == "simulate__intervals": 
      simulate__intervals = line[1]       
    elif line[0] == "simulate__xaxis_label": 
      simulate__xaxis_label = line[1]
    elif line[0] == "single_param_scan_simulations_number": 
      single_param_scan_simulations_number = line[1] 
    elif line[0] == "single_param_scan_percent_levels": 
      single_param_scan_percent_levels = {'True': True, 'False': False}.get(line[1], False)
    elif line[0] == "single_param_scan_knock_down_only": 
      single_param_scan_knock_down_only = {'True': True, 'False': False}.get(line[1], False)      
    elif line[0] == "min_level": 
      min_level = line[1]       
    elif line[0] == "max_level": 
      max_level = line[1]
    elif line[0] == "levels_number": 
      levels_number = line[1]          
    elif line[0] == "homogeneous_lines": 
      homogeneous_lines = {'True': True, 'False': False}.get(line[1], False)                


  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The folder containing the results
  working_folder="Working_Folder"
  # The name of the folder containing the computed dataset of the parameter scanning
  raw_sim_data="raw_sim_data"
  # The name of the folder containing the generated plots of the parameter scanning
  tc_parameter_scan_dir="tc_param_scan"  

  models_dir = os.path.join(project_dir, models_folder)
  results_dir = os.path.join(project_dir, working_folder, model[:-4])
  tmp_dir = os.path.join(copasi_reports_path)




  logger.info("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()

    
  
  logger.info("\n")
  logger.info("#############################################################")
  logger.info("### Processing model " + model)
  logger.info("#############################################################")
  logger.info("")    


  # preprocessing
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)


  if generate_data == True:
    logger.info("\n")
    logger.info("Data generation:")
    logger.info("################")
    single_param_scan__generate_data.main(model, 
					  scanned_species, 
					  single_param_scan_simulations_number, 
					  simulate__intervals,
					  levels_number,
					  models_dir, 
					  os.path.join(results_dir, raw_sim_data), 
					  tmp_dir)
  
  
  if analyse_data == True:
    logger.info("\n")
    logger.info("Data analysis:")
    logger.info("##############")
    single_param_scan__analyse_data.main(model[:-4], scanned_species, single_param_scan_knock_down_only, results_dir, 
					 raw_sim_data, tc_parameter_scan_dir, simulate__xaxis_label, 
					 single_param_scan_simulations_number, 
					 single_param_scan_percent_levels, 
					 min_level, max_level, levels_number,
					 homogeneous_lines)
  
  
  
  if generate_report == True:
    logger.info("\n")
    logger.info("Report generation:")
    logger.info("##################")
    single_param_scan__generate_report.main(model[:-4], scanned_species, results_dir, tc_parameter_scan_dir)
  


  # Print the pipeline elapsed time
  end = time.clock()
  logger.info("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  logger.info("\n<END PIPELINE>\n")


  if len(glob.glob(os.path.join(results_dir, "*"+model[:-4]+"*.pdf"))) == 1 and len(glob.glob(os.path.join(results_dir, tc_parameter_scan_dir, model[:-4]+"*.png"))) > 0:
    return 0
  return 1
     