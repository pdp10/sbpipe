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


# INITIALIZATION
# model
# scanned_par1
# scanned_par2
# inputdir
# outputdir
def main(model, scanned_par1, scanned_par2, inputdir, outputdir):

  if not os.path.exists(inputdir): 
    logger.error("input_dir " + inputdir + " does not exist. Generate some data first.");
    return

  # folder preparation
  filesToDelete = glob.glob(os.path.join(outputdir,model+"*"))
  for f in filesToDelete:
    os.remove(f)
  if not os.path.exists(outputdir):
    os.mkdir(outputdir) 

  process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE, 'sb_pipe','pipelines','double_param_scan','double_param_scan__analyse_data.r'), 
			      model, scanned_par1, scanned_par2, inputdir, outputdir])    
  process.wait()
  
