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


import platform
import argparse
import logging
import os
from logging.config import fileConfig
from sbpipe.utils.parcomp import run_cmd

try:  # Python 2.7+
    from logging import NullHandler, StreamHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
# Add a default empty handler (developing mode)
logging.getLogger('sbpipe').addHandler(NullHandler())


def sbpipe_logo():
    """
    Return sbpipe logo.

    :return: sbpipe logo
    """
    sb_logo = (
        "\n"
        "                      _             \n"
        "          /\         (_)            \n"
        "    ___  / /_  ____    ____  ___    \n"
        "   / __\/ __ \/ __ \/\/ __ \/ _ \   \n"
        "  _\ \_/ /_/ / /_/ / / /_/ /  __/   \n"
        " \____/\____/ ____/_/ ____/\____/   \n"
        "           / /     / /              \n"
        "          /_/     /_/               \n"
    )
    return sb_logo


def sbpipe_license():
    """
    Return sbpipe license.

    :return: sbpipe license
    """
    return "MIT License"


def sbpipe_version():
    """
    Return sbpipe version.

    :return: sbpipe version
    """
    version = ""
    with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as in_file:
        version = in_file.read().splitlines()[0]
    return version


def set_basic_logger(level='INFO'):
    """
    Set a basic StreamHandler logger.
    :param level: the level for this console logger
    """
    # Add a stream handler (production mode)
    logger = logging.getLogger('sbpipe')
    logger.handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel('DEBUG')
    logger.debug('Set basic logger')


def set_color_logger(level='INFO'):
    """
    Replace the current logging.StreamHandler with colorlog.StreamHandler.
    :param level: the level for this console logger
    """
    logger = logging.getLogger('sbpipe')
    try:
        import colorlog
    except ImportError as e:
        logger.warning("Python package `colorlog` not found. Skipping color logs.")
        set_basic_logger(level)
        return
    # Remove all handlers except for instances of logging.FileHandler
    logger.handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    # Add a new colour stream handler
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s - %(message)s'))
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel('DEBUG')
    logger.debug('Setting color logger')


def set_console_logger(new_level='NOTSET', current_level='INFO', nocolor=False):
    """
    Set the console logger to a new level if this is different from NOTSET

    :param new_level: the new level to set for the console logger
    :param current_level: the current level to set for the console logger
    :param nocolor: True if no colors shouls be used
    """
    if new_level == 'NOTSET':
        new_level = current_level

    if nocolor:
        set_basic_logger(new_level)
    else:
        set_color_logger(new_level)


def set_logger(level='NOTSET', nocolor=False):
    """
    Set the logger
    :param level: the level for the console logger
    :param nocolor: True if no colors shouls be used
    """
    home = os.path.expanduser('~')
    if not os.path.exists(os.path.join(home, '.sbpipe', 'logs')):
        os.makedirs(os.path.join(home, '.sbpipe', 'logs'))
    # disable_existing_loggers=False to enable logging for Python third-party packages
    logging_config_file = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
    if os.path.isfile(logging_config_file):
        try:
            with open(logging_config_file, 'r') as fname:
                fileConfig(fname,
                           defaults={'logfilename': os.path.join(home, '.sbpipe', 'logs', 'sbpipe.log')},
                           disable_existing_loggers=False)
            set_console_logger(level, logging.getLogger('sbpipe').getEffectiveLevel(), nocolor)
        except Exception:
            set_console_logger(level, 'INFO', nocolor)
            logger = logging.getLogger('sbpipe')
            logger.warning('Logging configuration file ' + logging_config_file + ' is corrupted')
    else:
        set_console_logger(level, 'INFO', nocolor)
        logger = logging.getLogger('sbpipe')
        logger.warning('Logging configuration file ' + logging_config_file + ' is missing')


