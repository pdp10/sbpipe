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
  print("Tool for autogenerating latex file containing graphs for parameter scan- by Piero Dalle Pezze\n") 
  # INITIALIZATION
  # The perturbated species
  species = args[0]
  # The input folder containing the models results (e.g. $project/simulations/ ) 
  input_dir = args[1]
  # the output folder containing the comparative results (e.g. $project/simulations/hp_comparison/ )
  output_dir = args[2]
  models = ['mtor_model_0_8_5_0_tsc_dep_model', 
	    'mtor_model_0_8_5_0_pi3k_dep_model', 
	    'mtor_model_0_8_5_0_pi3k_indep_model',
	    'mtor_model_0_8_5_0_pi3k_variant_dep_model']
  input_dirs = [ input_dir + '/' + models[0] + '/tc_parameter_scan/', input_dir + '/' + models[1] + '/tc_parameter_scan/', input_dir + '/' + models[2] + '/tc_parameter_scan/', input_dir + '/' + models[3] + '/tc_parameter_scan/' ]
  folders = [ os.listdir(input_dirs[0]), os.listdir(input_dirs[1]), os.listdir(input_dirs[2]), os.listdir(input_dirs[3]) ]
  # Sort and clean files in folders
  preprocess_comparison(folders)
  # Consider only the species
  for i in range(0, len(models)):
    folders[i][:] = (value for value in folders[i] if value.find(species) != -1)
  #print(len(folders[0]))
  #print("\n")
  #print(len(folders[1]))
  #print("\n")
  #print(len(folders[2]))
  #exit()

  compare_model_hypotheses(output_dir, folders, models, species)

main(sys.argv[1:])