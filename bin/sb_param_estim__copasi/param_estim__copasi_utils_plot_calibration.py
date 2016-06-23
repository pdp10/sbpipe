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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $



# command:
# ./plot_calibration.py folder rscript_folder

import sys
import os
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")

from PlotCalibration import *




def main(args):
  print("\nPlot the calibration results as an Iteration-MSE function\n") 
  # INITIALIZATION
  #folder = "../results/calibration/"
  #rscript_folder = "../results/"    # "./"
  folder = args[0]
  rscript_folder = args[1]
  
  #pools = [ "small_values_config", "medium_values_config", "large_values_config" ]
  pools = [ "estimation error" ]
  colours = ["black", "blue", "green", "orange", "brown", "red", "purple"]
  plot_calibration(rscript_folder, folder, pools, colours)

main(sys.argv[1:])  