def sbpipe(create_project='',
           simulate='',
           parameter_scan1='',
           parameter_scan2='',
           parameter_estimation='',
           version=False,
           logo=False,
           license=False,
           nocolor=False,
           log_level='',
           quiet=False,
           verbose=False):
    """
    SBpipe function.

    :param create_project: create a project with the name as argument
    :param simulate: model simulation using a configuration file as argument
    :param parameter_scan1: model one parameter scan using a configuration file as argument
    :param parameter_scan2: model two parameters scan using a configuration file as argument
    :param parameter_estimation: model parameter estimation using a configuration file as argument
    :param version: True to print the version
    :param logo: True to print the logo
    :param license: True to print the license
    :param nocolor: True to print logging messages without colors
    :param log_level: Set the logging level
    :param quiet: True if quiet (CRITICAL+)
    :param verbose: True if verbose (DEBUG+)
    :return: 0 if OK, 1  if trouble (e.g. a pipeline did not execute correctly).
    """

    exit_status = 0

    # setup the logger
    if log_level:
        set_logger(log_level, nocolor=nocolor)
    elif quiet:
        set_logger('CRITICAL', nocolor=nocolor)
    elif verbose:
        set_logger('DEBUG', nocolor=nocolor)
    else:
        set_logger()

    logger = logging.getLogger('sbpipe')

    # add platform information
    #logger.debug(platform.machine())
    logger.debug(platform.version())
    logger.debug(platform.platform())
    logger.debug('Python ' + platform.python_version())
    # retrieve the first line from the command output message
    logger.debug(run_cmd('R --version')[0].decode('utf-8').splitlines()[0])
    logger.debug('SBpipe ' + sbpipe_version())

    if version:
        print(sbpipe_version())
    elif logo:
        print(sbpipe_logo())
    elif license:
        print(sbpipe_license())
    elif create_project:
        from sbpipe.pl.create.newproj import NewProj
        s = NewProj()
        exit_status = 0 if s.run(create_project) else 1
    elif simulate:
        from sbpipe.pl.sim.sim import Sim
        s = Sim()
        exit_status = 0 if s.run(simulate) else 1
    elif parameter_scan1:
        from sbpipe.pl.ps1.parscan1 import ParScan1
        s = ParScan1()
        exit_status = 0 if s.run(parameter_scan1) else 1
    elif parameter_scan2:
        from sbpipe.pl.ps2.parscan2 import ParScan2
        s = ParScan2()
        exit_status = 0 if s.run(parameter_scan2) else 1
    elif parameter_estimation:
        from sbpipe.pl.pe.parest import ParEst
        s = ParEst()
        exit_status = 0 if s.run(parameter_estimation) else 1

    logging.shutdown()

    return exit_status


def main(argv=None):
    """
    SBpipe main function.

    :return: 0 if OK, 1 if trouble
    """
    parser = argparse.ArgumentParser(prog='sbpipe',
                                     description='Pipelines for systems modelling of biological networks.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''
Exit status:
0  if OK,
1  if trouble (e.g. a pipeline did not execute correctly).

Report bugs to sbpipe@googlegroups.com
SBpipe home page: <https://github.com/pdp10/sbpipe>
For complete documentation, see http://sbpipe.readthedocs.io .
    ''')

    parser.add_argument('-c', '--create-project',
                        help='create a project structure',
                        metavar='NAME',
                        nargs=1)
    parser.add_argument('-s', '--simulate',
                        help='run time course simulations',
                        metavar='FILE',
                        nargs=1)
    parser.add_argument('-p', '--parameter-scan1',
                        help='run parameter scans for 1 model variable',
                        metavar='FILE',
                        nargs=1)
    parser.add_argument('-d', '--parameter-scan2',
                        help='run parameter scans for 2 model variables',
                        metavar='FILE',
                        nargs=1)
    parser.add_argument('-e', '--parameter-estimation',
                        help='run parameter estimations',
                        metavar='FILE',
                        nargs=1)
    parser.add_argument('--license',
                        help='show the license and exit',
                        action='store_true')
    parser.add_argument('--nocolor',
                        help='print logging messages without colors',
                        action='store_true')
    parser.add_argument('--logo',
                        help='show the logo and exit',
                        action='store_true')
    parser.add_argument('-q', '--quiet',
                        help='do not print any log',
                        action='store_true')
    parser.add_argument('--log-level',
                        help='override the log level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-v', '--verbose',
                        help='print debugging output',
                        action='store_true')
    parser.add_argument('-V', '--version',
                        help='show the version and exit',
                        action='version',
                        version='%(prog)s ' + sbpipe_version())

    args = parser.parse_args()

    create_project = ''
    if args.create_project:
        create_project = args.create_project[0]

    simulate = ''
    if args.simulate:
        simulate = args.simulate[0]

    parameter_scan1 = ''
    if args.parameter_scan1:
        parameter_scan1 = args.parameter_scan1[0]

    parameter_scan2 = ''
    if args.parameter_scan2:
        parameter_scan2 = args.parameter_scan2[0]

    parameter_estimation = ''
    if args.parameter_estimation:
        parameter_estimation = args.parameter_estimation[0]

    return sbpipe(create_project=create_project, simulate=simulate,
                  parameter_scan1=parameter_scan1, parameter_scan2=parameter_scan2,
                  parameter_estimation=parameter_estimation, version=False,
                  logo=args.logo, license=args.license, nocolor=args.nocolor,
                  log_level=args.log_level, quiet=args.quiet, verbose=args.verbose)

