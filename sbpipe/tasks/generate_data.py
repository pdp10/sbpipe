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
from sbpipe.sbpipe_config import which
import argparse
import logging
logger = logging.getLogger('sbpipe')

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(SBPIPE)

from sbpipe.utils.parcomp import run_cmd


def run_copasi_model(infile):
    """
    Run a Copasi model

    :param infile: the input file
    """
    command = which("CopasiSE") + " " + infile
    run_cmd(command)


def run_generic_model(infile):
    """
    Run a generic model

    :param infile: the input file
    """
    command = which("python") + " " + infile + \
              " " + os.path.basename(infile)[:-4] + ".csv"
    run_cmd(command)


def generate_data(infile, copasi=False):
    """
    Replicate a copasi model and adds an id.

    :param infile: the input file
    :param copasi: True if the model is a Copasi model
    """
    if copasi:
        run_copasi_model(infile)
    else:
        run_generic_model(infile)


# python generate_data.py -i preproc/insulin_receptor.cps -c

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-c', '--copasi', action='store_true')
    args = parser.parse_args()
    generate_data(args.input_file,
                  args.copasi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
