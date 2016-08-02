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
import datetime

import os
import sys
import glob
import shutil
import subprocess
import tarfile
import logging
logger = logging.getLogger('sbpipe')

import param_estim__generate_data
import param_estim__analyse_data
import param_estim__generate_report

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from config_parser import config_parser



"""
This module provides the user with a complete pipeline of scripts comprising the configuration 
and execution of jobs on the cluster, results retrieval and concatenation, parameter estimation 
analyses and finally results storing. This pipeline uses CopasiSE
"""
def main(config_file):
  """
  Execute and collect results from parameter estimation using Copasi
  Keyword arguments:
      config_file -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """  

  logger.info("Reading file " + config_file + " : \n")
  
  # Initialises the variables for this pipeline
  try:
    (generate_data, analyse_data, generate_report, 
      generate_tarball, project_dir, model, 
      cluster, pp_cpus, round, runs, 
      best_fits_percent, data_point_num, 
      plot_2d_66_95cl_corr) = config_parser(config_file, "param_estim")  
  except Exception as e:
    logger.error(e.message)
    import traceback
    logger.debug(traceback.format_exc())    
    return 2
  

  runs = int(runs)
  pp_cpus = int(pp_cpus)
  best_fits_percent = int(best_fits_percent)
  data_point_num = int(data_point_num)

  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The folder containing the working results
  working_folder="Working_Folder"
  # The dataset working folder
  sim_raw_data="sim_raw_data"
  # The folder containing the updated Copasi models
  updated_models_folder="updated_models"
  
  models_dir = os.path.join(project_dir,models_folder)
  working_dir = os.path.join(project_dir, working_folder)

  output_folder = model[:-4]+"_round"+round
  plots_folder = "plots"
  results_dir = os.path.join(working_dir, output_folder)
  plots_dir = os.path.join(results_dir, plots_folder)
  fileout_final_estims = "final_estim_collection.csv"
  fileout_all_estims = "all_estim_collection.csv"
  fileout_approx_ple_stats = "approx_ple_stats.csv"
  fileout_conf_levels = "conf_levels.csv"
  

  # Get the pipeline start time
  start = datetime.datetime.now().replace(microsecond=0)

    
    
  logger.info("\n")
  logger.info("Parameter estimation for model "+model)
  logger.info("#############################################################")
  logger.info("")

  # preprocessing
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)


  if generate_data == True:
    logger.info("\n")
    logger.info("Generate data:")
    logger.info("##############")
    param_estim__generate_data.main(model, 
				    models_dir, 
				    cluster, 
				    pp_cpus, 
				    runs, 
				    results_dir, 
				    sim_raw_data,
				    updated_models_folder)
    

  if analyse_data == True:
    logger.info("\n")
    logger.info("Analyse data:")
    logger.info("#############")
    param_estim__analyse_data.main(os.path.join(results_dir, sim_raw_data), 
				   results_dir, 
				   fileout_final_estims, 
				   fileout_all_estims,
				   fileout_approx_ple_stats,
				   fileout_conf_levels,
				   plots_dir, 
				   best_fits_percent,
				   data_point_num,
				   plot_2d_66_95cl_corr)


  if generate_report == True:
    logger.info("\n")
    logger.info("Report generation:")
    logger.info("##################")
    param_estim__generate_report.main(model[:-4], results_dir, plots_folder)
  


  if generate_tarball == True:
    logger.info("\n")
    logger.info("Store the fits sequences in a tarball:")
    logger.info("#####################################")
    # Create a gz tarball   
    origWD = os.getcwd() # remember our original working directory
    os.chdir(working_dir) # change folder
    with tarfile.open(output_folder+".tgz", "w:gz") as tar:
      tar.add(output_folder, arcname=os.path.basename(output_folder))
    os.chdir(origWD) # get back to our original working directory
    


  # Print the pipeline elapsed time
  end = datetime.datetime.now().replace(microsecond=0)
  logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end-start)) 


  if os.path.isfile(os.path.join(results_dir,fileout_final_estims)) and \
     os.path.isfile(os.path.join(results_dir,fileout_all_estims)) and \
     len(glob.glob(os.path.join(results_dir,'*'+model[:-4]+'*.pdf'))) == 1:
      return 0
  return 1
    
    
