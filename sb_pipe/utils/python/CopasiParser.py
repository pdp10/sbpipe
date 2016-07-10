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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $


from xml.dom.minidom import parse, parseString

# Class CopasiParser: it provides methods to retrieve information from a Copasi file
class CopasiParser: 

  # Constructor of the class
  def __init__(self):
    pass
   
  # Task: PARAMETER ESTIMATION. Parse a Copasi file and retrieve informations about the parameters to estimate
  def retrieve_param_estim_values(self, file_in):
    report_filename_template = ""
    lower_bounds = []
    param_names = []
    start_values = []
    upper_bounds = []
    print("\nParsing the xml document")
    with open(file_in) as file:
      dom = parse(file)
      # select the task tag (note: root->ListOfTaks->Tasks)
      tasks = dom.getElementsByTagName('ListOfTasks')[0].getElementsByTagName('Task')
      # iterates tasks list
      for task in tasks:
	task_name = task.getAttribute('name')
	# select Parameter Estimation task
	if task_name == "Parameter Estimation":
	  print("\nRetrieving information for " + task_name)
	  # retrieve report name for this task
	  report_filename_template = task.getElementsByTagName('Report')[0].getAttribute('target')
	  # retrieve parameter values
	  optim_item_list = task.getElementsByTagName('Problem')[0].getElementsByTagName('ParameterGroup')[0].getElementsByTagName('ParameterGroup')
	  for fit_item in optim_item_list:
	    parameters = fit_item.getElementsByTagName('Parameter')
	    # retrieve lowerbound param
	    if len(parameters) > 0 :
	      lower_bounds.append(parameters[0].getAttribute('value'))
	      # retrieve param name
	      param_names.append(parameters[1].getAttribute('value'))
	      # retrieve start value param
	      start_values.append(parameters[2].getAttribute('value'))
	      # retrieve upperbound param
	      upper_bounds.append(parameters[3].getAttribute('value'))      
	  break
    return report_filename_template, lower_bounds, param_names, start_values, upper_bounds

