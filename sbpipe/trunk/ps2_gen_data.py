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

from utils import call_proc


def run_copasi_model(inputdir, model):
    """
    Run a Copasi model

    :param inputdir: the directory containing the model
    :param model: the model to process
    """
    command = "CopasiSE " + os.path.join(inputdir, model)
    call_proc(command)


def run_generic_model(inputdir, model, simulator, opts):
    """
    Run a generic model

    :param inputdir: the directory containing the model
    :param model: the model to process
    :param simulator: the simulator name (e.g. Rscript, python, java, octave)
    :param opts: the simulator options
    """
    command = simulator + " " + opts + " " + os.path.join(inputdir, model) + \
              " " + model[:-4] + ".csv"
    call_proc(command)


# python ps2_gen_data.py -i Models -o preproc -m insulin_receptor.cps -r 5 -c


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputdir', default='Models')
    parser.add_argument('-m', '--model', default='model')
    parser.add_argument('-c', '--copasi', action='store_true')
    parser.add_argument('-s', '--sim-opts', default=' ')
    args = parser.parse_args()
    if args.copasi:
        run_copasi_model(args.inputdir, args.model)
    else:
        run_generic_model(args.inputdir, args.model, args.sim_opts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
