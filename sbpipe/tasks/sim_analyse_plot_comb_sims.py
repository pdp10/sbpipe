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


def sim_analyse_plot_comb_sims(inputdir,
                               outputdir,
                               model,
                               exp_dataset,
                               plot_exp_dataset,
                               exp_dataset_alpha,
                               xaxis_label,
                               yaxis_label,
                               variable):
    """
    Plot model simulation time courses (Python wrapper).

    :param inputdir: the directory containing the data to analyse
    :param outputdir: the output directory containing the results
    :param model: the model name
    :param exp_dataset: the full path of the experimental data set
    :param plot_exp_dataset: True if the experimental data set should also be plotted
    :param exp_dataset_alpha: the alpha level for the data set
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    :param variable: the model variable to analyse
    """

    if float(exp_dataset_alpha) > 1.0 or float(exp_dataset_alpha) < 0.0:
        logger.warning("variable exp_dataset_alpha must be in [0,1]. Please, check your configuration file.")
        exp_dataset_alpha = 1.0

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_comb_sims(\"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + model + \
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
    logger.debug(command)
    run_cmd(command)


# this is a Python wrapper for sim analysis in R.
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir')
    parser.add_argument('--outputdir')
    parser.add_argument('-m', '--model')
    parser.add_argument('--exp-dataset')
    parser.add_argument('--plot-exp-dataset')
    parser.add_argument('--exp-dataset-alpha')
    parser.add_argument('--xaxis-label')
    parser.add_argument('--yaxis-label')
    parser.add_argument('--variable')

    args = parser.parse_args()
    sim_analyse_plot_comb_sims(args.inputdir,
                               args.outputdir,
                               args.model,
                               args.exp_dataset,
                               args.plot_exp_dataset,
                               args.exp_dataset_alpha,
                               args.xaxis_label,
                               args.yaxis_label,
                               args.variable)
    return 0


if __name__ == "__main__":
    sys.exit(main())
