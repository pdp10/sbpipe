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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 16:14:32 $




# for computing the pipeline elapsed time 
import datetime
import os
import sys
import glob
import re
import shutil
import logging
from subprocess import Popen,PIPE
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from sb_config import get_copasi,which
from config_parser import config_parser
from copasi_utils import replace_str_copasi_sim_report
from io_util_functions import refresh_directory, replace_string_in_file
from parallel_computation import parallel_computation
from random_functions import get_rand_num_str, get_rand_alphanum_str
from latex_reports import latex_report_simulate


"""
This module provides the user with a complete pipeline of scripts for running 
a model simulation using copasi
"""

def main(config_file):
  """
  Execute and collect results for a model simulation using Copasi
  Keyword arguments:
      config_file -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """
  
  logger.info("Reading file " + config_file + " : \n")
  
  # Initialises the variables for this pipeline
  try:
    (generate_data, analyse_data, generate_report,
      project_dir, model, cluster, pp_cpus, runs, 
      simulate__xaxis_label) = config_parser(config_file, "simulate")
  except Exception as e:
    logger.error(e.message)
    import traceback
    logger.debug(traceback.format_exc())
    return 2
  
  
  runs = int(runs)
  pp_cpus = int(pp_cpus)

  # Some controls
  if runs < 1: 
    logger.error("variable `runs` must be greater than 0. Please, check your configuration file.");
    return 1


  # INTERNAL VARIABLES
  # The data folder containing the dataset
  data_folder="Data"  
  # The folder containing the models
  models_folder="Models"
  # The folder containing the working results
  working_folder="Working_Folder"
  # The dataset working folder
  sim_data_folder="simulate_data"
  # The dataset mean timecourses dir
  sim_plots_folder="simulate_plots"

  models_dir = os.path.join(project_dir, models_folder)
  outputdir = os.path.join(project_dir, working_folder, model[:-4])
  data_dir = os.path.join(project_dir, data_folder)


  # Get the pipeline start time
  start = datetime.datetime.now().replace(microsecond=0)


      
  logger.info("\n")
  logger.info("Processing model "+ model)
  logger.info("#############################################################")
  logger.info("")
	
  # preprocessing
  if not os.path.exists(outputdir):
    os.makedirs(outputdir) 
 
 
  if generate_data == True:
    logger.info("\n")
    logger.info("Data generation:")
    logger.info("################")
    fun_generate_data(model, models_dir, os.path.join(outputdir, sim_data_folder), cluster, pp_cpus, runs)


  if analyse_data == True:
    logger.info("\n")
    logger.info("Data analysis:")
    logger.info("##############")
    fun_analyse_data(model[:-4], os.path.join(outputdir, sim_data_folder), outputdir, sim_plots_folder, simulate__xaxis_label)    


  if generate_report == True:
    logger.info("\n")
    logger.info("Report generation:")
    logger.info("##################")
    fun_generate_report(model[:-4], outputdir, sim_plots_folder)


  # Print the pipeline elapsed time
  end = datetime.datetime.now().replace(microsecond=0)
  logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end-start)) 


  if len(glob.glob(os.path.join(outputdir, sim_plots_folder, model[:-4]+'*.png'))) > 0 and len(glob.glob(os.path.join(outputdir, '*'+model[:-4]+'*.pdf'))) == 1:
       return 0
  return 1







