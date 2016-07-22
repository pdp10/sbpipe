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
# $Date: 2015-05-30 16:14:32 $





# for computing the pipeline elapsed time 
import time

import os
import sys
import glob
import shutil
import subprocess
import logging
logger = logging.getLogger('sbpipe')

from ConfigParser import ConfigParser
from StringIO import StringIO

SB_PIPE = os.environ["SB_PIPE"]
import sensitivity__generate_data
import sensitivity__analyse_data
import sensitivity__generate_report


"""
This module provides the user with a complete pipeline of scripts for computing 
model sensitivity analysis using Copasi
"""

def main(model_configuration):
  """
  Execute and collect results for model sensitivity using Copasi
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
  # The project directory
  project_dir=".."
  # The copasi model
  model="mymodel.cps"
  # The path to Copasi reports
  copasi_reports_path="tmp"  


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
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]
      
  
  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The working folder containing the results
  working_folder="Working_Folder"  
  # The folder containing the sensitivity analysis results
  sensitivities_dir="sensitivities"
  
  models_dir = os.path.join(project_dir, models_folder)
  results_dir = os.path.join(project_dir, working_folder, model[:-4], sensitivities_dir)
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
  # remove the folder the previous results if any
#   filesToDelete = glob.glob(os.path.join(sensitivities_dir, "*.png"))
#   for f in filesToDelete:
#     os.remove(f)
  if not os.path.exists(results_dir):
    os.mkdir(results_dir)



  if generate_data == True:
    logger.info("\n")
    logger.info("Data generation:")
    logger.info("################")
    sensitivity__generate_data.main(model, models_dir, results_dir, tmp_dir) 


  if analyse_data == True:
    logger.info("\n")
    logger.info("Data analysis:")
    logger.info("##############")
    sensitivity__analyse_data.main(results_dir)  


  if generate_report == True:
    logger.info("\n")
    logger.info("Report generation:")
    logger.info("##################")
    sensitivity__generate_report.main()     


  # Print the pipeline elapsed time
  end = time.clock()
  logger.info("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  logger.info("\n<END PIPELINE>\n")


  if len(glob.glob(os.path.join(results_dir, '*.csv'))) > 0:
      return 0
  return 1
    
    