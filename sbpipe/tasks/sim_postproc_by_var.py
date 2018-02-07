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
from sbpipe.utils.io import refresh

def sim_postproc_by_var(model, outputdir, folder):
    """
    Refresh the postproc_by_var folder

    :param model: the model name
    :param outputdir: the output directory containing the results
    :param folder: the folder containing the postprocessing data by variable
    """

    sim_data_by_var_dir = os.path.join(outputdir, folder)
    refresh(sim_data_by_var_dir, os.path.splitext(model)[0])


# this is a Python wrapper for sim postproc by var
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')
    parser.add_argument('--outputdir')
    parser.add_argument('--folder')

    args = parser.parse_args()
    sim_postproc_by_var(args.model, args.outputdir, args.folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
