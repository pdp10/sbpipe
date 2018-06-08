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


import re
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
        header = filein.readline()
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
            for line in filein:
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

