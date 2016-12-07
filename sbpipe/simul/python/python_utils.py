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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $

# Utilities for changing column names generated with Python

import re


def replace_str_python_sim_report(report):
    """
    Replace a group of annotation strings from a generated Python report files
    
    :param report: The report file with absolute path
    """

    # `with` ensures that the file is closed correctly
    # re.sub(pattern, replace, string) is the equivalent of s/pattern/replace/ in sed.
    with open(report, "r") as file:
        lines = file.readlines()
    with open(report, "w") as file:
        # for idx, line in lines:
        for i in range(len(lines)):
            if i < 1:
                # First remove non-alphanumerics and non-underscores. 
                # Then replaces whites with TAB.
                # Finally use rstrip to remove the TAB at the end.
                # [^\w] matches anything that is not alphanumeric or underscore
                lines[i] = lines[i].replace("\"", "").replace("time", "Time")
                file.write(
                    re.sub(r"\s+", '\t', re.sub(r'[^\w]', " ", lines[i])).rstrip('\t') + '\n')
            else:
                file.write(lines[i].rstrip('\t'))
