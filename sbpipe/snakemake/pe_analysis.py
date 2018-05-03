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


def pe_combine_param_best_fits_stats(plots_dir,
                                     fileout_param_estim_best_fits_details):
    """
    Combine the statistics for the parameter estimation details

    :param plots_dir: the directory to save the generated plots
    :param fileout_param_estim_best_fits_details: the name of the file containing the detailed statistics for the estimated parameters
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); combine_param_best_fits_stats(\"' + plots_dir + \
              '\", \"' + fileout_param_estim_best_fits_details
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    # print(command)
    run_cmd(command)


def pe_combine_param_ple_stats(plots_dir,
                         fileout_param_estim_details):
    """
    Combine the statistics for the parameter estimation details

    :param plots_dir: the directory to save the generated plots
    :param fileout_param_estim_details: the name of the file containing the detailed statistics for the estimated parameters
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); combine_param_ple_stats(\"' + plots_dir + \
              '\", \"' + fileout_param_estim_details
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    # print(command)
    run_cmd(command)


def pe_ds_preproc(filename,
                  param_names,
                  logspace=True,
                  all_fits=False,
                  data_point_num=0,
                  fileout_param_estim_summary="param_estim_summary.csv"):
    """
    Parameter estimation pre-processing. It renames the data set columns, and applies
    a log10 transformation if logspace is TRUE. If all.fits is true, it also computes
    the confidence levels.

    :param filename: the dataset filename containing the fits sequence
    :param param_names: the list of estimated parameter names
    :param logspace: true if the data set shoud be log10-transformed.
    :param all_fits: true if filename contains all fits, false otherwise
    :param data_point_num: the number of data points used for parameterise the model. Ignored if all.fits is false
    :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation. Ignored if all.fits is false
    """

    # convert param_names into an R vector
    param_names_r = "c("
    for i in param_names:
        param_names_r += "\"" + i + "\","
    if len(param_names) > 0:
        param_names_r = param_names_r[:-1]
    param_names_r = param_names_r + ")"

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); pe_ds_preproc(\"' + filename + \
              '\", ' + param_names_r + \
              ', ' + str(logspace).upper() + \
              ', ' + str(all_fits).upper() + \
              ', ' + str(data_point_num) + \
              ', \"' + fileout_param_estim_summary
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    # print(command)
    run_cmd(command)


def pe_objval_vs_iters_analysis(model_name,
                                filename,
                                plots_dir):
    """
    Analysis of the Objective values vs Iterations.

    :param model_name: the model name without extension
    :param filename: the filename containing the fits sequence
    :param plots_dir: the directory for storing the plots
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); objval_vs_iters_analysis(\"' + model_name + \
              '\", \"' + filename + \
              '\", \"' + plots_dir
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    # print(command)
    run_cmd(command)


def pe_parameter_density_analysis(model_name,
                                  filename,
                                  parameter,
                                  plots_dir,
                                  thres="BestFits",
                                  best_fits_percent=100,
                                  fileout_param_estim_summary="",
                                  logspace=True,
                                  scientific_notation=True):
    """
    Parameter density analysis.

    :param model_name: the model name without extension
    :param filename: the filename containing the fits sequence
    :param parameter: the name of the parameter to plot the density
    :param plots_dir: the directory for storing the plots
    :param thres: the threshold used to filter the dataset. Values: "BestFits", "CL66", "CL95", "CL99", "All".
    :param best_fits_percent: the percent of best fits to analyse. Only used if thres="BestFits".
    :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation. Only used if thres!="BestFits".
    :param logspace: true if the parameters should be plotted in logspace
    :param scientific_notation: true if the axis labels should be plotted in scientific notation
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); parameter_density_analysis(\"' + model_name + \
              '\", \"' + filename + \
              '\", \"' + parameter + \
              '\", \"' + plots_dir + \
              '\", \"' + thres + \
              '\", ' + str(best_fits_percent) + \
              ', \"' + fileout_param_estim_summary + \
              '\", ' + str(logspace).upper() + \
              ', ' + str(scientific_notation).upper()
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += ')\''
    # print(command)
    run_cmd(command)


def pe_parameter_pca_analysis(model_name,
                              filename,
                              plots_dir,
                              best_fits_percent=100):
    """
    PCA for the best fits of the estimated parameters.

    :param model_name: the model name without extension
    :param filename: the filename containing the fits sequence
    :param plots_dir: the directory for storing the plots
    :param best_fits_percent: the percent of best fits to analyse. Only used if thres="BestFits".
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); parameter_pca_analysis(\"' + model_name + \
              '\", \"' + filename + \
              '\", \"' + plots_dir + \
              '\", ' + str(best_fits_percent)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += ')\''
    # print(command)
    run_cmd(command)


def pe_sampled_2d_ple_analysis(model_name,
                               filename,
                               parameter1,
                               parameter2,
                               plots_dir,
                               thres="BestFits",
                               best_fits_percent=100,
                               fileout_param_estim_summary="",
                               logspace=True,
                               scientific_notation=True):
    """
    2D profile likelihood estimation analysis.

    :param model_name: the model name without extension
    :param filename: the filename containing the fits sequence
    :param parameter1: the name of the first parameter
    :param parameter2: the name of the second parameter
    :param plots_dir: the directory for storing the plots
    :param thres: the threshold used to filter the dataset. Values: "BestFits", "CL66", "CL95", "CL99", "All".
    :param best_fits_percent: the percent of best fits to analyse. Only used if thres="BestFits".
    :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation. Only used if thres!="BestFits".
    :param logspace: true if the parameters should be plotted in logspace
    :param scientific_notation: true if the axis labels should be plotted in scientific notation
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); sampled_2d_ple_analysis(\"' + model_name + \
              '\", \"' + filename + \
              '\", \"' + parameter1 + \
              '\", \"' + parameter2 + \
              '\", \"' + plots_dir + \
              '\", \"' + thres + \
              '\", ' + str(best_fits_percent) + \
              ', \"' + fileout_param_estim_summary + \
              '\", ' + str(logspace).upper() + \
              ', ' + str(scientific_notation).upper()
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += ')\''
    # print(command)
    run_cmd(command)


def pe_sampled_ple_analysis(model_name,
                            filename,
                            parameter,
                            plots_dir,
                            fileout_param_estim_summary,
                            logspace=True,
                            scientific_notation=True):
    """
    Run the profile likelihood estimation analysis.

    :param model_name: the model name without extension
    :param filename: the filename containing the fits sequence
    :param parameter: the parameter to compute the PLE analysis
    :param plots_dir: the directory to save the generated plots
    :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation
    :param logspace: true if parameters should be plotted in logspace
    :param scientific_notation: true if the axis labels should be plotted in scientific notation
    """

    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); sampled_ple_analysis(\"' + model_name + \
              '\", \"' + filename + \
              '\", \"' + parameter + \
              '\", \"' + plots_dir + \
              '\", \"' + fileout_param_estim_summary + \
              '\", ' + str(logspace).upper() + \
              ', ' + str(scientific_notation).upper()
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += ')\''
    # print(command)
    run_cmd(command)

