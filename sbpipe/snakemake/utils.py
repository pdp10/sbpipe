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

import re
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


def replace_str_in_report(report):

    # `with` ensures that the file is closed correctly
    # re.sub(pattern, replace, string) is the equivalent of s/pattern/replace/ in sed.
    with open(report, 'r') as file:
        lines = file.readlines()
    with open(report, 'w') as file:
        # for idx, line in lines:
        for i in range(len(lines)):
            if i < 1:
                # First remove non-alphanumerics and non-underscores.
                # Then replaces whites with TAB.
                # Finally use rstrip to remove the TAB at the end.
                # [^\w] matches anything that is not alphanumeric or underscore
                lines[i] = lines[i].replace("Values[", "").replace("]", "")
                file.write(
                    re.sub(r"\s+", '\t', re.sub(r'[^\w]', " ", lines[i])).rstrip('\t') + '\n')
            else:
                file.write(lines[i].rstrip('\t'))


def clean_copasi_files(inputdir, files):
    for report in files:
        os.remove(os.path.join(inputdir, report))


def makedir(outputdir):
    """
    Make a dir if this does not exist
    :param outputdir: the dir to create
    """
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
