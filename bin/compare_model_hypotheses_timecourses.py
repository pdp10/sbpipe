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

import sys
import os
PROJ_LIB = os.environ["PROJ_LIB"]
sys.path.append(PROJ_LIB + "/python/")
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
  # The input folder containing the models results (e.g. $project/simulations/ ) 
  input_dir = args[0]
  # the output folder containing the comparative results (e.g. $project/simulations/hp_comparison/ )
  output_dir = args[1]

  models = ['mtor_model_0_8_5_0_tsc_dep_model', 
	    'mtor_model_0_8_5_0_pi3k_dep_model', 
	    'mtor_model_0_8_5_0_pi3k_indep_model',
	    'mtor_model_0_8_5_0_pi3k_variant_dep_model']
  input_dirs = [ input_dir + '/' + models[0] + '/tc_mean_with_exp/', input_dir + '/' + models[1] + '/tc_mean_with_exp/', input_dir + '/' + models[2] + '/tc_mean_with_exp/', input_dir + '/' + models[3] + '/tc_mean_with_exp/' ]
  folders = [ os.listdir(input_dirs[0]), os.listdir(input_dirs[1]), os.listdir(input_dirs[2]), os.listdir(input_dirs[3]) ]
  # Sort and clean files in folders
  preprocess_comparison_3hp(folders)
  #print(len(folders[0]))
  #print("\n")
  #print(len(folders[1]))
  #print("\n")
  #print(len(folders[2]))
  #print(folders[0])
  #print("\n")
  #print(folders[1])
  #print("\n")
  #print(folders[2])
  #exit()
  # A lookup table for computational-experimental comparison
  names_table = [ 'IR_beta_pY1146', 'Akt_pT308', 'Akt_pT308_pS473',
		  'mTORC2_pS2481', 'mTORC1_pS2448', 'PRAS40_pT246',
		  'PRAS40_pS183', 'p70S6K_pT389', 
  #		'IRS1_negative_feedback']
		  'IRS1_pS636_PI3K']
  #names_table = [ 'IR_beta_pY1146', 'Akt_pT308_PIP3_clx', 'Akt_pT308_pS473_PIP3_clx',
		  #'mTORC2_pS2481', 'mTORC1_pS2448', 'mTORC1_PRAS40_pT246_clx',
		  #'mTORC1_PRAS40_pS183_pT246_clx', 'p70S6K_pT389', 
  ##		'IRS1_negative_feedback']
		  #'IRS1_pS636']		
				  
  compare_model_hypotheses_timecourses(output_dir, folders, models, names_table)


main(sys.argv[1:])