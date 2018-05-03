#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
from itertools import islice
import shutil
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
    # print("Retrieving column index for " + scanned_par + " from file " + report)
    # Read the first line of a file.
    with open(report) as myfile:
        # 1 is the number of lines to read, 0 is the i-th element to extract from the list.
        header = list(islice(myfile, 1))[0].replace('\n', '').split('\t')
    # print(header)
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
        # print(str(j) + " " + name + " " + scanned_par)
        if name == scanned_par:
            scanned_par_index = j
            break
    if scanned_par_index == -1:
        print("Column index for " + scanned_par + ": " + str(
            scanned_par_index) + ". Species not found! You must add " + scanned_par +
                     " to the Copasi report.")
        return
    else:
        # print("Column index for " + scanned_par + ": " + str(scanned_par_index))
        pass

    # print(outfile)

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
            print("scanned_par_level not configured!")
            return
        else:
            # print(scanned_par + " level: " + str(scanned_par_level) + " (list index: " + str(scanned_par_index) + ")")
            pass

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

