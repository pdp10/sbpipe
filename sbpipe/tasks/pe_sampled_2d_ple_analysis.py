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



import os
import sys
import argparse
import logging
logger = logging.getLogger('sbpipe')

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)

from sbpipe.utils.parcomp import run_cmd

def pe_sampled_2d_ple_analysis(model_name,
                               filename,
                               parameter1,
                               parameter2,
                               plots_dir,
                               thres="BestFits",
                               best_fits_percent=100,
                               fileout_param_estim_summary="",
                               logspace=True,
                               scientific_notation=True):
    """
    2D profile likelihood estimation analysis.

    :param model_name: the model name without extension
    :param filename: the filename containing the fits sequence
    :param parameter1: the name of the first parameter
    :param parameter2: the name of the second parameter
    :param plots_dir: the directory for storing the plots
    :param thres: the threshold used to filter the dataset. Values: "BestFits", "CL66", "CL95", "CL99", "All".
    :param best_fits_percent: the percent of best fits to analyse. Only used if thres="BestFits".
    :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation. Only used if thres!="BestFits".
    :param logspace: true if the parameters should be plotted in logspace
    :param scientific_notation: true if the axis labels should be plotted in scientific notation
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); sampled_2d_ple_analysis(\"' + model_name + \
              '\", \"' + filename + \
              '\", \"' + parameter1 + \
              '\", \"' + parameter2 + \
              '\", \"' + plots_dir + \
              '\", \"' + thres + \
              '\", ' + str(best_fits_percent) + \
              ', \"' + fileout_param_estim_summary + \
              '\", ' + str(logspace).upper() + \
              ', ' + str(scientific_notation).upper()
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += ')\''
    logger.debug(command)
    run_cmd(command)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name')
    parser.add_argument('--filename')
    parser.add_argument('--parameter1')
    parser.add_argument('--parameter2')
    parser.add_argument('--plots-dir')
    parser.add_argument('--thres')
    parser.add_argument('--best-fits-percent')
    parser.add_argument('--fileout-param-estim-summary')
    parser.add_argument('--logspace')
    parser.add_argument('--scientific-notation')
    args = parser.parse_args()
    pe_sampled_2d_ple_analysis(args.model_name,
                               args.filename,
                               args.parameter1,
                               args.parameter2,
                               args.plots_dir,
                               args.thres,
                               args.best_fits_percent,
                               args.fileout_param_estim_summary,
                               args.logspace,
                               args.scientific_notation)
    return 0


if __name__ == "__main__":
    sys.exit(main())
