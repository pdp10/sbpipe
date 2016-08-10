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
import datetime


import glob
import os
import os.path
import sys
import shutil
import subprocess
import logging
logger = logging.getLogger('sbpipe')

import double_param_scan__generate_data
import double_param_scan__analyse_data
import double_param_scan__generate_report

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from config_parser import config_parser



"""
This module provides the user with a complete pipeline of scripts for computing 
a double parameter scan using copasi.
"""

def main(config_file):
  """
  Execute and collect results from a parameter scan using Copasi
  Keyword arguments:
      config_file -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """

  logger.info("Reading file " + config_file + " : \n")
  
  

  # e.g.
  #scanned_var1 = "mTORC1"
  #scan_intervals_var1 = 9
  #scan_type_var1 = "inhibition" | "overexpression" | "mixed"
  #sim_length = "21" (e.g. days)
  
  # Initialises the variables for this pipeline
  try:
    (generate_data, analyse_data, generate_report, 
      project_dir, model, scanned_par1, scanned_par2,  
      scan_intervals_par1, scan_intervals_par2, scan_type_par1, scan_type_par2, 
      sim_length, min_level, max_level) = config_parser(config_file, "double_param_scan")
  except Exception as e:
    logger.error(e.message)
    import traceback
    logger.debug(traceback.format_exc())    
    return 2  


  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The folder containing the results
  working_folder="Working_Folder"
  # The name of the folder containing the computed dataset of the parameter scan
  raw_sim_data="raw_double_param_scan_data"
  # The name of the folder containing the generated plots of the parameter scan
  tc_parameter_scan_dir="tc_double_param_scan"  

  models_dir = os.path.join(project_dir, models_folder)
  results_dir = os.path.join(project_dir, working_folder, model[:-4])


  # Get the pipeline start time
  start = datetime.datetime.now().replace(microsecond=0)

    
  
  logger.info("\n")
  logger.info("Processing model " + model)
  logger.info("#############################################################")
  logger.info("")    


  # preprocessing
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)


  if generate_data == True:
    logger.info("\n")
    logger.info("Data generation:")
    logger.info("################")
    #single_param_scan__generate_data.main(model, 
					  #scanned_species, 
					  #single_param_scan_simulations_number, 
					  #simulate__intervals,
					  #levels_number,
					  #models_dir, 
					  #os.path.join(results_dir, raw_sim_data))
  
  
  if analyse_data == True:
    logger.info("\n")
    logger.info("Data analysis: (SKIP)")
    logger.info("##############")      
    #single_param_scan__analyse_data.main(model[:-4], scanned_species, single_param_scan_knock_down_only, results_dir, 
					 #raw_sim_data, tc_parameter_scan_dir, simulate__xaxis_label, 
					 #single_param_scan_simulations_number, 
					 #single_param_scan_percent_levels, 
					 #min_level, max_level, levels_number,
					 #homogeneous_lines)
  
  
  if generate_report == True:
    logger.info("\n")
    logger.info("Report generation: (SKIP)")
    logger.info("##################")
    #single_param_scan__generate_report.main(model[:-4], scanned_species, results_dir, tc_parameter_scan_dir)
  


  # Print the pipeline elapsed time
  end = datetime.datetime.now().replace(microsecond=0)
  logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end-start)) 


  if len(glob.glob(os.path.join(results_dir, "*"+model[:-4]+"*.pdf"))) == 1 and len(glob.glob(os.path.join(results_dir, tc_parameter_scan_dir, model[:-4]+"*.png"))) > 0:
    return 0
  ### TODO : set the next return to 1
  return 0
     