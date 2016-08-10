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


# INITIALIZATION (COMMENTS TO UPDATE)
# model: read the model
# species: the species to knock-down (name of the species as in copasi)
# sim_number: Number of times the model should be simulated. For deterministic simulations, ${sim_number}==1 . For stochastic simulations, ${sim_number}==h. 
# models_dir: Read the models dir
# output_dir: the output dir
def main(model, scanned_par1, scanned_par2, scan_intervals_par1, scan_intervals_par2, sim_length, models_dir, output_dir):


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

  copasi=get_copasi()
  if copasi == None:
    logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
    return  
  
  
  # run CopasiSE. Copasi must generate a (TIME COURSE) report called ${model_noext}.csv
  process = subprocess.Popen([copasi, '--nologo', os.path.join(models_dir, model)])
  process.wait()
  

  if (not os.path.isfile(os.path.join(models_dir, model_noext+".csv")) and 
      not os.path.isfile(os.path.join(models_dir, model_noext+".txt"))): 
      logger.warn(os.path.join(models_dir, model_noext+".csv") + " (or .txt) does not exist!") 
      return
  
  # Replace some string in the report file   
  replace_str_copasi_sim_report(os.path.join(models_dir, model_noext+".csv"))
  
  
  
### TODO CONVERT THE FOLLOWING FROM BASH TO PYTHON
  
  #mv ${param_scan__double_perturb_copasi_model%.*}.csv ${raw_sim_data}/      
  
  
  # remove blank lines, if present (this is required if one single instance of copasi is executed)
#sed -i '/^$/d' ${path}/${param_scan__double_perturb_copasi_model%.*}.csv



## Extract a selected time point from all perturbed time courses contained in ${param_scan__double_perturb_copasi_model%.*}.csv
#for (( i=0; i<=${param_scan__double_perturb_simulation_length}; i++ ))
#do
    #fileout="${param_scan__double_perturb_copasi_model%.*}__tp_${i}.csv"
    #echo "Extract time point: ${i}"
    ## extract the header line and clean it
    #head -1 "${path}/${param_scan__double_perturb_copasi_model%.*}.csv" > ${path}/$fileout
    ##`replace_str_copasi_sim_report "${path}" "${fileout}"`  
    ## extract the i-th time point
    #sed -n "$((${i}+2))~$((${param_scan__double_perturb_simulation_length}+1))p" "${path}/${param_scan__double_perturb_copasi_model%.*}.csv" >> ${path}/$fileout
#done
  

