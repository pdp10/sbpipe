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



def pe_analyse_data_all_fits(model, outputdir, fileout_all_estims,
                     fileout_param_estim_details, fileout_param_estim_summary, plots_dir,
                     data_point_num,
                     plot_2d_66cl_corr=False, plot_2d_95cl_corr=False, plot_2d_99cl_corr=False,
                     logspace=True, scientific_notation=True):
    """
    Plot parameter estimation results (Python wrapper).

        :param model: the model name
        :param outputdir: the directory to store the results
        :param fileout_all_estims: the name of the file containing all the parameter sets with the objective value
        :param fileout_param_estim_details: the name of the file containing the detailed statistics for the \
        estimated parameters
        :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation
        :param plots_dir: the directory of the simulation plots
        :param data_point_num: the number of data points
        :param plot_2d_66cl_corr: True if 2 dim plots for the parameter sets within 66% should be plotted
        :param plot_2d_95cl_corr: True if 2 dim plots for the parameter sets within 95% should be plotted
        :param plot_2d_99cl_corr: True if 2 dim plots for the parameter sets within 99% should be plotted
        :param logspace: True if parameters should be plotted in log space
        :param scientific_notation: True if axis labels should be plotted in scientific notation
        :return: True if the task was completed successfully, False otherwise.
    """
    # requires devtools::install_github("pdp10/r-sbpipe")
    command = 'R -e \'library(r-sbpipe); r-sbpipe:::sbpipe_pe_main_all_fits(\"' + model + \
              '\", \"' + os.path.join(outputdir, fileout_all_estims) + \
              '\", \"' + plots_dir + \
              '\", \"' + str(data_point_num) + \
              '\", \"' + os.path.join(outputdir, fileout_param_estim_details) + \
              '\", \"' + os.path.join(outputdir, fileout_param_estim_summary) + \
              '\", \"' + str(plot_2d_66cl_corr).upper() + \
              '\", \"' + str(plot_2d_95cl_corr).upper() + \
              '\", \"' + str(plot_2d_99cl_corr).upper() + \
              '\", \"' + str(logspace).upper() + \
              '\", \"' + str(scientific_notation).upper()
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''

    run_cmd(command)


# this is a Python wrapper for parameter estimation analysis in R.
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')
    parser.add_argument('--outputdir')
    parser.add_argument('--allfits-file')
    parser.add_argument('--param-estim-details-file')
    parser.add_argument('--param-estim-summary-file')
    parser.add_argument('--plots-dir')
    parser.add_argument('--best-fits-percent', type=int, nargs='+')
    parser.add_argument('--datapointnum', type=int, nargs='+')
    parser.add_argument('--plot-66cl-corr', action='store_true')
    parser.add_argument('--plot-95cl-corr', action='store_true')
    parser.add_argument('--plot-99cl-corr', action='store_true')
    parser.add_argument('--logspace', action='store_true')
    parser.add_argument('--scientific-notation', action='store_true')

    args = parser.parse_args()
    pe_analyse_data_all_fits(args.model, args.outputdir, args.allfits_file,
                    args.param_estim_details_file, args.param_estim_summary_file, args.plots_dir,
                    args.best_fits_percent, args.datapointnum,
                    args.plot_66cl_corr, args.plot_95cl_corr, args.plot_99cl_corr,
                    args.logspace, args.scientific_notation)
    return 0


if __name__ == "__main__":
    sys.exit(main())
