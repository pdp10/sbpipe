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
import sys
import argparse
import shutil

SBPIPE = os.environ["SBPIPE"]
sys.path.insert(0, SBPIPE)

from sbpipe.utils.io import replace_str_in_file


def generic_preproc(infile, outfile):
    """
    Copy the model file

    :param infile: the input file
    :param outfile: the output file
    """
    shutil.copyfile(infile, outfile)


def copasi_preproc(infile, outfile):
    """
    Replicate a copasi model and adds an id.

    :param infile: the input file
    :param outfile: the output file
    """
    generic_preproc(infile, outfile)
    replace_str_in_file(outfile,
                        os.path.splitext(os.path.basename(infile))[0] + ".csv",
                        os.path.splitext(os.path.basename(outfile))[0] + ".csv")


# python preproc.py -i Models/insulin_receptor.cps -o preproc/insulin_receptor_1.cps -c

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-o', '--output-file')
    parser.add_argument('-c', '--copasi', action="store_true")
    args = parser.parse_args()
    if args.copasi:
        copasi_preproc(args.input_file, args.output_file)
    else:
        generic_preproc(args.input_file, args.output_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
