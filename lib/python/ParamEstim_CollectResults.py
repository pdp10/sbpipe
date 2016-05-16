#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
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
    self._parameters.insert(0,'Calibration')
    self._parameters.insert(1,'Objective Value')
    self._parameters.insert(2,'Standard Deviation')
    self._parameters.insert(3,'Root Mean Square')
    self._parameters.insert(4,'Sum Square Distance (by Block)')
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
    fd = open(filein, 'r')
    if os.path.isfile(filein):
      lines = fd.readlines()
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
    fd.close()


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
    names = ['Objective Function Value:','Standard Deviation:','Root Mean Square:']
    for filein in self._files:
      completed = False
      file_num = file_num + 1
      fd = open(filein, 'r')
      print("\tProcessing file: " + filein)
      if os.path.isfile(filein):
	lines = fd.readlines()
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
	      self._data[file_num + 1][param_num + 4] = str(split_result[2])
	  # Retrieve the objective function value, standard deviation, root mean square	      
	  for idx in range(0,len(names)):
	    if len(split_line) > 1 and split_line[0] == names[idx]:
	      self._data[file_num + 1][idx + 1] = str(split_line[1][:-2])
	      if idx == len(names) - 1:
		completed = True
	  if completed:
	    break
      fd.close()
    self._write_aux_data()

   
  # Add the statistics of one block of calibration results. A block of calibration 
  # is a group which converged to the same solution
  def _add_calib_set_statistics(self, names, statistics, block=0):
    # Add Mean + stdev of the best group
    offset = 8 * block
    nfiles = len(self._files)
    # Add a group of statistics to the tail of the matrix
    names_len = len(names)
    # Write the statistics
    for idx in range(0, names_len):
      self._data[1 + nfiles + offset + 2 + idx][0] = names[idx]
      self._data[1 + nfiles + offset + 2 + idx][1] = self._get_calib_name(col=idx + 1, value=str(statistics[idx][block]))
      self._data[1 + nfiles + offset + 2 + idx][2] = str(statistics[idx][block])
      self._data[1 + nfiles + offset + 2 + idx][3] = str(float(self._count_instances(idx + 1, statistics[idx][block]))/float(nfiles)*100) + "%"    
    self._data[1 + nfiles + offset + 2 + names_len - 1][4] = "Parameter Means"
    self._data[1 + nfiles + offset + 2 + names_len][4] = "Parameter Standard Deviations"
    for i in range(0, len(self._parameters) - 5):
      vect = []
      for j in range(0, nfiles):
        # Add only group (test by RMS)
        if self._data[1+j][3].find(str(statistics[2][block])) != -1:
          vect.append(float(self._data[j+1][i+5]))
      self._data[1 + nfiles + offset + 2 + names_len - 1][i+5] = str(numpy.mean(vect))
      self._data[1 + nfiles + offset + 2 + names_len][i+5] = str(numpy.std(vect))         
      

  # Compute the Sum Square Difference between the parameter and the mean of the parameters
  # looking at the right group of calibration
  # SSD definition: ssd_i = (calib(param_i) - mean_i)^2
  # SSD is scaled by n_parameters
  def _compute_ssd(self, row, offset):
    ssd = 0.0
    nparam = len(self._parameters) - 5
    for i in range(0, nparam):
	ssd = ssd + (float(self._data[row][i+5]) - float(self._data[1+len(self._files) + offset + 4][i+5]))**2
    if nparam == 0:
      nparam = 1 
    return ssd / float(nparam)
    
  # Add the Sum of Square Distance line for a block of calibrations using the vector of RMS
  def _compute_ssd_block(self, rms_block, block):
    vect_ssd = []
    nfiles = len(self._files)
    offset = 8 * block
    for j in range(0, nfiles):
      # Add only if belonging to the block of calibrations
      if self._data[j+1][3].find(str(rms_block)) != -1:
	ssd = self._compute_ssd(j+1, offset)
	vect_ssd.append(ssd)
	self._data[1+j][4] = str(ssd)	
    minimum_ssd = min(vect_ssd)
    calib_name = self._get_calib_name(4, minimum_ssd)
    self._data[1 + nfiles + offset + 5][0] = "Minimum Sum Square Distance"
    if minimum_ssd > 0.0: 
      if block + 1 < 10:
      # Add (*..*) to the best calibration for each group
	calib_name = calib_name + "("
	for j in range(0, block + 1):
	  calib_name = calib_name + "*"
	calib_name = calib_name + ")"
      self._data[1 + nfiles + offset + 5][1] = calib_name # This is labelled! :D
    else:
      # Only one calibration has this RMS
      self._data[1 + nfiles + offset + 5][1] ="Not Appliable (=> 1 calib)" # This is labelled! :D
    self._data[1 + nfiles + offset + 5][2] = str(minimum_ssd)  	
    self._data[1 + self._get_calib_index(4, minimum_ssd)][0] = calib_name # This is labelled! :D      
    count_ssd = self._count_instances(4, str(minimum_ssd))    
    self._data[1 + nfiles + offset + 5][3] = str(float(count_ssd)/float(len(self._files))*100) + "%"
    


  # Write Mean and standard Deviation of the parameters, plus the tail of the matrix
  def _write_aux_data(self):
    names = ["Objective Value","Standard Deviation","Root Mean Square"]
    # Retrieve the objective values,std dev, rms.
    (indexes, vect_rms) = self._get_col_no_rep(3)
    vect_obj = self._get_col_values(1, indexes)
    vect_std = self._get_col_values(2, indexes)
    summary = (vect_obj, vect_std, vect_rms)
    
    #print(summary)
    #print(len(vect_obj))
    #print(len(vect_std))
    #print(len(vect_rms))    
    ## Extend the matrix: add 8 rows (of (self._parameters) columns) for each retrieved objective value
    self._data = self._data + [[""] * len(self._parameters) for i in range(8 * len(vect_obj))]
    self._data[1 + len(self._files) + 1][0] = "Statistical Measure"
    self._data[1 + len(self._files) + 1][1] = "Best Calibration"
    self._data[1 + len(self._files) + 1][2] = "Value"  
    self._data[1 + len(self._files) + 1][3] = "% Subset"
    ## Add statistics for each group of calibrations selected by RMS
    for i in range(0,len(vect_obj)):
      self._add_calib_set_statistics(names, summary, i)
      self._compute_ssd_block(vect_rms[i], i)




  #####################
  ### UTILITY METHODS 
  #####################

  # Return a sorted array containing the values of a column without repetitions
  def _get_col_no_rep(self, col):
    vect = []
    indexes = [] 
    # a list of list [[item, index]..]. This way the final sort function results trivial
    container = []
    item = 0.0
    for i in range(0, len(self._files)):      
      item = float(self._data[1+i][col])
      # Prevent numerical approximations which can introduce errors. e.g. 3.12345 and 3.1234, it selects 3.1234      
      found = False
      for j in range(0, len(container)):	
	if str(item).find(str(container[j][0])) != -1:
	  # The new value item is longer
	  found = True
	  break
	elif str(container[j][0]).find(str(item)) != -1:
	  # The new value item is shorter
	  container[j][0] = item
	  found = True
	  break
      if not found:
	container.append([item, self._data[1+i][0]])
    container.sort()
    for i in range(0,len(container)):
      vect.append(container[i][0])
      indexes.append(container[i][1])
    return (indexes,vect)
    
  # Return a sorted array containing the values of a column correspondent to a list of names (column 0)
  def _get_col_values(self, col, indexes):
    vect = []
    for i in range(0, len(indexes)):
      vect.append(self._data[1 + self._get_calib_index(0, indexes[i])][col])
    return vect
    

  # Return the first calibration name which matches with value, in column col
  def _get_calib_name(self, col, value):
    calib_name = ""
    item = ""
    for i in range(0, len(self._files)):
      item = self._data[1+i][col]
      if item.find(str(value)) != -1:      
	calib_name = self._data[1+i][0]
	break
    return calib_name

  # Return the first calibration index which matches with value, in column col. 
  # Note: It DOES NOT consider the header! 
  def _get_calib_index(self, col, value):
    item = ""
    index = -1
    for i in range(0, len(self._files)):
      item = self._data[1+i][col]
      if item.find(str(value)) != -1:      
	index = i
	break
    return index

  # Return the number of instances which match value in column col
  def _count_instances(self, col, value):
    count = 0
    for i in range(0, len(self._files)):
      item = self._data[1+i][col]      
      if item.find(str(value)) != -1:
        count = count + 1
    return count
    
