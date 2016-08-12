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
from subprocess import Popen,PIPE
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from io_util_functions import refresh_directory

from sb_config import get_copasi


# Input parameters
# model, inputdir, outputdir
def main(model, inputdir, outputdir):

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

  p = Popen(command)
  p.wait()
 
  # move the output file
  move(os.path.join(model[:-4]+".csv"), outputdir)

    
