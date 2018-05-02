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

