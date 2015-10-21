#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either model_noext 2 of the License, or (at
# your option) any later model_noext.
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
from func_latex import *





def main(args):
  print("Tool for autogenerating latex file containing graphs - by Piero Dalle Pezze\n") 
  # INITIALIZATION
  # The model_noext of the model
  model_noext = args[0]
  results_dir = args[1]
  tc_mean_dir = args[2]
  simulate__prefix_results_filename = args[3]
  print(model_noext)
  # A lookup table for computational-experimental comparison
  #names_table = [ 'IR_beta_pY1146', 'Akt_pT308', 'Akt_pT308_pS473',
#		  'mTORC2_pS2481', 'mTORC1_pS2448', 'PRAS40_pT246',
#		  'PRAS40_pS183', 'p70S6K_pT389', 
  #		'IRS1_negative_feedback']
#		  'IRS1_pS636_PI3K']
  #names_table = [ 'IR_beta_pY1146', 'Akt_pT308_PIP3_clx', 'Akt_pT308_pS473_PIP3_clx',
		  #'mTORC2_pS2481', 'mTORC1_pS2448', 'mTORC1_PRAS40_pT246_clx',
		  #'mTORC1_PRAS40_pS183_pT246_clx', 'p70S6K_pT389', 
  ##		'IRS1_negative_feedback']
		  #'IRS1_pS636']

  latex_report(results_dir, tc_mean_dir, model_noext, simulate__prefix_results_filename)


main(sys.argv[1:])