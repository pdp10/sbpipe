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
from itertools import islice
import shutil
import argparse
import logging
logger = logging.getLogger('sbpipe')

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def ps1_header_init(report, scanned_par):
    """
    Header report initialisation for single parameter scan pipeline.

    :param report: a report
    :param scanned_par: the scanned parameter

    :return a list containing the header or an empty list if no header was created.
    """

    header = ['Time']
    # Find the index of scanned_par in the header file, so it is possible to read the amount at
    # the second line.
    logger.debug("Retrieving column index for " + scanned_par +
                 " from file " + report)
    # Read the first line of a file.
    with open(report) as myfile:
        # 1 is the number of lines to read, 0 is the i-th element to extract from the list.
        header = list(islice(myfile, 1))[0].replace('\n', '').split('\t')
    logger.debug(header)
    # Prepare the Header for the output files
    # Add a \t at the end of each element of the header
    header = [h + '\t' for h in header]
    # Remove the \t for the last element.
    header[-1] = header[-1].strip()
    return header


def generic_postproc(infile,
                     outfile,
                     scanned_par,
                     simulate_intervals,
                     single_param_scan_intervals,
                     copasi=True):
    """
    Perform post processing organisation to single parameter scan report files.

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param scanned_par: the scanned parameter
    :param simulate_intervals: the time step of each simulation
    :param single_param_scan_intervals: the number of scans to perform
    :param copasi: True if the model is a Copasi model
    """

    scanned_par_index = -1
    scanned_par_level = -1
    # Set the number of intervals
    intervals = int(single_param_scan_intervals) + 1
    # Set the number of timepoints
    timepoints = int(simulate_intervals) + 1
    # repeat number (this is the number before the file extension)
    rep = re.findall('\d+', os.path.basename(infile))[-1]

    shutil.copy(infile, outfile)

    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()
    simulator.replace_str_in_report(outfile)

    header = ps1_header_init(outfile, scanned_par)
    if not header:
        return

    for j, name in enumerate(header):
        # remove \n and \t from name
        name = ''.join(name.split())
        logger.debug(str(j) + " " + name + " " + scanned_par)
        if name == scanned_par:
            scanned_par_index = j
            break
    if scanned_par_index == -1:
        logger.error("Column index for " + scanned_par + ": " + str(
            scanned_par_index) + ". Species not found! You must add " + scanned_par +
                     " to the Copasi report.")
        return
    else:
        logger.debug("Column index for " + scanned_par + ": " + str(scanned_par_index))

    logger.debug(outfile)

    # Prepare the table content for the output files
    for j in range(0, intervals):
        # Read the scanned_par level
        # Read the second line of a file.

        with open(outfile, 'r') as myfile:
            # 2 is the number of lines to read, 1 is the i-th element to extract from the list.
            initial_configuration = list(islice(myfile, 2))[1].replace("\n", "").split('\t')
            # print(initial_configuration)
            scanned_par_level = initial_configuration[scanned_par_index]

        if scanned_par_level == -1:
            logger.error("scanned_par_level not configured!")
            return
        else:
            logger.debug(
                scanned_par + " level: " + str(scanned_par_level) + " (list index: " + str(
                    scanned_par_index) + ")")

        # copy the -th run to a new file: add 1 to timepoints because of the header.
        round_scanned_par_level = scanned_par_level
        # Read the first timepoints+1 lines of a file.
        with open(outfile, 'r') as myfile:
            table = list(islice(myfile, timepoints + 1))

        # Write the extracted table to a separate file
        filename = os.path.splitext(outfile)[0].replace('_'+rep, '') + \
            "__rep_" + rep + "__level_" + str(round_scanned_par_level) + ".csv"
        with open(filename, 'w') as myfile:
            for line in table:
                myfile.write(line)

        with open(outfile, 'r') as myfile:
            # read all lines
            lines = myfile.readlines()

        with open(outfile + "~", 'w') as myfile:
            myfile.writelines(header)
            myfile.writelines(lines[timepoints + 1:])

        shutil.move(outfile + "~", outfile)


def ps1_postproc(infile,
                 outfile,
                 scanned_par,
                 simulate_intervals,
                 single_param_scan_intervals,
                 copasi=True):
    """
    Perform post processing organisation to single parameter scan report files.

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param scanned_par: the scanned parameter
    :param simulate_intervals: the time step of each simulation
    :param single_param_scan_intervals: the number of scans to perform
    :param copasi: True if the model is a Copasi model
    """
    generic_postproc(infile, outfile, scanned_par, simulate_intervals, single_param_scan_intervals, copasi)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    parser.add_argument('-o', '--output-file')
    parser.add_argument('-a', '--scanned-par')
    parser.add_argument('-s', '--sim-intervals', default=1)
    parser.add_argument('-p', '--ps1-intervals', default=1)
    parser.add_argument('-c', '--copasi', action="store_true")
    args = parser.parse_args()
    ps1_postproc(args.input_file,
                 args.output_file,
                 args.scanned_par,
                 int(args.sim_intervals),
                 int(args.ps1_intervals),
                 args.copasi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
