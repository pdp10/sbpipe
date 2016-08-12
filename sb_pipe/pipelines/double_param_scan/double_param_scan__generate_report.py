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
# Object: Autogeneration of latex code containing images
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 22:58:32 $




import os
import sys
from subprocess import Popen,PIPE
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE ,'sb_pipe','utils','python'))
from latex_reports import latex_report_double_param_scan

from sb_config import which

# INITIALIZATION
# model_noext: read the model_noext
# scanned_par1: the first scanned parameter
# scanned_par2: the second scanned parameter
# results_dir: Read the results dir
# plots_dir: The directory containing the plots of the double parameter scan
def main(model_noext, scanned_par1, scanned_par2, results_dir, plots_dir): 
    
    if not os.path.exists(os.path.join(results_dir,plots_dir)): 
	logger.error("input_dir " + os.path.join(results_dir,plots_dir) + " does not exist. Analyse the data first.");
	return
    
      
    logger.info("Generating a LaTeX report")
    logger.info(model_noext)
    filename_prefix="report__double_param_scan_"
    latex_report_double_param_scan(results_dir, plots_dir, filename_prefix, 
			  model_noext, scanned_par1, scanned_par2)

    pdflatex = which("pdflatex")
    if pdflatex == None:
	logger.error("pdflatex not found! pdflatex must be installed for pdf reports.")
	return
      
    logger.info("Generating PDF report")  
    currdir=os.getcwd()
    os.chdir(results_dir)

    logger.info(pdflatex + " -halt-on-error " + filename_prefix + model_noext + ".tex ... ") 
    p1 = Popen([pdflatex, "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=PIPE)
    p1.communicate()[0]
    p1 = Popen([pdflatex, "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=PIPE)
    p1.communicate()[0]

    os.chdir(currdir)
