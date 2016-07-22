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
from subprocess import Popen,PIPE
import logging
logger = logging.getLogger('sbpipe')

SB_PIPE = os.environ["SB_PIPE"]
from collect_results import retrieve_final_estimates
from collect_results import retrieve_all_estimates



# Input parameters
# input_dir, results_dir, fileout_final_estims, fileout_all_estims, fileout_conf_levels, plots_dir, best_fits_percent, data_point_num
def main(input_dir, results_dir, fileout_final_estims, fileout_all_estims, fileout_approx_ple_stats, fileout_conf_levels, plots_dir, best_fits_percent, data_point_num, plot_2d_66_95cl_corr=False):

  if not os.path.exists(input_dir) or not os.listdir(input_dir): 
    logger.error("input_dir " + input_dir + " does not exist or is empty. Generate some data first.");
    return
  
  if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
  
  logger.info("Collect results:")
  # Collect and summarises the parameter estimation results
  retrieve_final_estimates(input_dir, results_dir, fileout_final_estims)
  retrieve_all_estimates(input_dir, results_dir, fileout_all_estims)  

  logger.info("\n")
  logger.info("Plot results:")
  logger.info("\n")
  process = Popen(['Rscript',
		   os.path.join(SB_PIPE,'sb_pipe','pipelines', 'param_estim', 'main_final_fits_analysis.r'),
		   os.path.join(results_dir, fileout_final_estims),
		   plots_dir,
		   str(best_fits_percent)])
  process.wait()
  process = Popen(['Rscript', os.path.join(SB_PIPE,'sb_pipe','pipelines', 'param_estim', 'main_all_fits_analysis.r'), 
		   os.path.join(results_dir, fileout_all_estims), plots_dir, str(data_point_num), 
		   os.path.join(results_dir, fileout_approx_ple_stats), os.path.join(results_dir, fileout_conf_levels), str(plot_2d_66_95cl_corr)])
  process.wait()  
  