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

import getopt
import logging
import os
import sys

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
# Add a default empty handler
logging.getLogger(__name__).addHandler(NullHandler())
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


def help():
    """
    Return help message.

    :return: the help message
    """
    message = (
        "Usage: sbpipe.py [OPTION] [FILE]\n"
        "Pipelines for systems modelling of biological networks.\n\n"
        "List of mandatory options:\n"
        "\t-h, --help\n\t\tShow this help.\n"
        "\t-c, --create-project\n\t\tCreate a project structure using the argument as name.\n"
        "\t-s, --simulate\n\t\tSimulate a model.\n"
        "\t-p, --single-param-scan\n\t\tSimulate a single parameter scan.\n"
        "\t-d, --double-param-scan\n\t\tSimulate a double parameter scan.\n"
        "\t-e, --param-estim\n\t\tGenerate a parameter fit sequence.\n"
        # "\t-n, --sensitivity\n\t\tRun a sensitivity analysis (in progress).\n\n"
        "\t-l, --license\n\t\tShow the license.\n"
        "\t-v, --version\n\t\tShow the version.\n"
        "Exit status:\n"
        " 0  if OK,\n"
        " 1  if minor problems (e.g. a pipeline did not execute correctly),\n"
        " 2  if serious trouble (e.g. cannot access command-line argument).\n\n"
        "Report bugs to sbpipe@googlegroups.com\n"
        "sbpipe home page: <https://pdp10.github.io/sbpipe>\n"
        "For complete documentation, see README.md .\n"
    )
    return message


def _read_file_header(filename):
    """
    Read the first line of a file

    :param filename: the file name to read
    :return: the first line
    """
    line = ''
    with open(os.path.join(SBPIPE, filename)) as filein:
        line = filein.readline().strip() + " " + filein.readline().strip()
    return line


def license():
    """
    Return the license

    :return: the license
    """
    return _read_file_header('LICENSE')


def version():
    """
    Return the version

    :return: the version
    """
    return _read_file_header('VERSION')


class Usage(Exception):
    """
    This class is used for printing a generic exception
    """

    def __init__(self, msg):
        """
        Constructor

        :param msg: the message to print
        """
        self.msg = msg


def check_args(args, msg):
    """
    Check that at least one argument is passed.

    :param args: the list of arguments
    :param msg: the message to print
    :raise: Usage exception if less than one argument is passed
    :return: no output
    """
    if len(args) < 1:
        raise (Usage(msg))


def main(argv=None):
    """
    SB pipe main function.
    
    :param argv: options for sbpipe. Type python -m sbpipe -h for a full list of options.
    :return: 0 if OK, 1 if minor problems, or 2 if serious trouble.
    """

    if argv is None:
        argv = sys.argv

    # logging settings
    home = os.path.expanduser('~')
    if not os.path.exists(os.path.join(home, '.sbpipe', 'logs')):
        os.makedirs(os.path.join(home, '.sbpipe', 'logs'))
    # disable_existing_loggers=False to enable logging for Python third-party packages
    fileConfig(os.path.join(SBPIPE, 'logging_config.ini'),
               defaults={'logfilename': os.path.join(home, '.sbpipe', 'logs', 'sbpipe.log')},
               disable_existing_loggers=False)

    exit_status = 0
    no_conf_file_msg = 'no configuration file received'
    no_project_name_msg = 'no project name received'

    try:
        try:
            opts, args = getopt.getopt(argv[1:],
                                       'hlvcspde',
                                       ['help',
                                        'license',
                                        'version'
                                        'create-project',
                                        'simulate',
                                        'single-param-scan',
                                        'double-param-scan',
                                        'param-estim'
                                        ])

            for opt, arg in opts:

                if opt in ('-h', '--help'):
                    print(help())

                elif opt in ('-l', '--license'):
                    print(license())

                elif opt in ('-v', '--version'):
                    print(version())

                elif opt in ('-c', '--create-project'):
                    check_args(args, no_project_name_msg)
                    from sbpipe.pl.create.newproj import NewProj
                    s = NewProj()
                    exit_status = 0 if s.run(args[0]) else 1

                elif opt in ('-s', '--simulate'):
                    check_args(args, no_conf_file_msg)
                    print(logo())
                    from sbpipe.pl.sim.sim import Sim
                    s = Sim()
                    exit_status = 0 if s.run(args[0]) else 1

                elif opt in ('-p', '--single-param-scan'):
                    check_args(args, no_conf_file_msg)
                    print(logo())
                    from sbpipe.pl.ps1.parscan1 import ParScan1
                    s = ParScan1()
                    exit_status = 0 if s.run(args[0]) else 1

                elif opt in ('-d', '--double-param-scan'):
                    check_args(args, no_conf_file_msg)
                    print(logo())
                    from sbpipe.pl.ps2.parscan2 import ParScan2
                    s = ParScan2()
                    exit_status = 0 if s.run(args[0]) else 1

                elif opt in ('-e', '--param-estim'):
                    check_args(args, no_conf_file_msg)
                    print(logo())
                    from sbpipe.pl.pe.parest import ParEst
                    s = ParEst()
                    exit_status = 0 if s.run(args[0]) else 1

                # elif opt in ('-n', '--sensitivity'):
                #     check_args(args, no_conf_file_msg)
                #     print(logo())
                #     print('Not yet available. Apologise.')
                #     exit_status = 0
                #     from sbpipe.pl.sens.sens import Sens
                #     s = Sens()
                    # exit_status = 0 if s.run(args[0]) else 1

            if len(opts) < 1:
                raise Usage('no option received')

        except getopt.error as msg:
            raise Usage(msg)

    except Usage as err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, 'for help use -h, --help'
        exit_status = 2

    return exit_status
