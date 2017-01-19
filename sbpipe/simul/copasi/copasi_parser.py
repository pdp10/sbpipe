#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $


import logging
from xml.dom.minidom import parse
import warnings

logger = logging.getLogger('sbpipe')


class CopasiParser:
    """
    Retrieve information from a Copasi file.
    """

    def __init__(self):
        """
        Constructor.
        """
        warnings.warn("deprecated class", DeprecationWarning, stacklevel=2)
        pass

    @classmethod
    def get_param_estim_val(cls, file_in):
        """
        Parse a Copasi file and retrieve information about the parameters to estimate.

        :param file_in: the Copasi file including absolute path to parse
        :return: a tuple containing the report file name, the parameter lower bounds, \
        names, starting values, and upper bounds
        """
        report_filename_template = ""
        lower_bounds = []
        param_names = []
        start_values = []
        upper_bounds = []
        logger.info("Parsing the xml document")
        with open(file_in) as file:
            dom = parse(file)
            # select the task tag (note: root->ListOfTaks->Tasks)
            tasks = dom.getElementsByTagName('ListOfTasks')[0].getElementsByTagName('Task')
            # iterates tasks list
            for task in tasks:
                task_name = task.getAttribute('name')
                # select Parameter Estimation task
                if task_name == "Parameter Estimation":
                    logger.info("Retrieving information for " + task_name)
                    # retrieve report name for this task
                    report_filename_template = task.getElementsByTagName('Report')[0].getAttribute('target')
                    # retrieve parameter values
                    optim_item_list = task.getElementsByTagName('Problem')[0].getElementsByTagName('ParameterGroup')[
                        0].getElementsByTagName('ParameterGroup')
                    for fit_item in optim_item_list:
                        parameters = fit_item.getElementsByTagName('Parameter')
                        # retrieve lowerbound param
                        if len(parameters) > 0:
                            lower_bounds.append(parameters[0].getAttribute('value'))
                            # retrieve param name
                            param_names.append(parameters[1].getAttribute('value'))
                            # retrieve start value param
                            start_values.append(parameters[2].getAttribute('value'))
                            # retrieve upperbound param
                            upper_bounds.append(parameters[3].getAttribute('value'))
                    break
        return report_filename_template, lower_bounds, param_names, start_values, upper_bounds
