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


def logo():
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


def sbpipe(create_project='', simulate='', single_param_scan='', double_param_scan='', param_estim='',
           logo='', license='', log_level='INFO', quiet=False):
    """
    SBpipe function.

    :param create_project: a file
    :param simulate: a file
    :param single_param_scan: a file
    :param double_param_scan: a file
    :param param_estim: a file
    :param logo: the logo
    :param license: the license
    :param log_level: the logging level
    :param quiet: True if quiet
    :return: 0 if OK, 1  if trouble (e.g. a pipeline did not execute correctly).
    """

    set_logger()

    exit_status = 0

    if quiet:
        logger = logging.getLogger('sbpipe')
        logger.setLevel("WARNING")

    if log_level:
        logger = logging.getLogger('sbpipe')
        logger.setLevel(log_level)

    if license:
        print(license)

    if logo:
        print(logo)

    if create_project:
        from sbpipe.pl.create.newproj import NewProj
        s = NewProj()
        exit_status = 0 if s.run(create_project) else 1

    elif simulate:
        from sbpipe.pl.sim.sim import Sim
        s = Sim()
        exit_status = 0 if s.run(simulate) else 1

    elif single_param_scan:
        from sbpipe.pl.ps1.parscan1 import ParScan1
        s = ParScan1()
        exit_status = 0 if s.run(single_param_scan) else 1

    elif double_param_scan:
        from sbpipe.pl.ps2.parscan2 import ParScan2
        s = ParScan2()
        exit_status = 0 if s.run(double_param_scan) else 1

    elif param_estim:
        from sbpipe.pl.pe.parest import ParEst
        s = ParEst()
        exit_status = 0 if s.run(param_estim) else 1

    return exit_status


def main(argv=None):
    """
    SBpipe main function.

    :return: 0 if OK, 1 if trouble
    """

    # PARSER
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

    parser.add_argument('-q', '--quiet',
                        help='run %(prog)s quietly',
                        action='store_true')
    parser.add_argument('--log-level',
                        help='override the log level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-V', '--version',
                        help='show the version',
                        action='version',
                        version='%(prog)s v' + read_file_header('VERSION'))
    parser.add_argument('--license',
                        help='show the license',
                        action='store_const',
                        const=read_file_header('LICENSE'))
    parser.add_argument('--logo',
                        help='show the logo',
                        action = 'store_const',
                        const = logo())
    parser.add_argument('-c', '--create-project',
                        help='create a project structure using the argument as name',
                        metavar = 'FILE',
                        nargs=1)
    parser.add_argument('-s', '--simulate',
                        help='simulate a model',
                        metavar='FILE',
                        nargs=1)
    parser.add_argument('-p', '--single-param-scan',
                        help='simulate a single parameter scan',
                        metavar='FILE',
                        nargs=1)
    parser.add_argument('-d', '--double-param-scan',
                        help='simulate a double parameter scan',
                        metavar='FILE',
                        nargs=1)
    parser.add_argument('-e', '--param-estim',
                        help='generate a parameter fit sequence',
                        metavar='FILE',
                        nargs=1)

    args = parser.parse_args()

    create_project = ''
    if args.create_project:
        create_project = args.create_project[0]

    simulate = ''
    if args.simulate:
        simulate = args.simulate[0]

    single_param_scan = ''
    if args.single_param_scan:
        single_param_scan = args.single_param_scan[0]

    double_param_scan = ''
    if args.double_param_scan:
        double_param_scan = args.double_param_scan[0]

    param_estim = ''
    if args.param_estim:
        param_estim = args.param_estim[0]

    return sbpipe(create_project=create_project, simulate=simulate,
                  single_param_scan=single_param_scan, double_param_scan=double_param_scan,
                  param_estim=param_estim,
                  logo=args.logo, license=args.license, log_level=args.log_level, quiet=args.quiet)
