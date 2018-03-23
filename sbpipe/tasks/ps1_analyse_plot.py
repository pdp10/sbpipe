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

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)

from sbpipe.utils.parcomp import run_cmd


def ps1_analyse_plot(model_name,
                     inhibition_only,
                     inputdir,
                     outputdir,
                     repeat,
                     percent_levels,
                     min_level,
                     max_level,
                     levels_number,
                     xaxis_label,
                     yaxis_label):
    """
    Plot model single parameter scan time courses (Python wrapper).

    :param model_name: the model name without extension
    :param inhibition_only: true if the scanning only decreases the variable amount (inhibition only)
    :param inputdir: the input directory containing the simulated data
    :param outputdir: the output directory that will contain the simulated plots
    :param repeat: the simulation number
    :param percent_levels: true if scanning levels are in percent
    :param min_level: the minimum level
    :param max_level: the maximum level
    :param levels_number: the number of levels
    :param homogeneous_lines: true if lines should be plotted homogeneously
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    """
    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_single_param_scan_data(\"' + model_name + \
              '\", \"' + str(inhibition_only).upper() + \
              '\", \"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + repeat + \
              '\", \"' + str(percent_levels).upper() + \
              '\", \"' + str(min_level) + \
              '\", \"' + str(max_level) + \
              '\", \"' + str(levels_number)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + xaxis_label + \
               '\", \"' + yaxis_label + \
               '\")\''
    logger.debug(command)
    run_cmd(command)


# this is a Python wrapper for ps1 analysis in R.
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')
    parser.add_argument('--inhibition-only')
    parser.add_argument('--inputdir')
    parser.add_argument('--outputdir')
    parser.add_argument('--repeat', type=int, nargs='+')
    parser.add_argument('--percent-levels')
    parser.add_argument('--min-level')
    parser.add_argument('--max-level')
    parser.add_argument('--levels-number')
    parser.add_argument('--xaxis-label')
    parser.add_argument('--yaxis-label')

    args = parser.parse_args()
    ps1_analyse_plot(args.model,
                     args.inhibition_only,
                     args.inputdir,
                     args.outputdir,
                     args.repeat,
                     args.percent_levels,
                     args.min_level,
                     args.max_level,
                     args.levels_number,
                     args.xaxis_label,
                     args.yaxis_label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
