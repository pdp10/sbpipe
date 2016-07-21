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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-16 12:14:32 $

import sys
import os
import glob
from re_utils import *



# Collect the estimated parameters from the results of a parameter estimation task using Copasi 
# Collect the results in a file filename_out
def retrieve_final_estimates(path_in=".", path_out=".", filename_out="final_estimates.csv"):
  # The path containing the results .csv files
  path = path_in
  # The collection of .csv files
  files = retrieve_input_files(path)
  # List of estimated parameters
  colNames = get_parameter_names_list(files[0])
  colNames.insert(0,'Estimation')
  colNames.insert(1,'ObjectiveValue')
  write_parameter_names(colNames, path_out, filename_out)  
  write_final_estimates(files, path_out, filename_out)
  
  

# Collect all the estimates from the results of a parameter estimation task using Copasi 
# Collect the results in a file filename_out
def retrieve_all_estimates(path_in=".", path_out=".", filename_out="all_estimates.csv"):
  # The path containing the results .csv files
  path = path_in
  # The collection of .csv files
  files = retrieve_input_files(path)
  # List of estimated parameters
  colNames = get_parameter_names_list(files[0])
  colNames.insert(0,'ObjectiveValue')
  write_parameter_names(colNames, path_out, filename_out)
  write_all_estimates(files, path_out, filename_out)
  


# Retrieve input files
def retrieve_input_files(path):
  files = glob.glob(os.path.join(path, "*.csv"))
  files.sort(key=natural_keys)
  return files



# Return the list of parameter names
def get_parameter_names_list(filein = ""):
  parameters = []
  with open(filein, 'r') as file:
    lines = file.readlines()
    line_num = -1
    for line in lines:
      line_num = line_num + 1
      split_line = line.split('\t')    
      if len(split_line) > 2 and split_line[1] == 'Parameter' and split_line[2] == 'Value':
	# add to _data the parameter values
	for result in lines[line_num + 1:]:
	  split_result = result.split("\t")
	  # Check whether this is the last sequence to read. If so, break
	  if len(split_result) == 1 and split_result[0] == '\n':
	    break
	  parameters.append(str(split_result[1]))
	# Nothing else to do
	break
  return parameters



# Print the list of parameter names
def write_parameter_names(colNames, path_out, filename_out):
  with open(os.path.join(path_out, filename_out), 'w') as file:
    i = -1
    for param in colNames:
      i = i+1
      if i < len(colNames)-1:
	file.write(param + '\t')
      else:
	file.write(param + '\n')


def write_final_estimates(files, path_out, filename_out):
  file_num = -1
  print("\nCollecting results:")
  with open(os.path.join(path_out, filename_out), 'a') as fileout:      
    for filein in files:
      completed = False
      file_num = file_num + 1
      with open(filein, 'r') as file:      
	print(os.path.basename(filein))
	lines = file.readlines()
	entry = []
	line_num = -1	
	for line in lines:
	  finished = False
	  line_num = line_num + 1
	  split_line = line.rstrip().split('\t')
	  # Retrieve the estimated values of the _parameters
	  # Retrieve the objective function value
	  if len(split_line) > 1 and split_line[0] == 'Objective Function Value:':
	    entry.append(os.path.basename(filein))	    
	    entry.append(split_line[1].rstrip())
	    
	  if len(split_line) > 2 and split_line[1] == 'Parameter' and split_line[2] == 'Value':
	    param_num = 0
	    for result in lines[line_num + 1:]:
	      param_num = param_num + 1
	      split_result = result.split("\t")
	      if len(split_result) >= 0 and split_result[0] == "\n":
		# All the parameters are retrieved, then exit
		line = result
		split_line = split_result
		finished = True
		break
	      entry.append(str(split_result[2]))
	  if finished:
	    fileout.write('\t'.join(map(str, entry))+'\n')
	    break


def write_all_estimates(files, path_out, filename_out):
  file_num = -1
  #print("\nCollecting results:")
  with open(os.path.join(path_out, filename_out), 'a') as fileout:      
    for file in files:
      file_num = file_num + 1
      with open(file, 'r') as filein:      
	#print(os.path.basename(file))
	lines = filein.readlines()
	line_num = -1
	for line in lines:
	  line_num = line_num + 1
	  split_line = line.rstrip().split("\t")	
	  # Retrieve the estimated values of the parameters
	  if len(split_line) > 2 and split_line[0] == '[Function Evaluations]' and split_line[1] == '[Best Value]' and split_line[2] == '[Best Parameters]':
	    # add to data the parameter values
	    line_num = line_num + 1
	    if line_num < len(lines):
	      split_line = lines[line_num].replace("\t(", "").replace("\t)", "").rstrip().split("\t")
	    
	    while len(split_line) > 2:
	      for k in xrange(1, len(split_line)):
		if k < len(split_line)-1:
		  fileout.write(str(split_line[k]) + '\t')
		else:
		  fileout.write(str(split_line[k]) + '\n')
	      line_num = line_num + 1
	      if line_num < len(lines):
		split_line = lines[line_num].replace("\t(", "").replace("\t)", "").rstrip().split("\t")

	    break


  
