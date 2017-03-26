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

from sbpipe.utils.re_utils import escape_special_chars
from sbpipe.utils.parcomp import run_cmd


def sim_analyse_data(model, inputdir, outputdir, sim_plots_dir, exp_dataset, plot_exp_dataset,
                     xaxis_label='', yaxis_label=''):
    """
    Plot model simulation time courses (Python wrapper).

    :param model: the model name
    :param inputdir: the directory containing the data to analyse
    :param outputdir: the output directory containing the results
    :param sim_plots_dir: the directory to save the plots
    :param exp_dataset: the full path of the experimental data set
    :param plot_exp_dataset: True if the experimental data set should also be plotted
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    """

    ## TODO ALTHOUGH THIS WORKS, IT escapes snakemake checkpoints.
    ## TODO this should be passed as parameter and checked as a rule output
    sim_data_by_var_dir = os.path.join(outputdir, "simulate_data_by_var")
    from sbpipe.utils.io import refresh
    refresh(sim_data_by_var_dir, os.path.splitext(model)[0])

    command = 'Rscript --vanilla ' + os.path.join(SBPIPE, 'sbpipe', 'R', 'sbpipe_sim_main.r') + \
              ' ' + model + ' ' + inputdir + ' ' + sim_plots_dir + \
              ' ' + os.path.join(outputdir, 'sim_stats_' + model + '.csv') + \
              ' ' + os.path.join(sim_data_by_var_dir, model + '.csv') + \
              ' ' + exp_dataset + ' ' + str(plot_exp_dataset)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += ' ' + escape_special_chars(xaxis_label) + ' ' + escape_special_chars(yaxis_label)

    run_cmd(command)


# this is a Python wrapper for sim analysis in R.
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')
    parser.add_argument('--inputdir')
    parser.add_argument('--outputdir')
    parser.add_argument('--sim-plots-dir')
    parser.add_argument('--exp-dataset')
    parser.add_argument('--plot-exp-dataset')
    parser.add_argument('--xaxis-label')
    parser.add_argument('--yaxis-label')

    args = parser.parse_args()
    sim_analyse_data(args.model, args.inputdir, args.outputdir, args.sim_plots_dir, \
                     args.exp_dataset, args.plot_exp_dataset, args.xaxis_label, args.yaxis_label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
