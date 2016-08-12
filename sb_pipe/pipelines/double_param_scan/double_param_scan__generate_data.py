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
from io_util_functions import refresh_directory


# INITIALIZATION (COMMENTS TO UPDATE)
# model: read the model
# species: the species to knock-down (name of the species as in copasi)
# sim_number: Number of times the model should be simulated. For deterministic simulations, ${sim_number}==1 . For stochastic simulations, ${sim_number}==h. 
# inputdir: Read the models dir
# outputdir: the output dir
def main(model, sim_length, inputdir, outputdir):

  if not os.path.isfile(os.path.join(inputdir,model)):
    logger.error(os.path.join(inputdir, model) + " does not exist.") 
    return
  
  refresh_directory(outputdir, model[:-4])    

  logger.info("Simulating Model: "+ model)

  model_noext=model[:-4]

  copasi=get_copasi()
  if copasi == None:
    logger.error("CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
    return  
  
  
  # run CopasiSE. Copasi must generate a (TIME COURSE) report
  process = subprocess.Popen([copasi, '--nologo', os.path.join(inputdir, model)])
  process.wait()
  

  if (not os.path.isfile(os.path.join(inputdir, model_noext+".csv")) and 
      not os.path.isfile(os.path.join(inputdir, model_noext+".txt"))): 
      logger.warn(os.path.join(inputdir, model_noext+".csv") + " (or .txt) does not exist!") 
      return
  
  if os.path.isfile(os.path.join(inputdir, model_noext+".txt")):
    os.rename(os.path.join(inputdir, model_noext+".txt"), os.path.join(inputdir, model_noext+".csv"))
    
  # Replace some string in the report file   
  replace_str_copasi_sim_report(os.path.join(inputdir, model_noext+".csv"))

  # copy file removing empty lines 
  with open(os.path.join(inputdir, model_noext+".csv"),'r') as filein, open(os.path.join(outputdir, model_noext+".csv"),'w') as fileout:
    for line in filein:
        if not line.isspace():
            fileout.write(line)
  os.remove(os.path.join(inputdir, model_noext+".csv"))


  # Extract a selected time point from all perturbed time courses contained in the report file
  with open(os.path.join(outputdir, model_noext+".csv"),'r') as filein:
    lines = filein.readlines()
    header = lines[0]
    lines = lines[1:]
    timepoints = range(0, sim_length+1)
    filesout = []
    try:
	filesout = [open(os.path.join(outputdir, model_noext + "__tp_%d.csv" % i), "w") for i in timepoints]
	# copy the header
	for fileout in filesout: 
	  fileout.write(header)
	# extract the i-th time point and copy it to the corresponding i-th file
	for line in lines:
	  tp = line.rstrip().split('\t')[0]
	  if (not '.' in tp and int(tp) in timepoints):
	    filesout[int(tp)].write(line)
    finally:
	for fileout in filesout:
	    fileout.close()      
	  
