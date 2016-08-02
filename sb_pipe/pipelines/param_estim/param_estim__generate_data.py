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
# Object: Execute the model several times for deterministic or stochastical analysis
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 13:45:32 $




import os
import sys
import re
import shutil
from subprocess import Popen,PIPE
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE)
from sb_config import get_copasi

sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from RandomiseParameters import *
from parallel_computation import parallel_computation
from random_functions import get_rand_num_str, get_rand_alphanum_str



# Input parameters
# model: read the model
# models_dir: read the models dir
# output_dir: The output dir
# sim_number: the number of simulations to perform
def main(model, models_dir, cluster_type, pp_cpus, nfits, results_dir, reports_folder, updated_models_folder):
  
  if int(nfits) < 1: 
    logger.error("variable " + nfits + " must be greater than 0. Please, check your configuration file.");
    return

  if not os.path.isfile(os.path.join(models_dir,model)):
    logger.error(os.path.join(models_dir, model) + " does not exist.") 
    return  
  
  if not os.path.exists(os.path.join(results_dir, reports_folder)):
    os.mkdir(os.path.join(results_dir, reports_folder)) 
  
  if not os.path.exists(os.path.join(results_dir, updated_models_folder)):
    os.mkdir(os.path.join(results_dir, updated_models_folder)) 


  copasi = get_copasi()
  if copasi == None:
    logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
    return

  logger.info("Configure Copasi:")
  logger.info("Replicate a Copasi file configured for parameter estimation and randomise the initial parameter values")
  groupid = "_" + get_rand_alphanum_str(20) + "_"
  group_model = model[:-4] + groupid   
  pre_param_estim = RandomiseParameters(models_dir, model)
  pre_param_estim.print_parameters_to_estimate()
  pre_param_estim.generate_instances_from_template(nfits, groupid)
  

  logger.info("\n")
  logger.info("Parallel parameter estimation:")  
  number_to_replace = get_rand_num_str(5)
  command = copasi + " -s "+os.path.join(models_dir, group_model+number_to_replace+".cps")+" "+os.path.join(models_dir, group_model+number_to_replace+".cps")
  parallel_computation(command, number_to_replace, cluster_type, nfits, results_dir, pp_cpus)

  # Move the report files to the results_dir
  reportFiles = [f for f in os.listdir(models_dir) if re.match(group_model+'[0-9]+.*\.csv', f) or re.match(group_model+'[0-9]+.*\.txt', f)]
  for file in reportFiles:
    # copy report and remove the groupid
    shutil.move(os.path.join(models_dir, file), os.path.join(results_dir, reports_folder, file.replace(groupid, "_")))

  # removed repeated copasi files
  repeatedCopasiFiles = [f for f in os.listdir(models_dir) if re.match(group_model+'[0-9]+.*\.cps', f)]
  for file in repeatedCopasiFiles:
    #os.remove(os.path.join(models_dir, file))
    shutil.move(os.path.join(models_dir, file), os.path.join(results_dir, updated_models_folder, file.replace(groupid, "_")))
