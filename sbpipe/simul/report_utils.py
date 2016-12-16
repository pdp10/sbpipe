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
# $Date: 2016-12-16 12:14:32 $

import os
import shutil
import re


def replace_str_pl_sim_report(report):
    """
    Replace a group of annotation strings from report generated with a programming language
    
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


def move_sim_report_files(outputdir, group_model, groupid):
    """
    Move the report files
    :param outputdir: the output directory
    :param group_model: the model file name
    :param groupid: the group id of the reports
    """
    # move the report files from the current folder to the output folder
    # Note, R executes the model from the current folder.
    report_files = [f for f in os.listdir('.') if
                    re.match(group_model + '[0-9]+.*\.csv', f) or re.match(group_model + '[0-9]+.*\.txt', f)]
    # print(report_files)
    for file in report_files:
        # Replace some string in the report file
        replace_str_pl_sim_report(file)
        # rename and move the output file
        shutil.move(file, os.path.join(outputdir, file.replace(groupid, "_")[:-4] + ".csv"))

