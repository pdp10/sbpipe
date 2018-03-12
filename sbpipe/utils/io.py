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
# $Date: 2015-07-13 12:14:32 $

import glob
import logging
import os
import re

logger = logging.getLogger('sbpipe')


def refresh(path, file_pattern):
    """
    Clean and create the folder if this does not exist.

    :param path: the path containing the files to remove
    :param file_pattern: the string pattern of the files to remove
    """
    if not os.path.exists(path):
        logger.debug('Creating folder ' + path)
        os.mkdir(path)
    else:
        logger.debug('Folder ' + path + ' already exists')
        files2delete = glob.glob(os.path.join(path, file_pattern + "*"))
        for f in files2delete:
            remove_file_silently(f)
        logger.debug('Folder has been cleaned')


def get_pattern_pos(pattern, filename):
    """
    Return the line number (as string) of the first occurrence of a pattern in filename

    :param pattern: the pattern of the string to find
    :param filename: the file name containing the pattern to search
    :return: the line number containing the pattern or "-1" if the pattern was not found
    """
    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if pattern in line:
                logger.debug(str(num) + " : " + pattern)
                return str(num)
    logger.debug(str(-1) + " : " + pattern)
    return str(-1)


def files_with_pattern_recur(folder, pattern):
    """
    Return all files with a certain pattern in folder+subdirectories
    
    :param folder: the folder to search for
    :param pattern: the string to search for
    :return: the files containing the pattern.
    """
    for dirname, subdirs, files in os.walk(folder):
        for f in files:
            if f.endswith(pattern):
                yield os.path.join(dirname, f)


def write_mat_on_file(fileout, data):
    """
    Write the matrix results stored in data to filename_out

    :param fileout: the output file
    :param data: the data to store in a file
    """
    with open(fileout, 'w') as file:
        for row in data:
            file.write(row + '\n')


def replace_str_in_file(filename_out, old_string, new_string):
    """
    Replace a string with another in filename_out

    :param filename_out: the output file
    :param old_string: the old string that should be replaced
    :param new_string: the new string replacing old_string
    """
    with open(filename_out, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(old_string, new_string)
    # Write the file out again
    with open(filename_out, 'w') as file:
        file.write(filedata)


def replace_str_in_report(report):
    """
    Replace nasty strings in COPASI report file.

    :param report: the report
    """

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

                # global variables
                lines[i] = lines[i].replace("Values[", "").replace(".InitialValue", "")
                # compartments
                lines[i] = lines[i].replace("Compartments[", "").replace(".InitialVolume", "").replace(".Volume", "")
                # particle numbers
                lines[i] = lines[i].replace(".InitialParticleNumber", "")
                # species
                lines[i] = lines[i].replace("Values[", "").replace("]_0", "")

                file.write(
                    re.sub(r"\s+", '\t', re.sub(r'[^\w]', " ", lines[i])).rstrip('\t') + '\n')
            else:
                file.write(lines[i].rstrip('\t'))


def remove_file_silently(filename):
    """
    Remove a filename silently, without reporting warnings or error messages. This is not really needed
    by Linux, but Windows sometimes fails to remove the file even if this exists.

    :param filename: the file to remove
    """
    try:
        os.remove(filename)
    except OSError:
        pass

