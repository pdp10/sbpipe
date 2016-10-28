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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 21:43:32 $


from ConfigParser import ConfigParser
from StringIO import StringIO

import logging

logger = logging.getLogger('sbpipe')


class Pipeline:
    """
    Generic pipeline.

    :param data_folder: the folder containing the experimental (wet) data sets
    :param models_folder: the folder containing the models
    :param working_folder: the folder to store the results
    :param sim_data_folder: the folder to store the simulation data
    :param sim_plots_folder: the folder to store the graphic results
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='sim_data', sim_plots_folder='sim_plots'):
        # The data folder containing the dataset
        self.__data_folder = data_folder
        # The folder containing the models
        self.__models_folder = models_folder
        # The folder containing the working results
        self.__working_folder = working_folder
        # The dataset working folder
        self.__sim_data_folder = sim_data_folder
        # The dataset mean timecourses dir
        self.__sim_plots_folder = sim_plots_folder

    def run(self, config_file):
        """
        Run the pipeline.

        :param config_file: a configuration file for this pipeline.
        :return: 0 if the pipeline was executed correctly,
                  1 if the pipeline executed but some output was skipped,
                  2 if the pipeline did not execute correctly.
        """
        pass

    def get_data_folder(self):
        """
        Return the folder containing the experimental (wet) data sets.
        
        :return: the experimental data sets folder.
        """
        return self.__data_folder

    def get_models_folder(self):
        """
        Return the folder containing the models.
        
        :return: the models folder.
        """
        return self.__models_folder

    def get_working_folder(self):
        """
        Return the folder containing the results.
        
        :return: the working folder.
        """
        return self.__working_folder

    def get_sim_data_folder(self):
        """
        Return the folder containing the in-silico generated data sets.
        
        :return: the folder of the simulated data sets.
        """
        return self.__sim_data_folder

    def get_sim_plots_folder(self):
        """
        Return the folder containing the in-silico generated plots.
        
        :return: the folder of the simulated plots.
        """
        return self.__sim_plots_folder

    def config_parser(self, config_file, section):
        """
        Return the configuration for the parsed section in the config_file
        
        :param config_file: the configuration file to parse
        :param section: the section in the configuration file to parse
        :return: the configuration for the parsed section in the config_file
        """
        parser = ConfigParser()

        with open(config_file) as stream:
            stream = StringIO(stream.read())
            parser.readfp(stream)

        return self.read_configuration(parser.items(section))

    def read_configuration(self, lines):
        """
        Read the section lines from the configuration file. This method is abstract.
        
        :return: a tuple containing the configuration
        """
        pass

    def read_common_configuration(self, lines):
        """
        Parse the common parameters from the configuration file
        
        :return: return a tuple containing the common parameters
        """
        # default values
        # Boolean flag
        generate_data = True
        # Boolean flag
        analyse_data = True
        # Boolean flag
        generate_report = True
        # the project directory
        project_dir = ""
        # the  model
        model = "model"

        # Initialises the variables
        for line in lines:
            # logger.info(line)
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

        return (generate_data, analyse_data, generate_report,
                project_dir, model)
