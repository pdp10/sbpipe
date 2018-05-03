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


import shutil
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def generic_postproc(infile, outfile, copasi=True):
    """
    Perform post processing file editing for the `simulate` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    shutil.copy(infile, outfile)
    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()
    simulator.replace_str_in_report(outfile)
    # print(command)


def sim_postproc(infile, outfile, copasi=True):
    """
    Perform post processing file editing for the `simulate` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    generic_postproc(infile, outfile, copasi)

