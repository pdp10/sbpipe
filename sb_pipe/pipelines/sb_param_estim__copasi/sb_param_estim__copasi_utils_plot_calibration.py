#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $



# command:
# ./plot_calibration.py folder rscript_folder

import sys
import os
SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))

from PlotCalibration import *



# INITIALIZATION
# folder : the folder containing the data to process
# rscript_folder : the rscript folder
def main(folder, rscript_folder):
  print("Plot the calibration results as an Iteration-MSE function") 
  #pools = [ "small_values_config", "medium_values_config", "large_values_config" ]
  pools = [ "estimation error" ]
  colours = ["black", "blue", "green", "orange", "brown", "red", "purple"]
  plot_calibration(rscript_folder, folder, pools, colours)

