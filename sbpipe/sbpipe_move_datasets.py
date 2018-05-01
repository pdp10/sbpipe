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
# $Date: 2016-11-02 10:18:32 $

import argparse
import glob
import os
import errno
import shutil
from os.path import basename
import sys

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)
from sbpipe.utils.io import replace_str_in_file


def get_index(name='', output_path='.'):
    """
    Get the largest index of the reports in output_path
    :param name: the name of the report
    :param output_path: the output path storing reports
    :return: the largest index or -1 if no file was found
    """
    files = glob.glob(os.path.join(output_path, name) + '_' + '*')
    print('Existing files in `' + output_path + '` : ' + str(len(files)))
    # print(files)
    # +1 is because the dataset include an underscore between the name and the sequence number
    name_length = len(name) + 1
    numbers = [-1]
    for my_file in files:
        # get the base name without extension
        f = basename(my_file).split('.')[0]
        numbers.append(int(f[name_length:]))
    return max(numbers)


def move_dataset(name='', input_path='', output_path=''):
    """
    Move data sets from one path to another and update the sequence number.

    :param name: the model name without extension
    :param input_path: the path containing the input files
    :param output_path: the path to store the output files
    """

    try:
        os.makedirs(output_path)
        print('Created missing output directory `' + output_path + '`')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # get the last index
    index = get_index(name, output_path)
    # update the index
    index += 1
    files = glob.glob(os.path.join(input_path, name) + '_' + '*')
    print('Files to copy from `' + input_path + '` to `' + output_path + '` : ' + str(len(files)))
    for filein in files:
        # get the base name extension
        ext = basename(filein).split('.')[1]
        fileout = os.path.join(output_path, name + '_' + str(index) + '.' + ext)
        shutil.move(filein, fileout)
        replace_str_in_file(fileout, basename(filein).split('.')[0], basename(fileout).split('.')[0])
        index += 1


def main(argv=None):
    """
    Move data sets from one Path to another and update the sequence number.
    """
    parser = argparse.ArgumentParser(prog='sbpipe_move_datasets',
                                     description='SBpipe script to move data sets from one path to another '
                                                 'and update the sequence number.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''
Report bugs to sbpipe@googlegroups.com
SBpipe home page: <https://github.com/pdp10/sbpipe>
For complete documentation, see http://sbpipe.readthedocs.io .
    ''')

    parser.add_argument('-n', '--model-name',
                        help='the model name without extension',
                        metavar='NAME',
                        required=True,
                        nargs=1)
    parser.add_argument('-i', '--input-path',
                        help='the path containing the input files',
                        metavar='PATH',
                        required=True,
                        nargs=1)
    parser.add_argument('-o', '--output-path',
                        help='the path to store the output files',
                        metavar='PATH',
                        required=True,
                        nargs=1)

    args = parser.parse_args()

    name = args.model_name[0]
    input_path = args.input_path[0]
    output_path = args.output_path[0]

    move_dataset(name=name, input_path=input_path, output_path=output_path)


if __name__ == "__main__":
    main()
