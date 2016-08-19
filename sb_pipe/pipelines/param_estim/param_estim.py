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
import re
import shutil
import subprocess
import tarfile
import logging
logger = logging.getLogger('sbpipe')


SB_PIPE = os.environ["SB_PIPE"]

from sb_config import get_copasi, which
from collect_results import retrieve_final_estimates
from collect_results import retrieve_all_estimates

sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from config_parser import config_parser
from RandomiseParameters import *
from parallel_computation import parallel_computation
from random_functions import get_rand_num_str, get_rand_alphanum_str
from io_util_functions import refresh_directory
from latex_reports import latex_report



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
	  plot_2d_66_95cl_corr,logspace) = config_parser(config_file, "param_estim")  
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
    sim_data_folder="param_estim_data"
    # The folder containing the generated plots
    sim_plots_folder = "param_estim_plots"
    # The folder containing the updated Copasi models
    updated_models_folder="updated_models"
    
    models_dir = os.path.join(project_dir,models_folder)
    working_dir = os.path.join(project_dir, working_folder)

    output_folder = model[:-4]+"_round"+round
    outputdir = os.path.join(working_dir, output_folder)
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
    if not os.path.exists(outputdir):
	os.makedirs(outputdir)


    if generate_data == True:
	logger.info("\n")
	logger.info("Generate data:")
	logger.info("##############")
	fun_generate_data(model, 
			  models_dir, 
			  cluster, 
			  pp_cpus, 
			  runs, 
			  outputdir, 
			  sim_data_folder,
			  updated_models_folder)
      

    if analyse_data == True:
	logger.info("\n")
	logger.info("Analyse data:")
	logger.info("#############")
	fun_analyse_data(model[:-4],
			  os.path.join(outputdir, sim_data_folder), 
			  outputdir, 
			  fileout_final_estims, 
			  fileout_all_estims,
			  fileout_approx_ple_stats,
			  fileout_conf_levels,
			  sim_plots_folder, 
			  best_fits_percent,
			  data_point_num,
			  plot_2d_66_95cl_corr,
			  logspace)


    if generate_report == True:
	logger.info("\n")
	logger.info("Report generation:")
	logger.info("##################")
	fun_generate_report(model[:-4], outputdir, sim_plots_folder)
    


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


    if os.path.isfile(os.path.join(outputdir,fileout_final_estims)) and \
      os.path.isfile(os.path.join(outputdir,fileout_all_estims)) and \
      len(glob.glob(os.path.join(outputdir,'*'+model[:-4]+'*.pdf'))) == 1:
	return 0
    return 1
    
    






# Input parameters
# model: read the model
# inputdir: read the models dir
# output_dir: The output dir
# sim_number: the number of simulations to perform
def fun_generate_data(model, inputdir, cluster_type, pp_cpus, nfits, outputdir, sim_data_folder, updated_models_folder):
    
    if int(nfits) < 1: 
	logger.error("variable " + nfits + " must be greater than 0. Please, check your configuration file.");
	return

    if not os.path.isfile(os.path.join(inputdir,model)):
	logger.error(os.path.join(inputdir, model) + " does not exist.") 
	return  
    
    # folder preparation
    refresh_directory(os.path.join(outputdir, sim_data_folder), model[:-4])
    refresh_directory(os.path.join(outputdir, updated_models_folder), model[:-4])


    copasi = get_copasi()
    if copasi == None:
	logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
	return

    logger.info("Configure Copasi:")
    logger.info("Replicate a Copasi file configured for parameter estimation and randomise the initial parameter values")
    groupid = "_" + get_rand_alphanum_str(20) + "_"
    group_model = model[:-4] + groupid   
    pre_param_estim = RandomiseParameters(inputdir, model)
    pre_param_estim.print_parameters_to_estimate()
    pre_param_estim.generate_instances_from_template(nfits, groupid)
    

    logger.info("\n")
    logger.info("Parallel parameter estimation:")  
    # To make things simple, the last 10 character of groupid are extracted and reversed. 
    # This string will be likely different from groupid and is the string to replace with 
    # the iteration number.
    str_to_replace = groupid[10::-1]
    command = copasi + " -s "+os.path.join(inputdir, group_model+str_to_replace+".cps")+" "+os.path.join(inputdir, group_model+str_to_replace+".cps")
    parallel_computation(command, str_to_replace, cluster_type, nfits, outputdir, pp_cpus)

    # Move the report files to the outputdir
    reportFiles = [f for f in os.listdir(inputdir) if re.match(group_model+'[0-9]+.*\.csv', f) or re.match(group_model+'[0-9]+.*\.txt', f)]
    for file in reportFiles:
	# copy report and remove the groupid
	shutil.move(os.path.join(inputdir, file), os.path.join(outputdir, sim_data_folder, file.replace(groupid, "_")))

    # removed repeated copasi files
    repeatedCopasiFiles = [f for f in os.listdir(inputdir) if re.match(group_model+'[0-9]+.*\.cps', f)]
    for file in repeatedCopasiFiles:
	#os.remove(os.path.join(inputdir, file))
	shutil.move(os.path.join(inputdir, file), os.path.join(outputdir, updated_models_folder, file.replace(groupid, "_")))









# Input parameters
# inputdir, outputdir, fileout_final_estims, fileout_all_estims, fileout_conf_levels, sim_plots_folder, best_fits_percent, data_point_num, plot_2d_66_95cl_corr, logspace
def fun_analyse_data(model, inputdir, outputdir, fileout_final_estims, fileout_all_estims, fileout_approx_ple_stats, fileout_conf_levels, sim_plots_folder, best_fits_percent, data_point_num, plot_2d_66_95cl_corr=False, logspace=True):

    if not os.path.exists(inputdir) or not os.listdir(inputdir): 
      logger.error("inputdir " + inputdir + " does not exist or is empty. Generate some data first.");
      return

    refresh_directory(os.path.join(outputdir,sim_plots_folder), model[:-4])

    logger.info("Collect results:")
    # Collect and summarises the parameter estimation results
    retrieve_final_estimates(inputdir, outputdir, fileout_final_estims)
    retrieve_all_estimates(inputdir, outputdir, fileout_all_estims)  

    logger.info("\n")
    logger.info("Plot results:")
    logger.info("\n")
    process = Popen(['Rscript',
		    os.path.join(SB_PIPE,'sb_pipe','pipelines', 'param_estim', 'main_final_fits_analysis.r'),
		    model,
		    os.path.join(outputdir, fileout_final_estims),
		    os.path.join(outputdir, sim_plots_folder),
		    str(best_fits_percent), str(logspace)])
    process.wait()
    process = Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines', 'param_estim', 'main_all_fits_analysis.r'), 
		    model,
		    os.path.join(outputdir, fileout_all_estims), 
		    os.path.join(outputdir, sim_plots_folder), 
		    str(data_point_num), 
		    os.path.join(outputdir, fileout_approx_ple_stats),
		    os.path.join(outputdir, fileout_conf_levels), 
		    str(plot_2d_66_95cl_corr), str(logspace)])
    process.wait()  
  
  






# INITIALIZATION
# model_noext: read the model_noext
# outputdir: read the outputdir  
# sim_plots_folder: the directory containing the time courses results combined with experimental data  
def fun_generate_report(model_noext, outputdir, sim_plots_folder):

    if not os.path.exists(os.path.join(outputdir, sim_plots_folder)): 
	logger.error("input_dir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.");
	return       
      
    logger.info("Generating LaTeX report")
    filename_prefix="report__param_estim_"
    latex_report(outputdir, sim_plots_folder, model_noext, filename_prefix)

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





