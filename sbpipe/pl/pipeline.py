#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
# locate is used to dynamically load a class by its name.
from pydoc import locate
import yaml
import os
import tarfile

logger = logging.getLogger('sbpipe')


class Pipeline:
    """
    Generic pipeline.

    :param models_folder: the folder containing the models
    :param working_folder: the folder to store the results
    :param sim_data_folder: the folder to store the simulation data
    :param sim_plots_folder: the folder to store the graphic results
    """

    def __init__(self, models_folder='Models', working_folder='Results',
                 sim_data_folder='sim_data', sim_plots_folder='sim_plots'):
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
        :return: True if the pipeline was executed correctly, False otherwise.
        """
        pass

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

    @staticmethod
    def generate_tarball(working_dir, output_folder):
        """
        Create a gz tarball.

        :param working_dir: the working directory
        :param output_folder: the name of the folder to store the tar.gz file
        :return: True if the generation of the tarball succeeded.
        """
        logger.info("\n")
        logger.info("Zipping results:")
        logger.info("================")
        logger.info("Generating .tgz file")
        orig_wd = os.getcwd()  # remember our original working directory
        os.chdir(working_dir)  # change folder
        with tarfile.open(output_folder + ".tgz", "w:gz") as tar:
            tar.add(output_folder, arcname=os.path.basename(output_folder))
        os.chdir(orig_wd)  # get back to our original working directory
        logger.info(output_folder + ".tgz")
        return True

    @classmethod
    def get_simul_obj(cls, simulator):
        """
        Return the simulator object if this exists. Otherwise throws an exception.
        The simulator name starts with an upper case letter. Each simulator is in a package
        within `sbpipe.simulator`.
       
        :param simulator: the simulator name
        :return: the simulator object.
        """
        # use reflection to dynamically load the simulator class by name
        logger.debug('Loading simulator: ' + simulator)
        simul = locate('sbpipe.simul.' + simulator.lower() + '.' + simulator.lower() + '.' + simulator)()
        logger.debug('Simulator loaded: ' + str(simul.__class__))
        return simul

    @classmethod
    def load(cls, config):
        """
        Safely load a YAML configuration file and return its structure as a dictionary object.

        :param config: a YAML configuration file
        :return: the dictionary structure of the configuration file
        :raise: yaml.YAMLError if the config cannot be loaded.
        """
        with open(config, 'r') as stream:
            config_dict = yaml.safe_load(stream)
        logger.debug('Loaded configuration dictionary: ' + str(config_dict))
        return config_dict

    def parse(self, config_dict):
        """
        Read a dictionary structure containing the pipeline configuration. This method is abstract.
        
        :return: a tuple containing the configuration
        """
        pass
