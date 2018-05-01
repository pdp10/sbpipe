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
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def pe_collect(inputdir,
               outputdir,
               fileout_final_estims,
               fileout_all_estims,
               copasi=True):
    """
    Collect the results so that they can be processed.

    :param inputdir: the input folder containing the data
    :param outputdir: the output folder to stored the collected results
    :param fileout_final_estims: the name of the file containing the best estimations
    :param fileout_all_estims: the name of the file containing all the estimations
    :param copasi: True if COPASI was used to generate the data.
    """
    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()


    # Collect and summarises the parameter estimation results
    try:
        files_num = simulator.get_best_fits(inputdir, outputdir, fileout_final_estims)
        simulator.get_all_fits(inputdir, outputdir, fileout_all_estims)
        logger.info('Files retrieved: ' + str(files_num))
    except Exception as e:
        logger.error("simulator: " + simulator + " not found.")
        import traceback
        logger.debug(traceback.format_exc())

