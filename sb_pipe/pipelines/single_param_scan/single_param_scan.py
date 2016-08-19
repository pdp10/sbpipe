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

# For reading the first N lines of a file.
from itertools import islice

SB_PIPE = os.environ["SB_PIPE"]
from sb_config import get_copasi, which

sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from config_parser import config_parser
from copasi_utils import replace_str_copasi_sim_report
from io_util_functions import refresh_directory
from latex_reports import latex_report_single_param_scan



"""
This module provides the user with a complete pipeline of scripts for computing 
a single parameter scan using copasi.
"""

def main(config_file):
  """
  Execute and collect results from a parameter scan using Copasi
  Keyword arguments:
      config_file -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """

  logger.info("Reading file " + config_file + " : \n")
  
  # Initialises the variables for this pipeline
  try:
    (generate_data, analyse_data, generate_report, 
      project_dir, model, scanned_par,  
      simulate__intervals, simulate__xaxis_label, 
      single_param_scan_simulations_number, single_param_scan_percent_levels, 
      single_param_scan_knock_down_only, levels_number, min_level, max_level, 
      homogeneous_lines) = config_parser(config_file, "single_param_scan")
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
  # The name of the folder containing the computed dataset of the parameter scanning
  sim_data_folder="single_param_scan_data"
  # The name of the folder containing the generated plots of the parameter scanning
  sim_plots_folder="single_param_scan_plots"  

  models_dir = os.path.join(project_dir, models_folder)
  outputdir = os.path.join(project_dir, working_folder, model[:-4])


  # Get the pipeline start time
  start = datetime.datetime.now().replace(microsecond=0)

    
  
  logger.info("\n")
  logger.info("Processing model " + model)
  logger.info("#############################################################")
  logger.info("")    


  # preprocessing
  if not os.path.exists(outputdir):
    os.makedirs(outputdir)


  if generate_data == True:
    logger.info("\n")
    logger.info("Data generation:")
    logger.info("################")
    fun_generate_data(model, 
		      scanned_par, 
		      single_param_scan_simulations_number, 
		      simulate__intervals,
		      levels_number,
		      models_dir, 
		      os.path.join(outputdir, sim_data_folder))
  
  
  if analyse_data == True:
    logger.info("\n")
    logger.info("Data analysis:")
    logger.info("##############")
    fun_analyse_data(model[:-4], scanned_par, single_param_scan_knock_down_only, outputdir, 
		    sim_data_folder, sim_plots_folder, simulate__xaxis_label, 
		    single_param_scan_simulations_number, 
		    single_param_scan_percent_levels, 
		    min_level, max_level, levels_number,
		    homogeneous_lines)
  
  
  
  if generate_report == True:
    logger.info("\n")
    logger.info("Report generation:")
    logger.info("##################")
    fun_generate_report(model[:-4], scanned_par, outputdir, sim_plots_folder)
  


  # Print the pipeline elapsed time
  end = datetime.datetime.now().replace(microsecond=0)
  logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end-start)) 


  if len(glob.glob(os.path.join(outputdir, "*"+model[:-4]+"*.pdf"))) == 1 and len(glob.glob(os.path.join(outputdir, sim_plots_folder, model[:-4]+"*.png"))) > 0:
    return 0
  return 1
     
     
     
     
     
     
     
     
