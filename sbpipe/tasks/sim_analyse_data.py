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
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul

from sbpipe.utils.re_utils import escape_special_chars
from sbpipe.utils.parcomp import run_cmd


def sim_analyse_data(model, inputdir, outputdir, sim_plots_dir, variable, exp_dataset, plot_exp_dataset,
                     exp_dataset_alpha, xaxis_label='', yaxis_label='', copasi=True):
    """
    Plot model simulation time courses (Python wrapper).

    :param model: the model name
    :param inputdir: the directory containing the data to analyse
    :param outputdir: the output directory containing the results
    :param sim_plots_dir: the directory to save the plots
    :param variable: the model variable to analyse
    :param exp_dataset: the full path of the experimental data set
    :param plot_exp_dataset: True if the experimental data set should also be plotted
    :param exp_dataset_alpha: the alpha level for the data set
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    """

    if float(exp_dataset_alpha) > 1.0 or float(exp_dataset_alpha) < 0.0:
        logger.warning("variable exp_dataset_alpha must be in [0,1]. Please, check your configuration file.")
        exp_dataset_alpha = 1.0

    sim_data_by_var_dir = os.path.join(outputdir, "simulate_data_by_var")
    from sbpipe.utils.io import refresh
    refresh(sim_data_by_var_dir, os.path.splitext(model)[0] + "_" + variable)

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R -e \'library(sbpiper); sbpipe_sim(\"' + model + \
              '\", \"' + inputdir + '\", \"' + sim_plots_dir + \
              '\", \"' + os.path.join(outputdir, 'sim_stats_' + model + '_' + variable + '.csv') + \
              '\", \"' + os.path.join(sim_data_by_var_dir, model + '.csv') + \
              '\", \"' + exp_dataset + \
              '\", ' + str(plot_exp_dataset).upper() + \
              ', \"' + str(exp_dataset_alpha)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + xaxis_label + \
               '\", \"' + yaxis_label + \
               '\", \"' + variable + \
               '\")\''
    run_cmd(command)


# this is a Python wrapper for sim analysis in R.
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')
    parser.add_argument('--inputdir')
    parser.add_argument('--outputdir')
    parser.add_argument('--sim-plots-dir')
    parser.add_argument('--variable')
    parser.add_argument('--exp-dataset')
    parser.add_argument('--plot-exp-dataset')
    parser.add_argument('--exp-dataset-alpha')
    parser.add_argument('--xaxis-label')
    parser.add_argument('--yaxis-label')
    parser.add_argument('-c', '--copasi', action="store_true")

    args = parser.parse_args()
    sim_analyse_data(args.model, args.inputdir, args.outputdir, args.sim_plots_dir, args.variable, \
                     args.exp_dataset, args.plot_exp_dataset, args.exp_dataset_alpha, \
                     args.xaxis_label, args.yaxis_label, args.copasi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
