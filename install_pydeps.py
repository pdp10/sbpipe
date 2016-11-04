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
# Object: install sbpipe requirements
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-26 22:18:32 $

import logging
import os
import subprocess
import sys
from logging.config import fileConfig

SBPIPE = os.environ["SBPIPE"]
sys.path.append(os.path.join(SBPIPE, "sbpipe"))
from sbpipe.sb_config import which


def install_python_deps(requirements_file):
    """
    Install python depenencies using pip. pip must have been installed.
    """
    cmd = ['pip', 'install', '--user', '-r', requirements_file]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    return out


def python_deps(logger):
    logger.info("Installing Python dependencies...")
    if which("pip") is None:
        logger.warn("pip not found. Skipping installation of Python dependencies."
                    "Please, install `python-dev` and `python-pip` packages.")
    else:
        out = str(install_python_deps(os.path.join(SBPIPE, 'requirements.txt')))
        logger.debug(out)
        if ' ERROR:' in out or ' Error:' in out:
            logger.error("Some error occurred when installing Python dependencies."
                         "Please check log files in logs/")
        else:
            logger.info("Python dependencies should have been installed correctly.")


def main():
    # logging settings
    home = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home, '.sbpipe', 'logs')):
        os.makedirs(os.path.join(home, '.sbpipe', 'logs'))
    # disable_existing_loggers=False to enable logging for Python third-party packages
    fileConfig(os.path.join(SBPIPE, 'logging_config.ini'),
               defaults={'logfilename': os.path.join(home, '.sbpipe', 'logs', 'sbpipe_pydeps.log')},
               disable_existing_loggers=False)
    logger = logging.getLogger('sbpipe')

    if which("CopasiSE") is None:
        logger.error("CopasiSE not found. Please install Copasi as explained on the sbpipe website.")

    if which("R") is None:
        logger.error("R not found. Skipping installation of R dependencies."
                     "sbpipe will be severely affected due to this.")

    python_deps(logger)


if __name__ == "__main__":
    sys.exit(main())
