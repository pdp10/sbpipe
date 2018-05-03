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


def sim_analyse_gen_stats_table(inputfile,
                                outputfile,
                                variable):
    """
    Plot model simulation time courses (Python wrapper).

    :param inputfile: the file containing the repeats
    :param outputfile: the output file containing the statistics
    :param variable: the model variable to analyse
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); gen_stats_table(\"' + inputfile + \
              '\", \"' + outputfile
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + variable + \
               '\")\''
    # print(command)
    run_cmd(command)


def sim_analyse_summarise_data(inputdir,
                               model,
                               outputfile_repeats,
                               variable):
    """
    Plot model simulation time courses (Python wrapper).

    :param inputdir: the directory containing the data to analyse
    :param model: the model name
    :param outputfile_repeats: the output file containing the model simulation repeats
    :param variable: the model variable to analyse
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); summarise_data(\"' + inputdir + \
              '\", \"' + model + \
              '\", \"' + outputfile_repeats
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + variable + \
               '\")\''
    # print(command)
    run_cmd(command)


def sim_analyse_plot_sep_sims(inputdir,
                              outputdir,
                              model,
                              exp_dataset,
                              plot_exp_dataset,
                              exp_dataset_alpha,
                              xaxis_label,
                              yaxis_label,
                              variable):
    """
    Plot model simulation time courses (Python wrapper).

    :param inputdir: the directory containing the data to analyse
    :param outputdir: the output directory containing the results
    :param model: the model name
    :param exp_dataset: the full path of the experimental data set
    :param plot_exp_dataset: True if the experimental data set should also be plotted
    :param exp_dataset_alpha: the alpha level for the data set
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    :param variable: the model variable to analyse
    """

    if float(exp_dataset_alpha) > 1.0 or float(exp_dataset_alpha) < 0.0:
        print("variable exp_dataset_alpha must be in [0,1]. Please, check your configuration file.")
        exp_dataset_alpha = 1.0

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_sep_sims(\"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + model + \
              '\", \"' + exp_dataset + \
              '\", ' + str(plot_exp_dataset).upper() + \
              ', \"' + str(exp_dataset_alpha)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + xaxis_label + \
               '\", \"' + yaxis_label + \
               '\", \"' + variable + \
               '\")\''
    # print(command)
    run_cmd(command)


def sim_analyse_plot_comb_sims(inputdir,
                               outputdir,
                               model,
                               exp_dataset,
                               plot_exp_dataset,
                               exp_dataset_alpha,
                               xaxis_label,
                               yaxis_label,
                               variable):
    """
    Plot model simulation time courses (Python wrapper).

    :param inputdir: the directory containing the data to analyse
    :param outputdir: the output directory containing the results
    :param model: the model name
    :param exp_dataset: the full path of the experimental data set
    :param plot_exp_dataset: True if the experimental data set should also be plotted
    :param exp_dataset_alpha: the alpha level for the data set
    :param xaxis_label: the label for the x axis (e.g. Time [min])
    :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
    :param variable: the model variable to analyse
    """

    if float(exp_dataset_alpha) > 1.0 or float(exp_dataset_alpha) < 0.0:
        print("variable exp_dataset_alpha must be in [0,1]. Please, check your configuration file.")
        exp_dataset_alpha = 1.0

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_comb_sims(\"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + model + \
              '\", \"' + exp_dataset + \
              '\", ' + str(plot_exp_dataset).upper() + \
              ', \"' + str(exp_dataset_alpha)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\", \"' + xaxis_label + \
               '\", \"' + yaxis_label + \
               '\", \"' + variable + \
               '\")\''
    # print(command)
    run_cmd(command)

