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


# Collect the estimated parameters from the results of a parameter estimation task using Copasi

import sys
import os
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")

from ParamEstim_CollectResults import *
 
  
def main(args):
  print("\nCollect the estimated parameters from the results of a parameter estimation task using Copasi - by Piero Dalle Pezze\n") 
  # INITIALIZATION
  # 1 input parameters 
  # The path containing COPASI parameter estimation reports
  path = args[0]
  
  filename_out = "/parameter_estimation_collected_results.csv"
  post_param_estim = ParamEstim_CollectResults()
  post_param_estim.collect_results(path, filename_out)


main(sys.argv[1:])


