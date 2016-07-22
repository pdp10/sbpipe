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

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from latex_reports import latex_report_simulate



# INITIALIZATION
# model_noext: read the model_noext
# results_dir: read the results_dir  
# plots_dir: the directory containing the time courses results combined with experimental data  
def main(model_noext, results_dir, plots_dir):
    
    if not os.path.exists(os.path.join(results_dir, plots_dir)): 
	print("ERROR: input_dir " + os.path.join(results_dir, plots_dir) + " does not exist. Analyse the data first.");
	return    
      
    print("Generating a LaTeX report")
    filename_prefix="report__sensitivity_"
    latex_report_simulate(results_dir, plots_dir, model_noext, filename_prefix)
    
    
    print("Generating PDF report\n")  
    currdir=os.getcwd()
    os.chdir(results_dir)
    print("pdflatex -halt-on-error " + filename_prefix + model_noext + ".tex ... ") 
    p1 = Popen(["pdflatex", "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=PIPE)
    p1.communicate()[0]
    p1 = Popen(["pdflatex", "-halt-on-error", filename_prefix + model_noext + ".tex"], stdout=PIPE)
    p1.communicate()[0]
    
    # remove temporary files
    #os.remove(filename_prefix+model_noext+".out")
    #os.remove(filename_prefix+model_noext+".log")
    #os.remove(filename_prefix+model_noext+".aux")
    
    os.chdir(currdir)
    print("DONE\n")
  
