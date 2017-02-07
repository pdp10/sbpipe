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

from sbpipe.utils.re_utils import escape_special_chars
from sbpipe.utils.parcomp import run_cmd


def ps1_analyse_data(model_name, scanned_par, inhibition_only, outputdir,
        sim_data_folder, sim_plots_folder, repeat, percent_levels, min_level,
        max_level, levels_number, homogeneous_lines, xaxis_label, yaxis_label):
    """
    Plot model single parameter scan time courses (Python wrapper).

    :param model_name: the model name without extension
    :param scanned_par: the model variable to scan
    :param inhibition_only: true if the scanning only decreases the variable amount (inhibition only)
    :param outputdir: the output directory
    :param sim_data_folder: the name of the folder containing the simulated data
    :param sim_plots_folder: the name of the folder containing the simulated plots
    :param repeat: the simulation number
    :param percent_levels: true if scanning levels are in percent
    :param min_level: the minimum level
    :param max_level: the maximum level
    :param levels_number: the number of levels
    :param homogeneous_lines: true if lines should be plotted homogeneously
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    """
    # We do this to make sure that characters like [ or ] don't cause troubles.
    xaxis_label = escape_special_chars(xaxis_label)
    yaxis_label = escape_special_chars(yaxis_label)

    command = 'Rscript --vanilla ' + os.path.join(SBPIPE, 'sbpipe', 'R', 'sbpipe_ps1_main.r') + \
        ' ' + model_name + ' ' + scanned_par + ' ' + inhibition_only + ' ' + outputdir + \
        ' ' + sim_data_folder + ' ' + sim_plots_folder + ' ' + repeat + ' ' + percent_levels + ' ' + min_level + \
        ' ' + max_level + ' ' + levels_number + ' ' + homogeneous_lines + ' ' + xaxis_label + ' ' + yaxis_label
    run_cmd(command)


# this is a Python wrapper for ps1 analysis in R.
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')
    parser.add_argument('--scanned-par')
    parser.add_argument('--inhibition-only')
    parser.add_argument('--outputdir')
    parser.add_argument('--sim-data-folder')
    parser.add_argument('--sim-plot-folder')
    parser.add_argument('--repeat', type=int, nargs='+')
    parser.add_argument('--percent-levels')
    parser.add_argument('--min-level')
    parser.add_argument('--max-level')
    parser.add_argument('--levels-number')
    parser.add_argument('--homogeneous-lines')
    parser.add_argument('--xaxis-label')
    parser.add_argument('--yaxis-label')

    args = parser.parse_args()
    ps1_analyse_data(args.model, args.scanned_par, args.inhibition_only, args.outputdir, args.sim_data_folder, \
        args.sim_plot_folder, args.repeat, args.percent_levels, args.min_level, args.max_level, args.levels_number, \
        args.homogeneous_lines, args.xaxis_label, args.yaxis_label)
    return 0


if __name__ == "__main__":
    sys.exit(main())