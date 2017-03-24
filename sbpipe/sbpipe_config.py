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
# $Date: 2016-07-11 11:14:32 $

import os
import subprocess
import logging
logger = logging.getLogger('sbpipe')


def which(cmd_name):
    """
    Utility equivalent to `which` in GNU/Linux OS.
    
    :param cmd_name: a command name
    :return: return the command name with absolute path if this exists, or None
    """
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, cmd_name)):
            return os.path.join(path, cmd_name)
        if os.path.exists(os.path.join(path, cmd_name + '.exe')):
            return os.path.join(path, cmd_name + '.exe')
    return None

def isPyPackageInstalled(package):
    """
    Utility checking whether a Python package is installed.

    :param package: a Python package name
    :return: True if it is installed, false otherwise.
    """
    try:
        installed_packages = subprocess.Popen(['pip', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        if package in str(installed_packages):
            return True
        return False
    except OSError as e:
        logger.warning("pip is not installed")
        return False
