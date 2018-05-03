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

from sbpipe.utils.dependencies import which
from sbpipe.utils.parcomp import run_cmd


def run_copasi_model(infile):
    """
    Run a Copasi model

    :param infile: the input file
    """
    command = which("CopasiSE") + " " + infile
    run_cmd(command)


def run_generic_model(infile):
    """
    Run a generic model

    :param infile: the input file
    """
    command = which("python") + " " + infile + \
              " " + os.path.basename(infile)[:-4] + ".csv"
    run_cmd(command)


def generate_data(infile, copasi=False):
    """
    Replicate a copasi model and adds an id.

    :param infile: the input file
    :param copasi: True if the model is a Copasi model
    """
    if copasi:
        run_copasi_model(infile)
    else:
        run_generic_model(infile)

