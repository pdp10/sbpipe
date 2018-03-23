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

def pe_combine_param_ple_stats(plots_dir,
                         fileout_param_estim_details):
    """
    Combine the statistics for the parameter estimation details

    :param plots_dir: the directory to save the generated plots
    :param fileout_param_estim_details: the name of the file containing the detailed statistics for the estimated parameters
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); combine_param_ple_stats(\"' + plots_dir + \
              '\", \"' + fileout_param_estim_details
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    logger.debug(command)
    run_cmd(command)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--plots-dir')
    parser.add_argument('--fileout-param-estim-details')
    args = parser.parse_args()
    pe_combine_param_ple_stats(args.plots_dir,
                         args.fileout_param_estim_details)
    return 0


if __name__ == "__main__":
    sys.exit(main())
