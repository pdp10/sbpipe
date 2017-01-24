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
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-11-01 15:43:32 $



import logging
logger = logging.getLogger('sbpipe')

try:
    import configparser # Python 3
except ImportError:
    import ConfigParser as configparser # Python 2



def config_parser(self, config_file, section):
    """
    Return the configuration for the parsed section in the config_file

    :param config_file: the configuration file to parse
    :param section: the section in the configuration file to parse
    :return: the configuration for the parsed section in the config_file
    """
    parser = configparser.ConfigParser()
    with open(config_file) as myfile:
        # TODO - Legacy code for Python 2.7.
        # Although readfp() works for Python 3, it is deprecated.
        # In the future the code below will be just
        # parser.read_file(myfile)
        import sys
        if sys.version_info < (3,):
            parser.readfp(myfile)
        else:
            parser.read_file(myfile)
    return self.read_config(parser.items(section))


def read_common_config(lines):
    """
    Parse the common parameters from the configuration file

    :param lines: the lines to parse.
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


def read_ps2_config(lines):

    # parse common options
    (generate_data, analyse_data, generate_report,
     project_dir, model) = read_common_config(lines)

    # default values
    simulator = 'Copasi'
    # the first scanned param
    scanned_par1 = ""
    # the second scanned param
    scanned_par2 = ""
    cluster = 'local'
    local_cpus = 1
    runs = 1
    # the simulation length
    sim_length = 1

    # Initialises the variables
    for line in lines:
        logger.info(line)
        if line[0] == "simulator":
            simulator = line[1]
        elif line[0] == "scanned_par1":
            scanned_par1 = line[1]
        elif line[0] == "scanned_par2":
            scanned_par2 = line[1]
        elif line[0] == "cluster":
            cluster = line[1]
        elif line[0] == "local_cpus":
            local_cpus = line[1]
        elif line[0] == "runs":
            runs = line[1]
        elif line[0] == "sim_length":
            sim_length = line[1]

    return (generate_data, analyse_data, generate_report,
            project_dir, simulator, model, scanned_par1, scanned_par2,
            cluster, local_cpus, runs, sim_length)
