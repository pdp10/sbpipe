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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $


import sys, os, os.path
from CopasiParser import *
from python_to_bash_utils import *
import shutil
import random
import shlex
from subprocess import * 


# It reads a copasi file configured for parameter estimation task, and randomize the starting values of the parameters to estimate. 
# Then, it saves the new file. As input, it receives the number of files to generate (multiple calibrations)
class ParamEstim_RandomizeStartValue:
  
  # A Copasi Object
  _copasi = None
  # Path containing the template Copasi file
  _path = ""
  # The name of the template Copasi file
  _filename_in = ""
  # The name of the template parameter estimation report
  _report_filename_template = ""
  # The list of lower bounds of the parameters
  _lower_bounds = [] 
  # The list of names of the parameters  
  _param_names = [] 
  # The list of start values of the parameters  
  _start_values = []
  # The list of upper bounds of the parameters  
  _upper_bounds = []


# PUBLIC

  def __init__(self, _path, _filename_in):
    self._copasi = CopasiParser()
    self._path = _path
    self._filename_in = _filename_in
    self._report_filename_template, self._lower_bounds, self._param_names, self._start_values, self._upper_bounds = self._copasi.retrieve_param_estim_values(self._path + "/" + self._filename_in)

  # Generate num_files files, in which the parameters to estimate have a random 
  # starting value chosen in the determined ammissible range for that parameter.
  def generate_instances_from_template(self, num_files):  
    for i in range(0, num_files):
      # initialise the names and generate the output file
      filename_out = self._filename_in[:-4] + str(i+1) + ".cps"
      report_filename = self._report_filename_template[:-4] + str(i+1) + ".csv"
      file_out = self._path + filename_out
      file_in = self._path + self._filename_in
      if os.path.isfile(file_out):
	os.remove(file_out)
      shutil.copy2(file_in, file_out)      
      # 1) RANDOMIZATION
      new__start_values, old_str, new_str = self._randomise_start_value()
      # 2) PRINT NEW VALUES
      print("\nInitial parameters for the output file: " + file_out)      
      self._print_parameters_to_estimate2(new__start_values)
      # 3) REPLACE VALUES IN THE NEW FILE
      self._replace_start_value_in_file(file_out, report_filename, old_str, new_str)


  # Print the values extracted from COPASI template file
  def print_parameters_to_estimate(self):
    print("\t\tLowerBound\t\tStartValue\t\tUpperBound\t\tParameterName")
    print("\t\t==========\t\t==========\t\t==========\t\t=============")
    for i in range(0, len(self._param_names)):
      print("\t\t" + self._lower_bounds[i] + "\t\t" + self._start_values[i] + "\t\t" + 
      self._upper_bounds[i] + "\t\t" + self._param_names[i][self._param_names[i].find("[")+1:self._param_names[i].find("]")])


  def update_model(self, _path, _filename_in):
    self._copasi = CopasiParser()
    self._path = _path
    self._filename_in = _filename_in
    self._report_filename_template, self._lower_bounds, self._param_names, self._start_values, self._upper_bounds = self._copasi.retrieve_param_estim_values(self._path + "/" + self._filename_in)


  # SET/GET methods
  # Return the Copasi Object
  def get_copasi_obj():
    return self._copasi
  # Return the path containing the template Copasi file
  def get_path():
    return self._path
  # Return the name of the template Copasi file
  def get_template_copasi_file():
    return self._filename_in
  # Return the name of the template parameter estimation report
  def get_report_filename_template_str():
    return self._report_filename_template
  # Return the list of lower bounds of the parameters
  def get_lower_bounds_list():
    return self._lower_bounds 
  # Return the list of names of the parameters  
  def get_param_names_list():
    return self._param_names 
  # Return the list of start values of the parameters  
  def get_start_values_list():
    return self._start_values
  # Return the list of upper bounds of the parameters  
  def get_upper_bounds_list():
    return self._upper_bounds




# PRIVATE

  # Print the values extracted from COPASI template file and the new random start value
  def _print_parameters_to_estimate2(self, new__start_values):
    print("\t\tLowerBound\t\tStartValue\t\tNEWStartValue\t\tUpperBound\t\tParameterName")
    print("\t\t==========\t\t==========\t\t=============\t\t==========\t\t=============")
    for i in range(0, len(self._param_names)):
      print("\t\t" + self._lower_bounds[i] + "\t\t" + self._start_values[i] + "\t\t" + 
      new__start_values[i] + "\t\t" + self._upper_bounds[i] + "\t\t" + self._param_names[i][self._param_names[i].find("[")+1:self._param_names[i].find("]")])


  # Randomise the start value of the parameters
  def _randomise_start_value(self):
    print("\nRandomize parameter starting values and generate new COPASI files")
    new__start_values = []
    old_str = []
    new_str = []
    # Randomize the starting values using the respective lower and upper bounds using a uniform distibution
    for i in range(0, len(self._param_names)):
      if(str(self._lower_bounds[i].find("CN=Root,Model=") != -1) or str(self._upper_bounds[i].find("CN=Root,Model=") != -1)):
	# Either the lower or the upper bound is a variable. Fix a random value in [1e-05,1]
	new__start_values.append(str(random.uniform(0.00001, 1)))
      else:
	# The lower and the upper bounds are constants
	new__start_values.append(str(random.uniform(float(self._lower_bounds[i]), float(self._upper_bounds[i]))))
      old_str.append('<Parameter name="StartValue" type="float" value="' + self._start_values[i] + '"\/>')
      new_str.append('<Parameter name="StartValue" type="float" value="' + new__start_values[i] + '"\/>')
      #print(old_str[i])
      #print(new_str[i])
    return new__start_values, old_str, new_str


  # For each parameter to estimate, replace the current start value with the new randomised start value
  def _replace_start_value_in_file(self, file_out, report_filename, old_str, new_str):
    # Attention: Popen with shell=True, launches a child process in parallel. This is not good in such a case. 
    # NOTE: .wait() is temporarily added in order to wait for the child to terminate before going on.
    Popen('sed -i \'s/' + self._report_filename_template + '/' + report_filename + '/g\' ' + file_out, shell=True).wait()
    #print('sed -i \'s/' + _report_filename_template + '/' + report_filename + '/g\' ' + file_out)  
    for i in range(0, len(self._param_names)):
      # Check whether the replacement of the parameter start value is exactly for the parameter estimation task 
      # and for the corresponding parameter name. So, if different parameters have same start values, the algorithm 
      # replaces only the value for the corresponding parameter and not to all the instances with equal start value.
      # (A) Retrieve the line number of the current parameter name to edit
      s = self._param_names[i]
      s = s.replace("[","\[")
      s = s.replace("]","\]")
      ctrl_str='<Parameter name="ObjectCN" type="cn" value="' + s + '"\/>'
      #print(ctrl_str)
      name_line_num = get_pattern_position(ctrl_str, file_out)    
      # (B) Retrieve the line number of the current parameter start value to edit
      start_val_line_num = get_pattern_position(old_str[i], file_out)
      # Test whether start_value of reference corresponds to the retrieved parameter name or not.
      if int(name_line_num) == int(start_val_line_num)-1:
	# replace the parameter starting value
	Popen('sed -i \'s/' + old_str[i] + '/' + new_str[i] + '/g\' ' + file_out, shell=True).wait()
	#print('sed -i \'s/' + old_str[i] + '/' + new_str[i] + '/g\' ' + file_out)  
      else:
	print("Error - Found wrong instance: [" + ctrl_str + "] at line " + name_line_num) 


