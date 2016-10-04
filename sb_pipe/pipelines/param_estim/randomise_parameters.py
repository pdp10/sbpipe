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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $


import sys, os, os.path
from copasi_parser import *
from io_util_functions import *
import shutil
import random
import shlex
from subprocess import * 
import logging
logger = logging.getLogger('sbpipe')


class RandomiseParameters:
    """
    This class generates multiple copies of a Copasi file configured for parameter estimation task, and randomises the starting
    values of the parameters to estimate.
    """

    def __init__(self, path, filename_in):
        """
        Constructor. Initialise the Copasi parser on filename_in.

        :param path: the path to filename_in
        :param filename_in: the Copasi file to process.
        """

        # A Copasi Object
        self.__copasi = CopasiParser()
        # Path containing the template Copasi file
        self.__path = path
        # The name of the template Copasi file
        self.__filename_in = filename_in
        # The name of the template parameter estimation report
        # The list of lower bounds of the parameters
        # The list of names of the parameters
        # The list of start values of the parameters
        # The list of upper bounds of the parameters
        self.__report_filename_template, self.__lower_bounds, self.__param_names, \
        self.__start_values, self.__upper_bounds = \
            self.__copasi.retrieve_param_estim_values(os.path.join(self.__path, self.__filename_in))

    def generate_instances_from_template(self, num_files, idstr):
        """
        Generate num_files files and randomise the starting values for the parameter to estimate.

        :param num_files: the number of files (instances) to generate
        :param idstr: an ID string to label the generated files (e.g. a timestamp)
        :return:
        """
        num_files = int(num_files)
        logger.info("Randomising parameters for:")
        for i in range(0, num_files):
            # initialise the names and generate the output file
            filename_out = self.__filename_in[:-4] + idstr + str(i + 1) + ".cps"
            report_filename = self.__report_filename_template[:-4] + idstr + str(i + 1) + ".csv"
            file_out = os.path.join(self.__path, filename_out)
            file_in = os.path.join(self.__path, self.__filename_in)
            if os.path.isfile(file_out):
                os.remove(file_out)
            shutil.copy2(file_in, file_out)
            # 1) RANDOMIZATION
            logger.info(filename_out)
            new_start_values, old_str, new_str = self.__randomise_start_value()
            # 2) PRINT NEW VALUES
            #logger.info("\nInitial parameters for the output file: " + file_out)
            self.__print_parameters_to_estimate2(new_start_values)
            # 3) REPLACE VALUES IN THE NEW FILE
            self.__replace_start_value_in_file(file_out, report_filename, old_str, new_str)

    def get_copasi_obj(self):
        """
        Return the Copasi parser object

        :return: the Copasi parser object
        """
        return self.__copasi

    def get_path(self):
        """
        Return the path containing the template Copasi file

        :return: the path to the Copasi file
        """
        return self.__path

    def get_template_copasi_file(self):
        """
        Return the name of the template Copasi file

        :return: the name of the Copasi file
        """
        return self.__filename_in

    def get_report_filename_template_str(self):
        """
        Return the name of the template parameter estimation report

        :return: the name of the report file name for parameter estimation
        """
        return self.__report_filename_template

    def get_lower_bounds_list(self):
        """
        Return the list of parameter lower bounds

        :return: the list of parameter lower bounds
        """
        return self.__lower_bounds

    def get_param_names_list(self):
        """
        Return the list of parameter names

        :return: the list of parameter names
        """
        return self.__param_names

    def get_start_values_list(self):
        """
        Return the list of parameter starting values

        :return: the list of parameter starting values
        """
        return self.__start_values

    def get_upper_bounds_list(self):
        """
        Return the list of parameter upper bounds

        :return: the list of parameter upper bounds
        """
        return self.__upper_bounds

    def print_parameters_to_estimate(self):
        """
        Print the parameter names, lower/upper bounds, and starting value, as extracted from COPASI template file

        :return:
        """
        logger.info("\t\tParameterName\t\tLowerBound\t\tStartValue\t\tUpperBound")
        logger.info("\t\t=============\t\t==========\t\t==========\t\t==========")
        for i in range(0, len(self.__param_names)):
            logger.info("\t\t" + self.__param_names[i][self.__param_names[i].find("[") +
                      1:self.__param_names[i].find("]")] +
                      "\t\t" + self.__lower_bounds[i] + "\t\t" + self.__start_values[i] +
                        "\t\t" + self.__upper_bounds[i])

    def __print_parameters_to_estimate2(self, new_start_values):
        """
        Print the parameter names, lower/upper bounds, and starting value, as extracted from COPASI template file. 
        Additionally, the new random starting value is also printed for each parameter.

        :param new_start_values: the list of new starting values for the parameters.
        :return:
        """
        logger.debug("\t\tParameter\t\tLowerBound\t\tUpperBound\t\tStartValue\t\tNEWStartValue")
        logger.debug("\t\t=========\t\t==========\t\t==========\t\t==========\t\t=============")
        for i in range(0, len(self.__param_names)):
            logger.debug("\t\t" + self.__param_names[i][self.__param_names[i].find("[") +
                                                        1:self.__param_names[i].find("]")] +
                        "\t\t" + self.__lower_bounds[i] +
                        "\t\t" + self.__upper_bounds[i] +
                        "\t\t" + self.__start_values[i] +
                        "\t\t" + new_start_values[i])

    def __randomise_start_value(self):
        """
        Randomise the parameter starting values

        :return: the lists of new starting values together with the lists of old and new XML strings containing 
        the old / new starting values in the Copasi file.
        """
        new_start_values = []
        old_str = []
        new_str = []
        # Randomize the starting values using the respective lower and upper bounds using a uniform distibution
        for i in range(0, len(self.__param_names)):
            if(str(self.__lower_bounds[i].find("CN=Root,Model=") != -1) or
               str(self.__upper_bounds[i].find("CN=Root,Model=") != -1)):
                # Either the lower or the upper bound is a variable. Fix a random value in [1e-05,1]
                new_start_values.append(str(random.uniform(0.00001, 1)))
            else:
                # The lower and the upper bounds are constants
                new_start_values.append(str(random.uniform(float(self.__lower_bounds[i]),
                                                            float(self.__upper_bounds[i]))))
            old_str.append('<Parameter name="StartValue" type="float" value="' + self.__start_values[i] + '"/>')
            new_str.append('<Parameter name="StartValue" type="float" value="' + new_start_values[i] + '"/>')
            #logger.debug(old_str[i])
            #logger.debug(new_str[i])
        return new_start_values, old_str, new_str

    def __replace_start_value_in_file(self, file_out, report_filename, old_str, new_str):
        """
        For each parameter to estimate, replace the current start value with the new randomised start value

        :param file_out: the Copasi output file.
        :param report_filename: the report file name
        :param old_str: the list of XML strings containing the old starting values. 
        :param new_str: the list of XML strings containing the new starting values.
        :return:
        """
        replace_string_in_file(file_out, self.__report_filename_template, report_filename)

        for i in range(0, len(self.__param_names)):
            # Check whether the replacement of the parameter start value is exactly for the parameter estimation task
            # and for the corresponding parameter name. So, if different parameters have same start values, the algorithm
            # replaces only the value for the corresponding parameter and not to all the instances with equal start value.
            # (A) Retrieve the line number of the current parameter name to edit
            s = self.__param_names[i]

            ctrl_str='<Parameter name="ObjectCN" type="cn" value="' + s + '"/>'
            #logger.debug(ctrl_str)
            name_line_num = get_pattern_position(ctrl_str, file_out)
            # (B) Retrieve the line number of the current parameter start value to edit
            start_val_line_num = get_pattern_position(old_str[i], file_out)
            # Test whether start_value of reference corresponds to the retrieved parameter name or not.
            if int(name_line_num) == int(start_val_line_num)-1:
                # replace the parameter starting value
                replace_string_in_file(file_out, old_str[i], new_str[i])
            else:
                logger.warn("Error - Found wrong instance: [" + ctrl_str + "] at line " + name_line_num)


