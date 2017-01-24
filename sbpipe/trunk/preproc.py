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


def generic_preproc(inputdir, outputdir, model):
    """
    Copy the model file

    :param inputdir: the input directory
    :param outputdir: the output directory
    :param model: the model file name
    """
    shutil.copyfile(os.path.join(inputdir, model), os.path.join(outputdir, model))


def copasi_preproc(inputdir, outputdir, model, id):
    """
    Replicate a copasi model `runs` times

    :param inputdir: the input directory
    :param outputdir: the output directory
    :param model: the model file name
    :param id: the number of the model
    """
    shutil.copyfile(os.path.join(inputdir, model), os.path.join(outputdir, os.path.splitext(model)[0]) + '_' + id + ".cps")
    replace_str_in_file(os.path.join(outputdir, os.path.splitext(model)[0]) + '_' + id + ".cps",
                        os.path.splitext(model)[0] + ".csv",
                        os.path.splitext(model)[0] + '_' + id + ".csv")


# python preproc.py -i Models -o preproc -m insulin_receptor.cps -d 1 -c

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputdir', default='Models')
    parser.add_argument('-o', '--outputdir', default='preproc')
    parser.add_argument('-m', '--model', default='model')
    parser.add_argument('-d', '--id', default=1)
    parser.add_argument('-c', '--copasi', action="store_true")
    args = parser.parse_args()
    if args.copasi:
        copasi_preproc(args.inputdir, args.outputdir, args.model, args.id)
    else:
        generic_preproc(args.inputdir, args.outputdir, args.model)
    return 0


if __name__ == "__main__":
    sys.exit(main())
