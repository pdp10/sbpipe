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
# $Date: 2016-07-16 12:14:32 $

import glob
import logging
import os
import shutil
import re
from sbpipe.utils.re_utils import nat_sort_key

logger = logging.getLogger('sbpipe')


# utilities for collecting parameter estimation results
#######################################################


def get_best_fits(path_in=".", path_out=".", filename_out="final_estimates.csv"):
    """
    Collect the final parameter estimates. Results
    are stored in filename_out.

    :param path_in: the path to the input files
    :param path_out: the path to the output files
    :param filename_out: the filename to store the final estimates
    """
    # The path containing the results .csv files
    path = path_in
    # The collection of .csv files
    files = get_input_files(path)
    # List of estimated parameters
    col_names = get_params_list(files[0])
    col_names.insert(0, 'Estimation')
    col_names.insert(1, 'ObjectiveValue')
    write_params(col_names, path_out, filename_out)
    write_best_fits(files, path_out, filename_out)


def get_all_fits(path_in=".", path_out=".", filename_out="all_estimates.csv"):
    """
    Collect all the parameter estimates. Results
    are stored in filename_out.

    :param path_in: the path to the input files
    :param path_out: the path to the output files
    :param filename_out: the filename to store the final estimates
    """
    # The path containing the results .csv files
    path = path_in
    # The collection of .csv files
    files = get_input_files(path)
    # List of estimated parameters
    col_names = get_params_list(files[0])
    col_names.insert(0, 'ObjectiveValue')
    write_params(col_names, path_out, filename_out)
    write_all_fits(files, path_out, filename_out)


def get_input_files(path):
    """
    Retrieve the input files in a path.

    :param path: the path containing the input files to retrieve
    :return: the list of input files
    """
    files = glob.glob(os.path.join(path, "*.csv"))
    files.sort(key=nat_sort_key)
    return files


def get_params_list(filein):
    """
    Return the list of parameter names from filein

    :param filein: a report file
    :return: the list of parameter names
    """
    with open(filein, 'r') as file:
        header = file.readline().strip('\n')
    parameters = header.split('\t')
    parameters.remove(parameters[0])
    return parameters


def write_params(col_names, path_out, filename_out):
    """
    Write the list of parameter names to filename_out

    :param col_names: the list of parameter names
    :param path_out: the path to store filename_out
    :param filename_out: the output file to store the parameter names
    """
    with open(os.path.join(path_out, filename_out), 'w') as file:
        i = -1
        for param in col_names:
            i += 1
            if i < len(col_names) - 1:
                file.write(param + '\t')
            else:
                file.write(param + '\n')


def write_best_fits(files, path_out, filename_out):
    """
    Write the final estimates to filename_out

    :param files: the list of parameter estimation reports
    :param path_out: the path to store the file combining the final (best) estimates (filename_out)
    :param filename_out: the file containing the final (best) estimates
    """
    logger.info("\nCollecting results:")
    with open(os.path.join(path_out, filename_out), 'a') as fileout:
        for filein in files:
            with open(filein, 'r') as file:
                logger.info(os.path.basename(filein))
                lines = file.readlines()
                fileout.write(os.path.basename(filein) + '\t' + lines[len(lines)-1])


def write_all_fits(files, path_out, filename_out):
    """
    Write all the estimates to filename_out

    :param files: the list of parameter estimation reports
    :param path_out: the path to store the file combining all the estimates
    :param filename_out: the file containing all the estimates
    """
    # logger.info("\nCollecting results:")
    with open(os.path.join(path_out, filename_out), 'a') as fileout:
        for file in files:
            with open(file, 'r') as filein:
                # logger.info(os.path.basename(file))
                # skip the first line (header)
                filein.readline()
                # read the remaining lines
                lines = filein.readlines()
                for line in lines:
                    fileout.write(line)


# Utilities for editing and moving the report files generated by simulators
###########################################################################


def replace_str_pl_report(report):
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


def move_report_files(outputdir, group_model, groupid):
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
        replace_str_pl_report(file)
        # rename and move the output file
        shutil.move(file, os.path.join(outputdir, file.replace(groupid, "_")[:-4] + ".csv"))

