#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Run CopasiSE performing a parameter scan.
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-24 13:14:32 $


import os, sys
import glob
import subprocess
import shutil

# For reading the first N lines of a file.
from itertools import islice


SB_PIPE = os.environ["SB_PIPE"]


# INITIALIZATION
# model
# scanned_species 
# param_scan__single_perturb_knock_down_only
# results_dir
# raw_sim_data
# tc_parameter_scan_dir
# simulate__xaxis_label
# param_scan__single_perturb_simulations_number
# param_scan__single_perturb_perturbation_in_percent_levels
# min_level
# max_level
# levels_number
def main(model, scanned_species, param_scan__single_perturb_knock_down_only, results_dir, 
	 raw_sim_data, tc_parameter_scan_dir, simulate__xaxis_label, 
	 param_scan__single_perturb_simulations_number, 
	 param_scan__single_perturb_perturbation_in_percent_levels, 
	 min_level, max_level, levels_number):


  if not os.path.exists(os.path.join(results_dir,raw_sim_data)): 
    print("ERROR: input_dir " + os.path.join(results_dir,raw_sim_data) + " does not exist. Generate some data first.");
    return
  
    # some control
  if int(min_level) < 0: 
    print("\n ERROR: min_level MUST BE non negative ")
    return
  
  if int(max_level) < 100: 
    print("\n ERROR: max_level MUST BE greater than 100 ")
    return  
  

  # folder preparation
  filesToDelete = glob.glob(os.path.join(results_dir,tc_parameter_scan_dir,model+"*"))
  for f in filesToDelete:
    os.remove(f)
  if not os.path.exists(os.path.join(results_dir, tc_parameter_scan_dir)):
    os.mkdir(os.path.join(results_dir, tc_parameter_scan_dir)) 


  process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE, 'sb_pipe','pipelines','sb_param_scan__single_perturb','sb_param_scan__analyse_data.r'), 
			      model, scanned_species, param_scan__single_perturb_knock_down_only, results_dir, raw_sim_data, tc_parameter_scan_dir, simulate__xaxis_label, 
			      param_scan__single_perturb_simulations_number, param_scan__single_perturb_perturbation_in_percent_levels, 
			      str(min_level), str(max_level), str(levels_number)])    
  process.wait()

