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
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $

import sys
import os
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")
import glob
import csv
import shlex, subprocess
from func_latex import *



# sort by string considering the locale
import locale
# this reads the environment and inits the right locale
locale.setlocale(locale.LC_ALL, "")
# alternatively, (but it's bad to hardcode)
# locale.setlocale(locale.LC_ALL, "sv_SE.UTF-8")



def main(args):
  print("Tool for autogenerating latex file containing graphs for parameter scan - by Piero Dalle Pezze\n")
  # INITIALIZATION
  model = 'mtor_model_0_8_6_0_FEBS_model'
  path = args[0]
  # Obtain the specie's name
  species = [ '_only_PI3K_level_', '_only_mTOR_level_', '_comb_PI3K_mTOR_level_' ]
  path = path + '/' + model + '/tc_parameter_scan/'
  folder = os.listdir(path)
  folder.sort(cmp=locale.strcoll)
  plots = [ [], [], [] ]
  # Remove unknown_mTORC2_activ and PI3K_like from folders[0] and folders[1]
  #folders[0][:] = (value for value in folders[0] if value.find("unknown_mTORC2_activ") == -1)
  # Consider only the specie
  for i in range(0, len(species)):
    plots[i][:] = (value for value in folder if value.find(species[i]) != -1)
  print(plots[0])
  print(plots[1])
  print(plots[2])

  plot_inhibitors_comparison(model, plots)


main(sys.argv[1:])
