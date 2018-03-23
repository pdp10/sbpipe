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

def pe_ds_preproc(filename,
                  param_names,
                  logspace=True,
                  all_fits=False,
                  data_point_num=0,
                  fileout_param_estim_summary="param_estim_summary.csv"):
    """
    Parameter estimation pre-processing. It renames the data set columns, and applies
    a log10 transformation if logspace is TRUE. If all.fits is true, it also computes
    the confidence levels.

    :param filename: the dataset filename containing the fits sequence
    :param param_names: the list of estimated parameter names
    :param logspace: true if the data set shoud be log10-transformed.
    :param all_fits: true if filename contains all fits, false otherwise
    :param data_point_num: the number of data points used for parameterise the model. Ignored if all.fits is false
    :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation. Ignored if all.fits is false
    """

    # convert param_names into an R vector
    param_names_r = "c("
    for i in param_names:
        param_names_r += "\"" + i + "\","
    if len(param_names) > 0:
        param_names_r = param_names_r[:-1]
    param_names_r = param_names_r + ")"

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); pe_ds_preproc(\"' + filename + \
              '\", ' + param_names_r + \
              ', ' + str(logspace).upper() + \
              ', ' + str(all_fits).upper() + \
              ', ' + str(data_point_num) + \
              ', \"' + fileout_param_estim_summary
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    logger.debug(command)
    run_cmd(command)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename')
    parser.add_argument('--param-names')
    parser.add_argument('--logspace')
    parser.add_argument('--allfits')
    parser.add_argument('--data-point-num')
    parser.add_argument('--fileout-param-estim-summary')
    args = parser.parse_args()
    pe_ds_preproc(args.filename,
                  args.param_names,
                  args.logspace,
                  args.allfits,
                  args.data_point_num,
                  args.fileout_param_estim_summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
