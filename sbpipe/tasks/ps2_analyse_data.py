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

from sbpipe.utils.parcomp import run_cmd


def ps2_analyse_data(model, scanned_par1, scanned_par2, inputdir, outputdir, id):
    """
    Plot model double parameter scan time courses (Python wrapper).

    :param model: the model name without extension
    :param scanned_par1: the 1st scanned parameter
    :param scanned_par2: the 2nd scanned parameter
    :param inputdir: the input directory
    :param outputdir: the output directory
    :param run: the simulation number
    """
    command = 'Rscript --vanilla ' + os.path.join(SBPIPE, 'sbpipe', 'R', 'sbpipe_ps2_main.r') + \
              ' ' + model + ' ' + scanned_par1 + ' ' + scanned_par2 + ' ' + inputdir + \
              ' ' + outputdir + ' ' + str(id)
    run_cmd(command)


# this is a Python wrapper for ps2 analysis in R.
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')
    parser.add_argument('--scanned-par1')
    parser.add_argument('--scanned-par2')
    parser.add_argument('-i', '--inputdir')
    parser.add_argument('-o', '--outputdir')
    parser.add_argument('-r', '--repeat', type=int, nargs='+')
    args = parser.parse_args()
    ps2_analyse_data(args.model, args.scanned_par1, args.scanned_par2, args.inputdir, args.outputdir, args.r)
    return 0


if __name__ == "__main__":
    sys.exit(main())