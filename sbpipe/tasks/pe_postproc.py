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
import re
from itertools import islice
import shutil
import argparse
import logging
logger = logging.getLogger('sbpipe')

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def generic_postproc(infile,
                     outfile,
                     copasi=True):
    """
    Perform post processing file editing for the `pe` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    shutil.copy(infile, outfile)
    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()
    simulator.replace_str_in_report(outfile)

    logger.debug(outfile)


def pe_postproc(infile,
                outfile,
                copasi=True):
    """
    Perform post processing file editing for the `pe` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    generic_postproc(infile, outfile, copasi)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-o', '--output-file')
    parser.add_argument('-c', '--copasi', action="store_true")
    args = parser.parse_args()
    pe_postproc(args.input_file,
                args.output_file,
                args.copasi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
