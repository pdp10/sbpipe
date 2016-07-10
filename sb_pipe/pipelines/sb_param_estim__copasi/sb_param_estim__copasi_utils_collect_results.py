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
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $


# Collect the estimated parameters from the results of a parameter estimation task using Copasi

import sys
import os
SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))

from ParamEstim_CollectResults import *



 
# INITIALIZATION
# path_in : The path containing COPASI parameter estimation reports
# path_out : The path to store filename_out
# filename_out : the file name of the collected results
def main(path_in, path_out, filename_out):
  print("\nCollect results from multiple parameter estimations\n") 
  post_param_estim = ParamEstim_CollectResults()
  post_param_estim.collect_results(path_in, path_out, filename_out)

