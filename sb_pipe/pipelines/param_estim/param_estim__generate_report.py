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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 12:38:32 $
# $Id: simulate__gen_report.py,v 1.0 2016-06-23 12:45:32 Piero Dalle Pezze Exp $



import os
import sys
from subprocess import Popen,PIPE
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from latex_reports import latex_report

from sb_config import which


# INITIALIZATION
# model_noext: read the model_noext
# results_dir: read the results_dir  
# plots_dir: the directory containing the time courses results combined with experimental data  
def main(model_noext, results_dir, plots_dir):
    
    if not os.path.exists(os.path.join(results_dir, plots_dir)): 
	logger.error("input_dir " + os.path.join(results_dir, plots_dir) + " does not exist. Analyse the data first.");
	return       
      
    logger.info("Generating LaTeX report")
    filename_prefix="report__param_estim_"
    latex_report(results_dir, plots_dir, model_noext, filename_prefix)

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
