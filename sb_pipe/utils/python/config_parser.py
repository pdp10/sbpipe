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
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-26 10:02:32 $



import sys
import logging
logger = logging.getLogger('sbpipe')

from ConfigParser import ConfigParser
from StringIO import StringIO




def config_parser(config_file, section):
  parser = ConfigParser()

  with open(config_file) as stream:
    stream = StringIO(stream.read())    
    parser.readfp(stream)     
  
  if section == 'simulate':
    return parse_simulate_section(parser.items(section))

  elif section == 'single_param_scan':
    return parse_single_param_scan_section(parser.items(section))

  elif section == 'double_param_scan':
    return parse_double_param_scan_section(parser.items(section))

  elif section == 'param_estim':
    return parse_param_estim_section(parser.items(section))
  
  elif section == 'sensitivity':
    return parse_sensitivity_section(parser.items(section))  

  else:
    raise Exception("Pipeline '" + section + "' not recognised " +
		    "by sb_pipe configuration parser.")
 
 
  


def parse_simulate_section(lines):
  
  # parse copasi common options
  (generate_data, analyse_data, generate_report,
      project_dir, model, copasi_reports_path) = parse_copasi_commons(lines)
  
  # default values
  # The parallel mechanism to use (pp | sge | lsf).
  cluster="pp"
  # The number of cpus for pp
  pp_cpus=1
  # The number of jobs to be executed
  runs=1  
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"
  
  # Initialises the variables
  for line in lines:
    logger.info(line)
    if line[0] == "cluster": 
      cluster = line[1] 
    elif line[0] == "pp_cpus": 
      pp_cpus = line[1] 
    elif line[0] == "runs": 
      runs = line[1]      
    elif line[0] == "simulate__xaxis_label":
      simulate__xaxis_label = line[1]
      
  return (generate_data, analyse_data, generate_report,
	  project_dir, model, copasi_reports_path, 
	  cluster, pp_cpus, runs, 
	  simulate__xaxis_label)





def parse_single_param_scan_section(lines):

  # parse copasi common options
  (generate_data, analyse_data, generate_report,
      project_dir, model, copasi_reports_path) = parse_copasi_commons(lines)  
  
  # default values  
  # The model species to scan (e.g. mTORC1)
  scanned_species=""
  # The number of intervals for one simulation
  simulate__intervals=100  
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"
  # The number of simulations (e.g. 1 for deterministic simulations, n for stochastic simulations)
  single_param_scan_simulations_number=1
  # The scanning is performed on percent levels (true) or through a modelled inhibitor/expressor (false)
  single_param_scan_percent_levels=False
  # if True then, plot only kd (blue), otherwise plot kd and overexpression
  single_param_scan_knock_down_only=True
  # The number of levels of inhibition/over-expression
  levels_number=10  
  # minimum level
  min_level=0
  # maximum level
  max_level=250
  # True if lines should have the same colour, no linetype, no legend. 
  # Useful for scanning from a confidence interval
  # If this is true, it overrides:
  # - single_param_scan_percent_levels and 
  # - single_param_scan_knock_down_only
  homogeneous_lines=False
  
  # Initialises the variables
  for line in lines:
    logger.info(line)
    if line[0] == "scanned_species": 
      scanned_species = line[1]
    elif line[0] == "simulate__intervals": 
      simulate__intervals = line[1]       
    elif line[0] == "simulate__xaxis_label": 
      simulate__xaxis_label = line[1]
    elif line[0] == "single_param_scan_simulations_number": 
      single_param_scan_simulations_number = line[1] 
    elif line[0] == "single_param_scan_percent_levels": 
      single_param_scan_percent_levels = {'True': True, 'False': False}.get(line[1], False)
    elif line[0] == "single_param_scan_knock_down_only": 
      single_param_scan_knock_down_only = {'True': True, 'False': False}.get(line[1], False)      
    elif line[0] == "min_level": 
      min_level = line[1]       
    elif line[0] == "max_level": 
      max_level = line[1]
    elif line[0] == "levels_number": 
      levels_number = line[1]          
    elif line[0] == "homogeneous_lines": 
      homogeneous_lines = {'True': True, 'False': False}.get(line[1], False)
  
  return (generate_data, analyse_data, generate_report, 
	  project_dir, model, scanned_species, copasi_reports_path, 
	  simulate__intervals, simulate__xaxis_label, 
	  single_param_scan_simulations_number, single_param_scan_percent_levels, 
	  single_param_scan_knock_down_only, levels_number, min_level, max_level, 
	  homogeneous_lines)
  


