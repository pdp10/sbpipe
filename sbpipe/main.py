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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-11-02 10:18:32 $

import argparse
import logging
import os
import sys

try:  # Python 2.7+
    from logging import NullHandler, StreamHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
# Add a default empty handler (developing mode)
logging.getLogger('sbpipe').addHandler(NullHandler())

from logging.config import fileConfig

SBPIPE = os.environ["SBPIPE"]
sys.path.insert(0, SBPIPE)


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


def read_file_header(filename):
    """
    Read the first line of a file

    :param filename: the file name to read
    :return: the first line
    """
    line = ''
    with open(os.path.join(SBPIPE, filename)) as filein:
        line = filein.readline().strip() + " " + filein.readline().strip()
    return line


def set_logger():
    """
    Set the logger
    """
    home = os.path.expanduser('~')
    if not os.path.exists(os.path.join(home, '.sbpipe', 'logs')):
        os.makedirs(os.path.join(home, '.sbpipe', 'logs'))
    # disable_existing_loggers=False to enable logging for Python third-party packages
    logging_config_file = os.path.join(SBPIPE, 'logging_config.ini')
    if os.path.isfile(logging_config_file):
        fileConfig(logging_config_file,
                   defaults={'logfilename': os.path.join(home, '.sbpipe', 'logs', 'sbpipe.log')},
                   disable_existing_loggers=False)
    else:
        # Add a stream handler (production mode)
        logger = logging.getLogger('sbpipe')
        logger.addHandler(StreamHandler(sys.stdout))
        logger.setLevel("INFO")
        logger.warning('Logging configuration file not found.')
        logger.warning('Setting up new stream logger (level: INFO) for this session.')


def sbpipe(create_project='', simulate='', parameter_scan1='', parameter_scan2='', parameter_estimation='',
           logo=False, license=False, log_level='', quiet=False, verbose=False):
    """
    SBpipe function.

    :param create_project: a file
    :param simulate: a file
    :param parameter_scan1: a file
    :param parameter_scan2: a file
    :param parameter_estimation: a file
    :param logo: the logo
    :param license: the license
    :param log_level: the logging level
    :param quiet: True if quiet (WARNING+)
    :param verbose: True if verbose (DEBUG+)
    :return: 0 if OK, 1  if trouble (e.g. a pipeline did not execute correctly).
    """

    set_logger()

    exit_status = 0

    if log_level:
        logger = logging.getLogger('sbpipe')
        logger.setLevel(log_level)
    elif quiet:
        logger = logging.getLogger('sbpipe')
        logger.setLevel("WARNING")
    elif verbose:
        logger = logging.getLogger('sbpipe')
        logger.setLevel("DEBUG")

    if license:
        print(read_file_header('LICENSE'))

    elif logo:
        print(sbpipe_logo())

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

    return exit_status


def main(argv=None):
    """
    SBpipe main function.

    :return: 0 if OK, 1 if trouble
    """
    parser = argparse.ArgumentParser(prog='sbpipe.py',
                                     description='Pipelines for systems modelling of biological networks.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''
Exit status:
0  if OK,
1  if trouble (e.g. a pipeline did not execute correctly).

Report bugs to sbpipe@googlegroups.com
SBpipe home page: <https://pdp10.github.io/sbpipe>
For complete documentation, see README.md .
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
    parser.add_argument('--logo',
                        help='show the logo and exit',
                        action='store_true')
    parser.add_argument('-q', '--quiet',
                        help='print warning and error message only',
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
                        version='%(prog)s v' + read_file_header('VERSION'))

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
                  parameter_estimation=parameter_estimation,
                  logo=args.logo, license=args.license,
                  log_level=args.log_level, quiet=args.quiet, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main.main())
