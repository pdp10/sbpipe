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


# Collect the estimated parameters from the results of a parameter estimation task using Copasi

import sys
import os
SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from ParamEstim_CollectResults import retrieve_final_estimates
from ParamEstim_CollectResults import retrieve_all_estimates


 
# INITIALIZATION
# path_in : The path containing COPASI parameter estimation reports
# path_out : The path to store filename_out
# fileout_final_estims : the file name of the final estimations
# fileout_all_estims : the file name of all estimations
def main(path_in, path_out, fileout_final_estims, fileout_all_estims):
  print("Collect results from multiple parameter estimations") 
  retrieve_final_estimates(path_in, path_out, fileout_final_estims)
  retrieve_all_estimates(path_in, path_out, fileout_all_estims)