def parse_double_param_scan_section(lines):
  # parse copasi common options
  (generate_data, analyse_data, generate_report,
      project_dir, model, copasi_reports_path) = parse_copasi_commons(lines)
  
  # Initialises the variables
  for line in lines:
    break

  return (generate_data, analyse_data, generate_report,
      project_dir, model, copasi_reports_path)




def parse_param_estim_section(lines):
  
  # parse copasi common options
  (generate_data, analyse_data, generate_report,
      project_dir, model, copasi_reports_path) = parse_copasi_commons(lines)  
  
  # default values  
  # The parallel mechanism to use (pp | sge | lsf).
  cluster="pp"
  # The number of cpus for pp
  pp_cpus=1
  # The parameter estimation round 
  round=1
  # The number of jobs to be executed
  runs=25
  # The percent of best fits to consider
  best_fits_percent=100
  # The number of available data points
  data_point_num=10
  # Plot 2D correlations using data from 66% or 95% confidence levels
  # This can be very time/memory consuming
  plot_2d_66_95cl_corr=False

  # Initialises the variables
  for line in lines:
    logger.info(line)
    if line[0] == "generate_tarball":
      generate_tarball = {'True': True, 'False': False}.get(line[1], False)      
    elif line[0] == "cluster":
      cluster = line[1]      
    elif line[0] == "round":
      round = line[1]       
    elif line[0] == "runs":
      runs = line[1] 
    elif line[0] == "pp_cpus": 
      pp_cpus = line[1]
    elif line[0] == "best_fits_percent": 
      best_fits_percent = line[1]
    elif line[0] == "data_point_num": 
      data_point_num = line[1]
    elif line[0] == "plot_2d_66_95cl_corr":
      plot_2d_66_95cl_corr = {'True': True, 'False': False}.get(line[1], False)
      
  return (generate_data, analyse_data, generate_report, generate_tarball, 
	  project_dir, model, copasi_reports_path, cluster, pp_cpus, 
	  round, runs, best_fits_percent, data_point_num, plot_2d_66_95cl_corr)
      



def parse_sensitivity_section(lines):
  # parse copasi common options 
  (generate_data, analyse_data, generate_report,
	  project_dir, model, copasi_reports_path) = parse_copasi_commons(lines)
    
  # Initialises the variables
  for line in lines:
    break
      
  return (generate_data, analyse_data, generate_report,
	  project_dir, model, copasi_reports_path)




def parse_copasi_commons(lines):
  
  # default values
  # Boolean
  generate_data=True
  # Boolean
  analyse_data=True
  # Boolean
  generate_report=True
  # the project directory
  project_dir=""
  # The Copasi model
  model="mymodel.cps"
  # The path to Copasi reports
  copasi_reports_path="tmp"
  
  # Initialises the variables
  for line in lines:
    logger.info(line)
    if line[0] == "generate_data":
      generate_data = {'True': True, 'False': False}.get(line[1], False)     
    elif line[0] == "analyse_data":
      analyse_data = {'True': True, 'False': False}.get(line[1], False)     
    elif line[0] == "generate_report":
      generate_report = {'True': True, 'False': False}.get(line[1], False)           
    elif line[0] == "project_dir":
      project_dir = line[1] 
    elif line[0] == "model": 
      model = line[1] 
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]
      
  return (generate_data, analyse_data, generate_report,
	  project_dir, model, copasi_reports_path)
