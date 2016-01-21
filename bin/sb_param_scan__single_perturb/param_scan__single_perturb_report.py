#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either model_noext 2 of the License, or (at
# your option) any later model_noext.
#    
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
# Object: Autogeneration of latex code containing images
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: param_scan__single_perturb_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $

import sys
import os
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")
import glob
import csv
from single_model_latex_reports import latex_report_par_scan




def main(args):
  print("Generating a LaTeX report containing graphs\n") 
  # INITIALIZATION
  # The model_noext of the model
  model_noext = args[0]
  species = args[1]
  results_dir = args[2]
  tc_parameter_scan_dir = args[3]
  param_scan__single_perturb_prefix_results_filename = args[4]
  tc_parameter_scan_dir = args[5]
  param_scan__single_perturb_legend = args[6]
  latex_report_par_scan(results_dir, tc_parameter_scan_dir, param_scan__single_perturb_prefix_results_filename, model_noext, species, param_scan__single_perturb_legend)


main(sys.argv[1:])