#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
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

SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")
from single_model_latex_reports import latex_report



def main(args):
  
  # INITIALIZATION
  # read the model_noext
  model_noext = args[1]
  # read the results_dir  
  results_dir = args[2]
  # the directory containing the time courses results combined with experimental data  
  tc_mean_dir = args[3]
  # The prefix name for the report  
  simulate__prefix_results_filename = args[4]
    
  print("Generating a LaTeX report containing graphs\n")
  print(model_noext)
  latex_report(results_dir, tc_mean_dir, model_noext, simulate__prefix_results_filename)
  
  
  print("Generating PDF file\n")  
  currdir=os.getcwd()
  os.chdir(results_dir)
  print("pdflatex -halt-on-error " + simulate__prefix_results_filename + model_noext + ".tex ... ") 
  p1 = Popen(["pdflatex", "-halt-on-error", simulate__prefix_results_filename + model_noext + ".tex"], stdout=PIPE)  #>/dev/null
  p1.communicate()[0]
  p1 = Popen(["pdflatex", "-halt-on-error", simulate__prefix_results_filename + model_noext + ".tex"], stdout=PIPE)  #>/dev/null
  p1.communicate()[0]
  
  # remove temporary files
  os.remove(simulate__prefix_results_filename+model_noext+".out")
  os.remove(simulate__prefix_results_filename+model_noext+".log")
  os.remove(simulate__prefix_results_filename+model_noext+".idx")
  os.remove(simulate__prefix_results_filename+model_noext+".toc")
  os.remove(simulate__prefix_results_filename+model_noext+".aux")
  
  os.chdir(currdir)
  print("DONE\n")
  
  
  
main(sys.argv)
