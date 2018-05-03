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


import argparse
import glob
import os
import errno
import shutil
from os.path import basename
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
