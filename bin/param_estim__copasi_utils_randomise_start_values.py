#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
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
#
# Institute for Ageing and Health
# Newcastle University
# Newcastle upon Tyne
# NE4 5PL
# UK
# Tel: +44 (0)191 248 1106
# Fax: +44 (0)191 248 1101
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $


# It randomizes the start values of the parameters to estimate from a template Copasi file and saves the new files. 
# As input, it receives the number of files to generate (multiple calibrations)


import sys
import os
PROJ_LIB = os.environ["PROJ_LIB"]
sys.path.append(PROJ_LIB + "/python/")

from ParamEstim_RandomizeStartValue import *


def main(args):
  print("\nTool for generating COPASI files, from a COPASI file configured for parameter estimation task,\nin which the parameters to estimate have random start values - by Piero Dalle Pezze\n") 
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



