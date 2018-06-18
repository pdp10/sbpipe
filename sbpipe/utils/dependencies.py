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


def is_py_package_installed(package):
    """
    Utility checking whether a Python package is installed.

    :param package: a Python package name
    :return: True if it is installed, false otherwise.
    """
    try:
        installed_packages = subprocess.Popen(['pip', 'list'],
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE).communicate()[0]
        if package in str(installed_packages):
            return True
        return False
    except OSError as e:
        logger.warning("pip is not installed")
        return False


def is_r_package_installed(package):
    """
    Utility checking whether a R package is installed.

    :param package: an R package name
    :return: True if it is installed, false otherwise.
    """
    try:
        output = subprocess.Popen(['Rscript',
                                   os.path.join(os.path.dirname(__file__), os.pardir, "is_package_installed.r"),
                                   package],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).communicate()[0]
        logger.debug("is sbpiper installed? " + str(output))
        if "TRUE" in str(output):
            return True
        return False
    except OSError as e:
        logger.error("R is not installed")
        return False
