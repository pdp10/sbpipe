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
import glob
from shutil import copyfile, move
import datetime
from subprocess import Popen,PIPE

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE)
from sb_config import getCopasi

sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from copasi_utils import replace_str_copasi_sim_report
from io_util_functions import replace_string_in_file
from parallel_computation import parallel_computation


# Input parameters
# model: read the model
# models_dir: read the models dir
# output_dir: The output dir
# tmp_dir: read the temp dir
# runs: the number of simulations to perform
def main(model, models_dir, output_dir, tmp_dir, cluster_type="pp", pp_cpus=2, runs=1):
  
  if runs < 1: 
    print("ERROR: variable " + str(runs) + " must be greater than 0. Please, check your configuration file.");
    return

  if not os.path.isfile(os.path.join(models_dir,model)):
    print(os.path.join(models_dir, model) + " does not exist.") 
    return  

  # folder preparation
  filesToDelete = glob.glob(os.path.join(output_dir, model[:-4]+"*"))
  for f in filesToDelete:
    os.remove(f)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # execute runs simulations.
  print("Simulating model " + model + " for " + str(runs) + " time(s)")
  # Replicate the copasi file and rename its report file
  for i in xrange(1, runs + 1):
    copyfile(os.path.join(models_dir,model), os.path.join(models_dir,model[:-4])+str(i)+".cps") 
    replace_string_in_file(os.path.join(models_dir,model[:-4])+str(i)+".cps", 
			   model[:-4]+".csv", 
			   model[:-4]+str(i)+".csv")
  
  # run copasi in parallel
  copasi = getCopasi()
  timestamp = "{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
  command = copasi + " " + os.path.join(models_dir, model[:-4]+timestamp+".cps")
  servers="localhost:65000"
  secret="sb_pipe"
  parallel_computation(command, timestamp, cluster_type, runs, output_dir, servers, secret, pp_cpus)
  
 
  for file in glob.glob(os.path.join(tmp_dir, model[:-4]+"*.csv")):
    # Replace some string in the report file
    replace_str_copasi_sim_report(file)
    # rename and move the output file
    move(file, os.path.join(output_dir, model[:-4]+"__sim_" + file.replace(os.path.join(tmp_dir, model[:-4]), "")[:-4] + ".csv"))
    
