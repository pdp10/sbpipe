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
import datetime

import os
import sys
import glob
import shutil
import subprocess
import logging
logger = logging.getLogger('sbpipe')


SB_PIPE = os.environ["SB_PIPE"]

from sb_config import get_copasi, which

sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from config_parser import config_parser
from io_util_functions import refresh_directory
from latex_reports import latex_report_simulate


"""
This module provides the user with a complete pipeline of scripts for computing 
model sensitivity analysis using Copasi
"""

def main(config_file):
    """
    Execute and collect results for model sensitivity using Copasi
    Keyword arguments:
	config_file -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
    """

    logger.info("Reading file " + config_file + " : \n")
    
    # Initialises the variables for this pipeline
    try:
	(generate_data, analyse_data, generate_report,
	  project_dir, model) = config_parser(config_file, "sensitivity")  
    except Exception as e:
	logger.error(e.message)
	import traceback
	logger.debug(traceback.format_exc())    
	return 2
    
    
    # INTERNAL VARIABLES
    # The folder containing the models
    models_folder="Models"
    # The working folder containing the results
    working_folder="Working_Folder"  
    # The folder containing the sensitivity analysis results
    sensitivities_dir="sensitivities"
    
    models_dir = os.path.join(project_dir, models_folder)
    outputdir = os.path.join(project_dir, working_folder, model[:-4], sensitivities_dir)


    # Get the pipeline start time
    start = datetime.datetime.now().replace(microsecond=0)

	

    logger.info("\n")
    logger.info("Processing model " + model)
    logger.info("#############################################################")
    logger.info("")


    # preprocessing
    # remove the folder the previous results if any
  #   filesToDelete = glob.glob(os.path.join(sensitivities_dir, "*.png"))
  #   for f in filesToDelete:
  #     os.remove(f)
    if not os.path.exists(outputdir):
	os.mkdir(outputdir)



    if generate_data == True:
	logger.info("\n")
	logger.info("Data generation:")
	logger.info("################")
	fun_generate_data(model, models_dir, outputdir) 


    if analyse_data == True:
	logger.info("\n")
	logger.info("Data analysis:")
	logger.info("##############")
	fun_analyse_data(outputdir)  


    if generate_report == True:
	logger.info("\n")
	logger.info("Report generation:")
	logger.info("##################")
	fun_generate_report()     


    # Print the pipeline elapsed time
    end = datetime.datetime.now().replace(microsecond=0)
    logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end-start)) 


    if len(glob.glob(os.path.join(outputdir, '*.csv'))) > 0:
	return 0
    return 1
    






# Input parameters
# model, inputdir, outputdir
def fun_generate_data(model, inputdir, outputdir):

    if not os.path.isfile(os.path.join(inputdir,model)):
	logger.error(os.path.join(inputdir, model) + " does not exist.") 
	return  

    # folder preparation
    refresh_directory(outputdir, model[:-4])

    # execute runs simulations.
    logger.info("Sensitivity analysis for " + model)
    
    # run copasi
    copasi = get_copasi()
    if copasi == None:
	logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
	return  
    
    command = [copasi, os.path.join(inputdir, model[:-4]+".cps")]

    p = subprocess.Popen(command)
    p.wait()
  
    # move the output file
    move(os.path.join(model[:-4]+".csv"), outputdir)
  
  
  
  



# Input parameters
# outputdir
def fun_analyse_data(outputdir):
    process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines','sensitivity','plot_sensitivity.r'), outputdir])
    process.wait()







# INITIALIZATION
# model_noext: read the model_noext
# outputdir: read the outputdir  
# sim_plots_folder: the directory containing the time courses results combined with experimental data  
def fun_generate_report(model_noext, outputdir, sim_plots_folder):
    
    if not os.path.exists(os.path.join(outputdir, sim_plots_folder)): 
	logger.error("input_dir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.");
	return    
      
    logger.info("Generating a LaTeX report")
    filename_prefix="report__sensitivity_"
    latex_report_simulate(outputdir, sim_plots_folder, model_noext, filename_prefix)
    
    pdflatex = which("pdflatex")
    if pdflatex == None:
	logger.error("pdflatex not found! pdflatex must be installed for pdf reports.")
	return
      
    logger.info("Generating PDF report")  
    currdir=os.getcwd()
    os.chdir(outputdir)

    logger.info(pdflatex + " -halt-on-error " + filename_prefix + model_noext + ".tex ... ") 
    p1 = subprocess.Popen([pdflatex, "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=subprocess.PIPE)
    p1.communicate()[0]
    p1 = subprocess.Popen([pdflatex, "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=subprocess.PIPE)
    p1.communicate()[0]
    
    os.chdir(currdir)
    
    