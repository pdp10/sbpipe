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
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 22:58:32 $
# $Id: latex_report.py,v 1.0 2016-06-23 22:58:32 Piero Dalle Pezze Exp $




import os
import sys
from subprocess import Popen,PIPE

SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/utils/python/")
from single_model_latex_reports import latex_report_par_scan


# INITIALIZATION
# model_noext: read the model_noext
# species: Read the species
# results_dir: Read the results dir
# tc_parameter_scan_dir: The directory containing the plots of the single perturbation scan
# param_scan__single_perturb_prefix_results_filename: The prefix for the results filename
# param_scan__single_perturb_legend: The name of the legend
def main(model_noext, species, results_dir, tc_parameter_scan_dir, param_scan__single_perturb_prefix_results_filename, param_scan__single_perturb_legend):
    
  print("Generating a LaTeX report containing graphs\n")
  print(model_noext)
  latex_report_par_scan(results_dir, tc_parameter_scan_dir, param_scan__single_perturb_prefix_results_filename, 
			model_noext, species, param_scan__single_perturb_legend)

  
  
  print("Generating PDF file\n")  
  currdir=os.getcwd()
  os.chdir(results_dir)
  print("pdflatex -halt-on-error " + param_scan__single_perturb_prefix_results_filename + model_noext + ".tex ... ") 
  p1 = Popen(["pdflatex", "-halt-on-error", param_scan__single_perturb_prefix_results_filename + model_noext + ".tex"])  #, stdout=PIPE
  p1.wait()
  p1 = Popen(["pdflatex", "-halt-on-error", param_scan__single_perturb_prefix_results_filename + model_noext + ".tex"])  #, stdout=PIPE
  p1.wait()
  
  # remove temporary files
  os.remove(param_scan__single_perturb_prefix_results_filename+model_noext+".out")
  os.remove(param_scan__single_perturb_prefix_results_filename+model_noext+".log")
  os.remove(param_scan__single_perturb_prefix_results_filename+model_noext+".idx")
  os.remove(param_scan__single_perturb_prefix_results_filename+model_noext+".toc")
  os.remove(param_scan__single_perturb_prefix_results_filename+model_noext+".aux")
  
  os.chdir(currdir)
  print("DONE\n")

