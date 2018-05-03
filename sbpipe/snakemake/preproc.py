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
import shutil
from sbpipe.utils.io import replace_str_in_file


def generic_preproc(infile, outfile):
    """
    Copy the model file

    :param infile: the input file
    :param outfile: the output file
    """
    shutil.copyfile(infile, outfile)


def copasi_preproc(infile, outfile):
    """
    Replicate a copasi model and adds an id.

    :param infile: the input file
    :param outfile: the output file
    """

    generic_preproc(infile, outfile)
    replace_str_in_file(outfile,
                        os.path.splitext(os.path.basename(infile))[0] + ".csv",
                        os.path.splitext(os.path.basename(outfile))[0] + ".csv")
    replace_str_in_file(outfile,
                        os.path.splitext(os.path.basename(infile))[0] + ".txt",
                        os.path.splitext(os.path.basename(outfile))[0] + ".csv")
    replace_str_in_file(outfile,
                        os.path.splitext(os.path.basename(infile))[0] + ".tsv",
                        os.path.splitext(os.path.basename(outfile))[0] + ".csv")
    replace_str_in_file(outfile,
                        os.path.splitext(os.path.basename(infile))[0] + ".dat",
                        os.path.splitext(os.path.basename(outfile))[0] + ".csv")


def preproc(infile, outfile, copasi=False):
    """
    Replicate a copasi model and adds an id.

    :param infile: the input file
    :param outfile: the output file
    :param copasi: True if the model is a Copasi model
    """
    if copasi:
        copasi_preproc(infile, outfile)
    else:
        generic_preproc(infile, outfile)

