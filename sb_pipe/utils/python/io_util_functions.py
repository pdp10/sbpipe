#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $



# I/O utilities

import sys
import os
import glob
import logging
logger = logging.getLogger('sbpipe')

reload(sys)  
sys.setdefaultencoding('utf8')


def refresh_directory(path, file_pattern):
    """
    Clean and create the folder if this does not exist.

    :param path: the path containing the files to remove
    :param file_pattern: the string pattern of the files to remove
    """
    if not os.path.exists(path):
        os.mkdir(path) 
    else:
        files2delete = glob.glob(os.path.join(path, file_pattern + "*"))
        for f in files2delete:
            os.remove(f)


def get_pattern_position(pattern, filename):
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


def write_matrix_on_file(path, filename_out, data):
    """
    Write the matrix results stored in data to filename_out

    :param path: the path to filename_out
    :param filename_out: the output file
    :param data: the data to store in a file
    """
    with open(os.path.join(path, filename_out), 'w') as file:
        for row in data:
            # convert a list of strings or numbers into a string with items delimited by a tab.
            concatStringList = '\t'.join(map(str, row))
            # write the string above and add a newline.
            file.write(concatStringList + "\n")

  
def replace_string_in_file(filename_out, old_string, new_string):
    """
    Replace a string with another in filename_out

    :param filename_out: the output file
    :param old_string: the old string that should be replaced
    :param new_string: the new string replacing old_string
    """
    filedata = None
    with open(filename_out, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(old_string, new_string)
    # Write the file out again
    with open(filename_out, 'w') as file:
        file.write(filedata)  