# INITIALIZATION
# model: read the model
# variable: the variable to knock-down (name of the variable as in copasi)
# sim_number: Number of times the model should be simulated. For deterministic simulations, ${sim_number}==1 . For stochastic simulations, ${sim_number}==h. 
# inputdir: Read the models dir
# outputdir: the output dir
def fun_generate_data(model, variable, sim_number, simulate_intervals, 
		      single_param_scan_intervals, inputdir, outputdir):

    if not os.path.isfile(os.path.join(inputdir,model)):
	logger.error(os.path.join(inputdir, model) + " does not exist.") 
	return
    
    refresh_directory(outputdir, model[:-4])    

    logger.info("Simulating Model: "+ model)

    model_noext=model[:-4]

    names=[]
    variable_index=-1
    variable_level=-1
    # Set the number of intervals
    intervals=int(single_param_scan_intervals)+1
    # Set the number of timepoints
    timepoints=int(simulate_intervals)+1

    copasi=get_copasi()
    if copasi == None:
	logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
	return  
    
    for i in xrange(0, int(sim_number)):
      
	logger.info("Simulation No.: "+str(i))
	# run CopasiSE. Copasi must generate a (TIME COURSE) report called ${model_noext}.csv
	process = subprocess.Popen([copasi, '--nologo', os.path.join(inputdir, model)])
	process.wait()
	

	if (not os.path.isfile(os.path.join(inputdir, model_noext+".csv")) and 
	    not os.path.isfile(os.path.join(inputdir, model_noext+".txt"))): 
	    logger.warn(os.path.join(inputdir, model_noext+".csv") + " (or .txt) does not exist!") 
	    continue
	
	# Replace some string in the report file   
	replace_str_copasi_sim_report(os.path.join(inputdir, model_noext+".csv"))
	



	# Find the index of variable in the header file, so it is possible to read the amount at 
	# the second line.
	if i == 0:
	  logger.info("Retrieving column index for "+variable+" from file "+ os.path.join(inputdir, model_noext+".csv"))
	  # Read the first line of a file.
	  with open(os.path.join(inputdir, model_noext+".csv")) as myfile:
	    # 1 is the number of lines to read, 0 is the i-th element to extract from the list.
	    header = list(islice(myfile, 1))[0].replace("\n", "").split('\t')
	  logger.debug(header)
	  for j, name in enumerate(header): 
	    logger.info(str(j) + " " + name + " " + variable)
	    if name == variable: 
	      variable_index=j 
	      break;
	  if variable_index == -1: 
	    logger.error("Column index for "+variable+": "+str(variable_index)+". Species not found! You must add "+variable+
	    " to the Copasi report.")
	    return
	  else:
	    logger.info("Column index for "+variable+": "+str(variable_index))


	# Prepare the Header for the output files
	# Add a \t at the end of each element of the header
	header = [h + "\t" for h in header]
	# Remove the \t for the last element.
	header[-1] = header[-1].strip()      


	# Prepare the table content for the output files
	for j in xrange(0, intervals):
	  # Read the variable level
	  # Read the second line of a file.
	  with open(os.path.join(inputdir, model_noext+".csv")) as myfile:
	    # 2 is the number of lines to read, 1 is the i-th element to extract from the list.	  
	    initial_configuration = list(islice(myfile, 2))[1].replace("\n", "").split('\t')
	  #print initial_configuration
	  variable_level = initial_configuration[variable_index]
	  if variable_level == -1: 
	    logger.error("variable_level not configured!")
	    return 
	  else:
	    logger.info(variable + " level: "+str(variable_level)+" (list index: "+str(variable_index)+")")
	  

	  # copy the -th run to a new file: add 1 to timepoints because of the header.
	  round_variable_level = variable_level
	  # Read the first timepoints+1 lines of a file.
	  with open(os.path.join(inputdir, model_noext+".csv"), 'r') as file:
	    table = list(islice(file, timepoints+1))  

	  # Write the extracted table to a separate file
	  with open(os.path.join(outputdir, model_noext+"__sim_"+str(i+1)+"__level_"+str(round_variable_level)+".csv"), 'w') as file:
	    for line in table:
	      file.write(line)

	  with open(os.path.join(inputdir, model_noext+".csv"), 'r') as file:
	    # read all lines
	    lines = file.readlines()
	    

	  with open(os.path.join(inputdir, model_noext+".csv~"), 'w') as file:
	    file.writelines(header)
	    file.writelines(lines[timepoints+1:])

	  shutil.move(os.path.join(inputdir, model_noext+".csv~"), os.path.join(inputdir, model_noext+".csv"))
	  
	  
	# remove the file
	os.remove(os.path.join(inputdir, model_noext+".csv"))
     
     
     
     
     
     
     
# INITIALIZATION
# model
# scanned_par 
# knock_down_only
# outputdir
# sim_data_folder
# sim_plots_folder
# simulate__xaxis_label
# simulations_number
# percent_levels
# min_level
# max_level
# levels_number
# homogeneous_lines
def fun_analyse_data(model, scanned_par, knock_down_only, outputdir, 
		    sim_data_folder, sim_plots_folder, simulate__xaxis_label, 
		    simulations_number, 
		    percent_levels, min_level, max_level, levels_number, 
		    homogeneous_lines):

    if not os.path.exists(os.path.join(outputdir,sim_data_folder)): 
	logger.error("input_dir " + os.path.join(outputdir,sim_data_folder) + " does not exist. Generate some data first.");
	return
    
      # some control
    if float(min_level) < 0: 
	logger.error("min_level MUST BE non negative.")
	return
    
    if percent_levels and float(max_level) < 100: 
	logger.error("max_level cannot be less than 100 (=ctrl) if option `percent_levels` is True .")
	return  
    
    # folder preparation
    refresh_directory(os.path.join(outputdir,sim_plots_folder), model[:-4])

    process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE, 'sb_pipe','pipelines','single_param_scan','single_param_scan__analyse_data.r'), 
				model, scanned_par, str(knock_down_only), outputdir, sim_data_folder, sim_plots_folder, simulate__xaxis_label, 
				simulations_number, str(percent_levels), str(min_level), str(max_level), str(levels_number), 
				str(homogeneous_lines)])    
    process.wait()
     
     
     
     
     

# INITIALIZATION
# model_noext: read the model_noext
# species: Read the species
# outputdir: Read the results dir
# sim_plots_folder: The directory containing the plots of the single parameter scan
# legend_noext: The name of the legend
def fun_generate_report(model_noext, species, outputdir, sim_plots_folder): 
    
    if not os.path.exists(os.path.join(outputdir,sim_plots_folder)): 
	logger.error("input_dir " + os.path.join(outputdir,sim_plots_folder) + " does not exist. Analyse the data first.");
	return
    
      
    logger.info("Generating a LaTeX report")
    logger.info(model_noext)
    filename_prefix="report__single_param_scan_"
    latex_report_single_param_scan(outputdir, sim_plots_folder, filename_prefix, 
				   model_noext, species)

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