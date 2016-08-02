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
import glob
import shutil
from subprocess import Popen,PIPE
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE)
from sb_config import get_copasi

sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from copasi_utils import replace_str_copasi_sim_report
from io_util_functions import replace_string_in_file
from parallel_computation import parallel_computation
from random_functions import get_rand_num_str, get_rand_alphanum_str


# Input parameters
# model: read the model
# models_dir: read the models dir
# output_dir: The output dir
# runs: the number of simulations to perform
def main(model, models_dir, output_dir, cluster_type="pp", pp_cpus=2, runs=1):
  
  if runs < 1: 
    logger.error("variable " + str(runs) + " must be greater than 0. Please, check your configuration file.");
    return

  if not os.path.isfile(os.path.join(models_dir,model)):
    logger.error(os.path.join(models_dir, model) + " does not exist.") 
    return  

  copasi = get_copasi()
  if copasi == None:
    logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
    return

  # preprocessing
  filesToDelete = glob.glob(os.path.join(output_dir, model[:-4]+"*"))
  for f in filesToDelete:
    os.remove(f)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)  

  # execute runs simulations.
  logger.info("Simulating model " + model + " for " + str(runs) + " time(s)")
  # Replicate the copasi file and rename its report file
  groupid = "_" + get_rand_alphanum_str(20) + "_"
  group_model = model[:-4] + groupid

  for i in xrange(1, runs + 1):
    shutil.copyfile(os.path.join(models_dir,model), os.path.join(models_dir,group_model)+str(i)+".cps") 
    replace_string_in_file(os.path.join(models_dir,group_model)+str(i)+".cps", 
			   model[:-4]+".csv", 
			   group_model+str(i)+".csv")
  
  # run copasi in parallel
  number_to_replace = get_rand_num_str(5)
  command = copasi + " " + os.path.join(models_dir, group_model+number_to_replace+".cps")
  parallel_computation(command, number_to_replace, cluster_type, runs, output_dir, pp_cpus)
  
  # move the report files
  reportFiles = [f for f in os.listdir(models_dir) if re.match(group_model+'[0-9]+.*\.csv', f) or re.match(group_model+'[0-9]+.*\.txt', f)]
  for file in reportFiles:
    # Replace some string in the report file
    replace_str_copasi_sim_report(os.path.join(models_dir, file))
    # rename and move the output file
    shutil.move(os.path.join(models_dir, file), os.path.join(output_dir, file.replace(groupid, "_")[:-4] + ".csv"))
   
    
  # removed repeated copasi files
  repeatedCopasiFiles = [f for f in os.listdir(models_dir) if re.match(group_model+'[0-9]+.*\.cps', f)]
  for file in repeatedCopasiFiles:
    os.remove(os.path.join(models_dir, file))  
    
    
    