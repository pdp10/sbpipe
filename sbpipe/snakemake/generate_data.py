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
import logging
logger = logging.getLogger('sbpipe')

SBPIPE = os.environ["SBPIPE"]
sys.path.insert(0, SBPIPE)

from sbpipe.snakemake.utils import call_proc


def run_copasi_model(infile):
    """
    Run a Copasi model

    :param infile: the input file
    """
    command = "CopasiSE " + infile
    call_proc(command)


def run_generic_model(infile, simulator, opts):
    """
    Run a generic model

    :param infile: the input file
    :param simulator: the simulator name (e.g. Rscript, python, java, octave)
    :param opts: the simulator options
    """
    command = simulator + " " + opts + " " + infile + \
              " " + os.path.basename(infile)[:-4] + ".csv"
    call_proc(command)


# python generate_data.py -i preproc/insulin_receptor.cps -c

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-c', '--copasi', action='store_true')
    parser.add_argument('-s', '--sim', default='CopasiSE')
    parser.add_argument('-o', '--sim-opts', default='')
    args = parser.parse_args()
    if args.copasi:
        run_copasi_model(args.input_file)
    else:
        run_generic_model(args.input_file, args.sim, args.sim_opts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
