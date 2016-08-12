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
from io_util_functions import refresh_directory



# Input parameters
# model: read the model
# inputdir: read the models dir
# output_dir: The output dir
# sim_number: the number of simulations to perform
def main(model, inputdir, cluster_type, pp_cpus, nfits, outputdir, sim_data_folder, updated_models_folder):
  
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
