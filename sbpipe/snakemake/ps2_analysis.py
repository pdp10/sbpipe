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


from sbpipe.utils.parcomp import run_cmd
from sbpipe.utils.dependencies import is_r_package_installed

if not is_r_package_installed('sbpiper'):
    raise Exception('R package `sbpiper` was not found. Abort.')


def ps2_analyse_plot(model,
                     scanned_par1,
                     scanned_par2,
                     inputdir,
                     outputdir,
                     id):
    """
    Plot model double parameter scan time courses (Python wrapper).

    :param model: the model name without extension
    :param scanned_par1: the 1st scanned parameter
    :param scanned_par2: the 2nd scanned parameter
    :param inputdir: the input directory
    :param outputdir: the output directory
    :param run: the simulation number
    """
    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_double_param_scan_data(\"' + model + \
              '\", \"' + scanned_par1 + '\", \"' + scanned_par2 + \
              '\", \"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + str(id)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    # print(command)
    run_cmd(command)

