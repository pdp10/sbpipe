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
import re
import argparse
import logging
logger = logging.getLogger('sbpipe')

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def generic_postproc(infile,
                     outfile,
                     sim_length,
                     copasi=True):
    """
    Perform post processing organisation to double parameter scan report files.

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param sim_length: the length of the simulation
    :param copasi: True if the model is a Copasi model
    """

    # copy file removing empty lines
    with open(infile, 'r') as filein, \
            open(outfile, 'w') as fileout:
        for line in filein:
            if not line.isspace():
                fileout.write(line)

    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()
    simulator.replace_str_in_report(outfile)

    # Extract a selected time point from all perturbed time courses contained in the report file
    with open(outfile, 'r') as filein:
        lines = filein.readlines()
        header = lines[0]
        lines = lines[1:]
        timepoints = list(range(0, sim_length + 1))
        filesout = []
        try:
            rep = re.findall(r'_\d+.csv', outfile)[0]

            filetemplate = outfile.replace(rep, '')
            filesout = [open(filetemplate + '__rep' + rep[:-4] + '__tp_%d.csv' % k, 'w') for k in timepoints]
            # copy the header
            for fileout in filesout:
                fileout.write(header)
            # extract the i-th time point and copy it to the corresponding i-th file
            for line in lines:
                tp = line.rstrip().split('\t')[0]
                if '.' not in tp and int(tp) in timepoints:
                    filesout[int(tp)].write(line)
        finally:
            for fileout in filesout:
                fileout.close()


def ps2_postproc(infile,
                 outfile,
                 sim_length,
                 copasi=True):
    """
    Perform post processing organisation to double parameter scan report files.

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param sim_length: the length of the simulation
    :param copasi: True if the model is a Copasi model
    """
    generic_postproc(infile, outfile, sim_length, copasi)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-o', '--output-file')
    parser.add_argument('-l', '--sim-length', default=1)
    parser.add_argument('-c', '--copasi', action="store_true")
    args = parser.parse_args()
    ps2_postproc(args.input_file,
                 args.output_file,
                 int(args.sim_length),
                 args.copasi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
