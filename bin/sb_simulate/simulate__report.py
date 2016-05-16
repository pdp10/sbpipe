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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: simulate_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $

import sys
import os
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")
import glob
import csv
from single_model_latex_reports import latex_report





def main(args):
  print("Generating a LaTeX report containing graphs\n") 
  # INITIALIZATION
  # The model_noext of the model
  model_noext = args[0]
  results_dir = args[1]
  tc_mean_dir = args[2]
  simulate__prefix_results_filename = args[3]
  print(model_noext)
  latex_report(results_dir, tc_mean_dir, model_noext, simulate__prefix_results_filename)


main(sys.argv[1:])