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
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]


# Input parameters
# model: read the model
# input_dir: the input dir
# outputdir: The results dir
# sim_plots_folder: The folder containing the plots
# xaxis_label : the x axis label
def main(model, input_dir, outputdir, sim_plots_folder, xaxis_label):   
  
  if not os.path.exists(input_dir): 
    logger.error("input_dir " + input_dir + " does not exist. Generate some data first.");
    return

  # folder preparation
  filesToDelete = glob.glob(os.path.join(outputdir, sim_plots_folder, model+"*"))    
  for f in filesToDelete:
    os.remove(f)

  if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):  
    os.mkdir(os.path.join(outputdir, sim_plots_folder))

  logger.info("Generating statistics from simulations:")
  process = Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines','simulate','simulate__plot_error_bars.r'), 
			      model, input_dir, 
			      os.path.join(outputdir, sim_plots_folder), 
			      os.path.join(outputdir, 'sim_stats_'+model+'.csv'), xaxis_label])
  process.wait() 


  #logger.info("\nGenerating overlapping plots (sim + exp):")
  #process = subprocess.Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines','simulate','simulate__plot_sim_exp_error_bars.r'), model, os.path.join(outputdir,sim_plots_folder), os.path.join(outputdir, tc_mean_exp_dir), os.path.join(outputdir, tc_mean_with_exp_dir), os.path.join(outputdir, 'sim_stats_'+model+'.csv'),  os.path.join(outputdir,'exp_stats_'+model+'.csv')])
  #process.wait() 

