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


def ps1_analyse_plot(model_name,
                     inhibition_only,
                     inputdir,
                     outputdir,
                     repeat,
                     percent_levels,
                     min_level,
                     max_level,
                     levels_number,
                     xaxis_label,
                     yaxis_label):
    """
    Plot model single parameter scan time courses (Python wrapper).

    :param model_name: the model name without extension
    :param inhibition_only: true if the scanning only decreases the variable amount (inhibition only)
    :param inputdir: the input directory containing the simulated data
    :param outputdir: the output directory that will contain the simulated plots
    :param repeat: the simulation number
    :param percent_levels: true if scanning levels are in percent
    :param min_level: the minimum level
    :param max_level: the maximum level
    :param levels_number: the number of levels
    :param homogeneous_lines: true if lines should be plotted homogeneously
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    """
    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_single_param_scan_data(\"' + model_name + \
              '\", \"' + str(inhibition_only).upper() + \
              '\", \"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + repeat + \
              '\", \"' + str(percent_levels).upper() + \
              '\", \"' + str(min_level) + \
              '\", \"' + str(max_level) + \
              '\", \"' + str(levels_number)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + xaxis_label + \
               '\", \"' + yaxis_label + \
               '\")\''
    # print(command)
    run_cmd(command)


def ps1_analyse_plot_homogen(model_name,
                             inputdir,
                             outputdir,
                             repeat,
                             xaxis_label,
                             yaxis_label):
    """
    Plot model single parameter scan time courses using homogeneous lines (Python wrapper).

    :param model_name: the model name without extension
    :param inputdir: the input directory containing the simulated data
    :param outputdir: the output directory that will contain the simulated plots
    :param repeat: the simulation number
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    """
    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_single_param_scan_data_homogen(\"' + model_name + \
              '\", \"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + repeat
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + xaxis_label + \
               '\", \"' + yaxis_label + \
               '\")\''
    # print(command)
    run_cmd(command)

