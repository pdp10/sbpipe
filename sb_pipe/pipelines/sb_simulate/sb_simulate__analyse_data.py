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
# Object: Execute the model several times for deterministic or stochastical analysis
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 13:45:32 $




import os
import sys
import glob
from subprocess import Popen,PIPE

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))


# Input parameters
# model: read the model
# input_dir: the input dir
# results_dir: The results dir
# tc_dir: the time course dir
# tc_mean_dir: the mean time course dir
# tc_mean_with_exp_dir: the mean time course with experimental data dir
# simulate__xaxis_label : the x axis label
def main(model, input_dir, results_dir, tc_dir, tc_mean_dir, tc_mean_with_exp_dir, xaxis_label):   
  
  if not os.path.exists(input_dir): 
    print("ERROR: input_dir " + input_dir + " does not exist. Generate some data first.");
    return

  # folder preparation
  filesToDelete = glob.glob(os.path.join(results_dir, tc_dir, model+"*"))
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(os.path.join(results_dir, tc_mean_dir, model+"*"))    
  for f in filesToDelete:
    os.remove(f)
  filesToDelete = glob.glob(os.path.join(results_dir, tc_mean_with_exp_dir, model+"*")) 
  for f in filesToDelete:
    os.remove(f)

  if not os.path.exists(os.path.join(results_dir, tc_dir)):  
    os.mkdir(os.path.join(results_dir, tc_dir)) 
  if not os.path.exists(os.path.join(results_dir, tc_mean_dir)):  
    os.mkdir(os.path.join(results_dir, tc_mean_dir))
  if not os.path.exists(os.path.join(results_dir, tc_mean_with_exp_dir)):  
    os.mkdir(os.path.join(results_dir, tc_mean_with_exp_dir))


  print("Generating statistics from simulations:")
  process = Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines','sb_simulate','sb_simulate__plot_error_bars.r'), 
			      model, input_dir, 
			      os.path.join(results_dir, tc_mean_dir), 
			      os.path.join(results_dir, 'sim_stats_'+model+'.csv'), xaxis_label])
  process.wait() 


  #print("\nGenerating overlapping plots (sim + exp):")
  #process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines','sb_simulate','sb_simulate__plot_sim_exp_error_bars.r'), model, os.path.join(results_dir,tc_mean_dir), os.path.join(results_dir, tc_mean_exp_dir), os.path.join(results_dir, tc_mean_with_exp_dir), os.path.join(results_dir, 'sim_stats_'+model+'.csv'),  os.path.join(results_dir,'exp_stats_'+model+'.csv')])
  #process.wait() 

