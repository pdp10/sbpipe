#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $


import sys, os, os.path, glob
from io_util_functions import *
from re_utils import *
import numpy

# Collect the estimated parameters from the results of a parameter estimation task using Copasi
class ParamEstim_CollectResults:

  # List of estimated parameters
  _parameters = []
  # A matrix (#_parameters + 1) x (#estimation_files + 1) collecting the results
  _data = [[]]
  # The path containing the results .csv files
  _path = ""
  # The collection of .csv files
  _files = []


# PUBLIC

  # Constructor
  def __init__(self):
    pass
 
 
  # Collect the results in a file filename_out
  def collect_results(self, path = "", filename_out = ""):
    self._parameters = []
    self._data = [[]]
    self._path = path
    self._files = []
    # Remove possible old outputfiles to not interfere with the input file retrieval
    fileout = path + filename_out
    if os.path.isfile(fileout):
	os.remove(fileout)
    self._retrieve_input_files()
    # (1) Take the first file and retrieve some information. Basically we need the parameters names  
    self._get_parameter_names_list(self._files[0])
    self.print_parameter_names()
    # Insert the header and tail
    self._parameters.insert(0,'Estimation')
    self._parameters.insert(1,'ObjectiveValue')
    # (2) Create a matrix
    self._create_matrix()
    # (3) Read all files in files
    print("\nCollecting results:")
    self._collect()
    self.print_collected_results()
    # (4) Write the matrix in a csv file as output
    write_matrix_on_file(path, filename_out, self._data)  
    

  # Print the list of parameter names
  def print_parameter_names(self):
    print("\nParameter Names:")
    for param in self._parameters:
      print("\t" + str(param))

  # Print the inner state of the matrix
  def print_collected_results(self):
    print("\nCollected results:")
    for line in self._data:
      print("\t" + str(line))


  # GET/SET methods
  # Return the list of estimated parameters
  def get_parameters_list():
    return self._parameters
  # Return a matrix (#_parameters + 1) x (#estimation_files + 1) collecting the results
  def get_results_matrix():
    return self._data
  # Return the path containing the results .csv files
  def get_path_str():
    return self._path
  # Return the collection of .csv files
  def get_results_files():
    return self._files


# PRIVATE


  # Return the list of parameter names
  def _get_parameter_names_list(self, filein = ""):
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
	    self._parameters.append(str(split_result[1]))
	  # Nothing else to do
	  break


  # Retrieve input files
  def _retrieve_input_files(self):
    self._files = glob.glob(self._path + "/*.csv")
    self._files.sort(key=natural_keys)


  # Create a matrix (1 + num_files) x (len(_parameters)) to contain the collected results
  def _create_matrix(self):
    rows, columns = (1 + len(self._files)), len(self._parameters)
    self._data = [[""] * columns for i in range(rows)]
    # Initialise first row with the names of the _parameters (plus 'Parameter' as header)
    for p in range(0, len(self._parameters)):
      self._data[0][p] = self._parameters[p]


  # Collect the results in a matrix
  def _collect(self):
    file_num = -1
    names = ['Objective Function Value:']
    for filein in self._files:
      completed = False
      file_num = file_num + 1
      with open(filein, 'r') as file:      
	print("\tProcessing file: " + filein)
	lines = file.readlines()
	line_num = -1
	for line in lines:
	  line_num = line_num + 1
	  split_line = line.split("\t")
	  # Retrieve the estimated values of the _parameters
	  if len(split_line) > 2 and split_line[1] == 'Parameter' and split_line[2] == 'Value':
	    # add to _data the parameter values
            self._data[file_num + 1][0] = filein[filein.rfind("/")+1:]  # "Calib" + str(file_num + 1)
	    param_num = 0
	    for result in lines[line_num + 1:]:
	      param_num = param_num + 1
	      split_result = result.split("\t")
              if len(split_result) >= 0 and split_result[0] == "\n":
                # All the parameters are retrieved, then exit
                line = result
                split_line = split_result
                break
	      self._data[file_num + 1][param_num + 1] = str(split_result[2])
	  # Retrieve the objective function value
	  for idx in range(0,len(names)):
	    if len(split_line) > 1 and split_line[0] == names[idx]:
	      self._data[file_num + 1][idx + 1] = split_line[1].rstrip()
	      if idx == len(names):
		completed = True
	  if completed:
	    break


