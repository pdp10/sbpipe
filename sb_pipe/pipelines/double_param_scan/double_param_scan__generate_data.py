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
# Object: Run CopasiSE performing a parameter scan.
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-24 13:14:32 $


import os
import sys
import glob
import subprocess
import shutil
import logging
logger = logging.getLogger('sbpipe')

# For reading the first N lines of a file.
from itertools import islice


SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE)
from sb_config import get_copasi

sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from copasi_utils import replace_str_copasi_sim_report


# INITIALIZATION
# model: read the model
# species: the species to knock-down (name of the species as in copasi)
# sim_number: Number of times the model should be simulated. For deterministic simulations, ${sim_number}==1 . For stochastic simulations, ${sim_number}==h. 
# models_dir: Read the models dir
# output_dir: the output dir
def main(model, species, sim_number, simulate__intervals, 
	 single_param_scan_intervals, models_dir, output_dir):


  if not os.path.isfile(os.path.join(models_dir,model)):
    logger.error(os.path.join(models_dir, model) + " does not exist.") 
    return
  
  filesToDelete = glob.glob(os.path.join(output_dir,model[:-4]+"*"))
  for f in filesToDelete:
    os.remove(f)
  if not os.path.exists(output_dir):
    os.mkdir(output_dir) 
    

  logger.info("Simulating Model: "+ model)

  model_noext=model[:-4]

  names=[]
  species_index=-1
  species_level=-1
  # Set the number of intervals
  intervals=int(single_param_scan_intervals)+1
  # Set the number of timepoints
  timepoints=int(simulate__intervals)+1

  copasi=get_copasi()
  if copasi == None:
    logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
    return  
  
  for i in xrange(0, int(sim_number)):
    
      logger.info("Simulation No.: "+str(i))
      # run CopasiSE. Copasi must generate a (TIME COURSE) report called ${model_noext}.csv
      process = subprocess.Popen([copasi, '--nologo', os.path.join(models_dir, model)])
      process.wait()
      

      if (not os.path.isfile(os.path.join(models_dir, model_noext+".csv")) and 
          not os.path.isfile(os.path.join(models_dir, model_noext+".txt"))): 
	  logger.warn(os.path.join(models_dir, model_noext+".csv") + " (or .txt) does not exist!") 
	  continue
      
      # Replace some string in the report file   
      replace_str_copasi_sim_report(os.path.join(models_dir, model_noext+".csv"))
      
      
      #mv ${param_scan__double_perturb_copasi_model%.*}.csv ${raw_sim_data}/      
      #bash ${SB_PIPE}/bin/sb_param_scan__double_perturb/param_scan__double_perturb_extract_timepoints.sh ${dp_datasets_dir} ${param_scan__double_perturb_copasi_model} ${param_scan__double_perturb_simulation_length}

