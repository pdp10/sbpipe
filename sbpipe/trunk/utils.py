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


import os
import subprocess
import shlex

import logging
logger = logging.getLogger('sbpipe')


def call_proc(cmd):
    """
    Run a command using Python subprocess.

    :param cmd: The string of the command to run
    """
    logger.info('Running ' + cmd)
    # p = subprocess.call(shlex.split(cmd))  # Block until cmd finishes
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out, err



def makedir(outputdir):
    """
    Make a dir if this does not exist
    :param outputdir: the dir to create
    """
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
