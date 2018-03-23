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

def pe_parameter_pca_analysis(model_name,
                              filename,
                              plots_dir,
                              best_fits_percent=100):
    """
    PCA for the best fits of the estimated parameters.

    :param model_name: the model name without extension
    :param filename: the filename containing the fits sequence
    :param plots_dir: the directory for storing the plots
    :param best_fits_percent: the percent of best fits to analyse. Only used if thres="BestFits".
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); parameter_pca_analysis(\"' + model_name + \
              '\", \"' + filename + \
              '\", \"' + plots_dir + \
              '\", ' + str(best_fits_percent)
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
    parser.add_argument('--plots-dir')
    parser.add_argument('--best-fits-percent')
    args = parser.parse_args()
    pe_parameter_pca_analysis(args.model_name,
                              args.filename,
                              args.plots_dir,
                              args.best_fits_percent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
