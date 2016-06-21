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


# It randomizes the start values of the parameters to estimate from a template Copasi file and saves the new files. 
# As input, it receives the number of files to generate (multiple calibrations)


import sys
import os
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")

from ParamEstim_RandomizeStartValue import *


def main(args):
  print("\nReplicate a Copasi file configured for parameter estimation and randomise the initial parameter values\n") 
  # INITIALIZATION
  # 3 input parameters 
  # The path containing COPASI template file configured for parameter estimation task
  path = args[0]
  # The name of this COPASI template file
  filename_in = args[1]
  # The number of files to generate from the previous COPASI template file
  num_files = int(args[2])
  
  pre_param_estim = ParamEstim_RandomizeStartValue(path, filename_in)
  pre_param_estim.print_parameters_to_estimate()
  pre_param_estim.generate_instances_from_template(num_files)

main(sys.argv[1:])



