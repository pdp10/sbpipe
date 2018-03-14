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
import traceback
import logging
logger = logging.getLogger('sbpipe')

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)

from sbpipe.pl import pipeline


def model_checking(infile, fileout, task_name):
    """
    Check the consistency for the COPASI file.

    :param infile: the input file
    :param fileout: the output file
    :param task_name: the name of the task (Copasi models)
    :return: False if model checking can be executed and fails or if the COPASI simulator is not found.
    """

    try:
        copasi = pipeline.Pipeline.get_simul_obj('Copasi')
    except TypeError as e:
        logger.error("simulator: copasi not found.")
        logger.debug(traceback.format_exc())
        return False

    return copasi.model_checking(infile, fileout, task_name)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-o', '--output-file')
    parser.add_argument('-t', '--task-name')
    args = parser.parse_args()
    model_checking(args.input_file,
                   args.output_file,
                   args.task_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