# Input parameters
# model: read the model
# inputdir: read the models dir
# outputdir: The output dir
# runs: the number of simulations to perform
def fun_generate_data(model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
    
    if runs < 1: 
	logger.error("variable " + str(runs) + " must be greater than 0. Please, check your configuration file.");
	return

    if not os.path.isfile(os.path.join(inputdir, model)):
	logger.error(os.path.join(inputdir, model) + " does not exist.") 
	return  

    copasi = get_copasi()
    if copasi == None:
	logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
	return

    # folder preparation
    refresh_directory(outputdir, model[:-4])

    # execute runs simulations.
    logger.info("Simulating model " + model + " for " + str(runs) + " time(s)")
    # Replicate the copasi file and rename its report file
    groupid = "_" + get_rand_alphanum_str(20) + "_"
    group_model = model[:-4] + groupid

    for i in xrange(1, runs + 1):
	shutil.copyfile(os.path.join(inputdir,model), os.path.join(inputdir,group_model)+str(i)+".cps") 
	replace_string_in_file(os.path.join(inputdir,group_model)+str(i)+".cps", 
			      model[:-4]+".csv", 
			      group_model+str(i)+".csv")
    
    # run copasi in parallel
    # To make things simple, the last 10 character of groupid are extracted and reversed. 
    # This string will be likely different from groupid and is the string to replace with 
    # the iteration number.
    str_to_replace = groupid[10::-1]
    command = copasi + " " + os.path.join(inputdir, group_model+str_to_replace+".cps")
    parallel_computation(command, str_to_replace, cluster_type, runs, outputdir, pp_cpus)
    
    # move the report files
    reportFiles = [f for f in os.listdir(inputdir) if re.match(group_model+'[0-9]+.*\.csv', f) or re.match(group_model+'[0-9]+.*\.txt', f)]
    for file in reportFiles:
	# Replace some string in the report file
	replace_str_copasi_sim_report(os.path.join(inputdir, file))
	# rename and move the output file
	shutil.move(os.path.join(inputdir, file), os.path.join(outputdir, file.replace(groupid, "_")[:-4] + ".csv"))
    
      
    # removed repeated copasi files
    repeatedCopasiFiles = [f for f in os.listdir(inputdir) if re.match(group_model+'[0-9]+.*\.cps', f)]
    for file in repeatedCopasiFiles:
	os.remove(os.path.join(inputdir, file))  





# Input parameters
# model: read the model
# input_dir: the input dir
# outputdir: The results dir
# sim_plots_folder: The folder containing the plots
# xaxis_label : the x axis label
def fun_analyse_data(model, input_dir, outputdir, sim_plots_folder, xaxis_label):   
    
    if not os.path.exists(input_dir): 
	logger.error("input_dir " + input_dir + " does not exist. Generate some data first.");
	return

    # folder preparation
    filesToDelete = glob.glob(os.path.join(outputdir, sim_plots_folder, model+"*"))    
    for f in filesToDelete:
	os.remove(f)

    if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):  
	os.mkdir(os.path.join(outputdir, sim_plots_folder))

    logger.info("Generating statistics from simulations:")
    process = Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines','simulate','simulate__plot_error_bars.r'), 
				model, input_dir, 
				os.path.join(outputdir, sim_plots_folder), 
				os.path.join(outputdir, 'sim_stats_'+model+'.csv'), xaxis_label])
    process.wait() 

    #logger.info("\nGenerating overlapping plots (sim + exp):")
    #process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines','simulate','simulate__plot_sim_exp_error_bars.r'), model, os.path.join(outputdir,sim_plots_folder), os.path.join(outputdir, tc_mean_exp_dir), os.path.join(outputdir, tc_mean_with_exp_dir), os.path.join(outputdir, 'sim_stats_'+model+'.csv'),  os.path.join(outputdir,'exp_stats_'+model+'.csv')])
    #process.wait() 






# INITIALIZATION
# model_noext: read the model_noext
# outputdir: read the outputdir  
# sim_plots_folder: the directory containing the time courses results combined with experimental data  
def fun_generate_report(model_noext, outputdir, sim_plots_folder):
    
    if not os.path.exists(os.path.join(outputdir, sim_plots_folder)): 
	logger.error("input_dir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.");
	return    
      
    logger.info("Generating a LaTeX report")
    filename_prefix="report__simulate_"
    latex_report_simulate(outputdir, sim_plots_folder, model_noext, filename_prefix)
    
    pdflatex = which("pdflatex")
    if pdflatex == None:
	logger.error("pdflatex not found! pdflatex must be installed for pdf reports.")
	return
      
    logger.info("Generating PDF report")  
    currdir=os.getcwd()
    os.chdir(outputdir)

    logger.info(pdflatex + " -halt-on-error " + filename_prefix + model_noext + ".tex ... ") 
    p1 = Popen([pdflatex, "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=PIPE)
    p1.communicate()[0]
    p1 = Popen([pdflatex, "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=PIPE)
    p1.communicate()[0]
    
    os.chdir(currdir)

