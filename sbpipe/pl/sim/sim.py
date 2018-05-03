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


# for computing the pipeline elapsed time
import datetime
import glob
import logging
import os
import yaml
import traceback
from ..pipeline import Pipeline
from sbpipe.utils.dependencies import is_r_package_installed
from sbpipe.utils.io import refresh
from sbpipe.utils.parcomp import parcomp
from sbpipe.report.latex_reports import latex_report_sim, pdf_report

logger = logging.getLogger('sbpipe')


class Sim(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for running 
    model simulations
    """

    def __init__(self, models_folder='Models', working_folder='Results',
                 sim_data_folder='simulate_data', sim_plots_folder='simulate_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, models_folder, working_folder, sim_data_folder, sim_plots_folder)

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("================================")
        logger.info("Pipeline: time course simulation")
        logger.info("================================")

        logger.info("\n")
        logger.info("Loading file: " + config_file)
        logger.info("=============\n")

        # load the configuration file
        try:
            config_dict = Pipeline.load(config_file)
        except yaml.YAMLError as e:
            logger.error(e.message)
            logger.debug(traceback.format_exc())
            return False
        except IOError:
            logger.error('File `' + config_file + '` does not exist.')
            logger.debug(traceback.format_exc())
            return False

        # variable initialisation
        (generate_data, analyse_data, generate_report, generate_tarball,
         project_dir, simulator, model, cluster, local_cpus, runs,
         exp_dataset, plot_exp_dataset,
         exp_dataset_alpha,
         xaxis_label, yaxis_label) = self.parse(config_dict)

        runs = int(runs)
        local_cpus = int(local_cpus)
        exp_dataset_alpha = float(exp_dataset_alpha)

        models_dir = os.path.join(project_dir, self.get_models_folder())
        working_dir = os.path.join(project_dir, self.get_working_folder())
        output_folder = os.path.splitext(model)[0]
        outputdir = os.path.join(working_dir, output_folder)

        # Get the pipeline start time
        start = datetime.datetime.now().replace(microsecond=0)

        # preprocessing
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        if generate_data:
            logger.info("\n")
            logger.info("Data generation:")
            logger.info("================")
            status = Sim.generate_data(simulator,
                                       model,
                                       models_dir,
                                       os.path.join(outputdir, self.get_sim_data_folder()),
                                       cluster,
                                       local_cpus,
                                       runs)
            if not status:
                return False

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("==============")
            status = Sim.analyse_data(simulator,
                                      os.path.splitext(model)[0],
                                      os.path.join(outputdir, self.get_sim_data_folder()),
                                      outputdir,
                                      os.path.join(outputdir, self.get_sim_plots_folder()),
                                      os.path.join(models_dir, exp_dataset),
                                      plot_exp_dataset,
                                      exp_dataset_alpha,
                                      cluster,
                                      local_cpus,
                                      xaxis_label,
                                      yaxis_label)
            if not status:
                return False

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("==================")
            status = Sim.generate_report(os.path.splitext(model)[0],
                                         outputdir,
                                         self.get_sim_plots_folder())
            if not status:
                return False

        if generate_tarball:
            status = self.generate_tarball(working_dir, output_folder)
            if not status:
                return False

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        return True

    @classmethod
    def generate_data(cls, simulator, model, inputdir, outputdir, cluster="local", local_cpus=2, runs=1):
        """
        The first pipeline step: data generation.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory containing the output files
        :param cluster: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param local_cpus: the number of CPUs.
        :param runs: the number of model simulation
        :return: True if the task was completed successfully, False otherwise.
        """

        if int(local_cpus) < 1:
            logger.error("variable local_cpus must be greater than 0. Please, check your configuration file.")
            return False

        if runs < 1:
            logger.error("variable runs must be greater than 0. Please, check your configuration file.")
            return False

        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return False

        # folder preparation
        refresh(outputdir, os.path.splitext(model)[0])

        # execute runs simulations.
        logger.info("Simulating model " + model + " for " + str(runs) + " time(s)")
        try:
            sim = cls.get_simul_obj(simulator)
        except TypeError as e:
            logger.error("simulator: " + simulator + " not found.")
            logger.debug(traceback.format_exc())
            return False
        try:
            return sim.sim(model, inputdir, outputdir, cluster, local_cpus, runs, False)
        except Exception as e:
            logger.error(str(e))
            logger.debug(traceback.format_exc())
            return False

    @classmethod
    def analyse_data(cls, simulator, model, inputdir, outputdir, sim_plots_dir, exp_dataset, plot_exp_dataset,
                     exp_dataset_alpha=1.0, cluster="local", local_cpus=2, xaxis_label='', yaxis_label=''):
        """
        The second pipeline step: data analysis.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model name
        :param inputdir: the directory containing the data to analyse
        :param outputdir: the output directory containing the results
        :param sim_plots_dir: the directory to save the plots
        :param exp_dataset: the full path of the experimental data set
        :param plot_exp_dataset: True if the experimental data set should also be plotted
        :param exp_dataset_alpha: the alpha level for the data set
        :param cluster: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param local_cpus: the number of CPUs.
        :param xaxis_label: the label for the x axis (e.g. Time [min])
        :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.exists(inputdir):
            logger.error("inputdir " + inputdir + " does not exist. Generate some data first.")
            return False

        if float(exp_dataset_alpha) > 1.0 or float(exp_dataset_alpha) < 0.0:
            logger.warning("variable exp_dataset_alpha must be in [0,1]. Please, check your configuration file.")
            exp_dataset_alpha = 1.0

        sim_data_by_var_dir = os.path.join(outputdir, "simulate_data_by_var")

        # folder preparation
        refresh(sim_plots_dir, os.path.splitext(model)[0])
        refresh(sim_data_by_var_dir, os.path.splitext(model)[0])

        # Read the columns to process
        try:
            sim = cls.get_simul_obj(simulator)
        except TypeError as e:
            logger.error("simulator: " + simulator + " not found.")
            logger.debug(traceback.format_exc())
            return False
        try:
            columns = sim.get_sim_columns(inputdir)
        except Exception as e:
            logger.error(str(e))
            logger.debug(traceback.format_exc())
            return False
        str_to_replace = 'COLUMN_TO_REPLACE'

        logger.info("Analysing generated simulations:")

        # requires devtools::install_github("pdp10/sbpiper")
        if not is_r_package_installed('sbpiper'):
            logger.critical('R package `sbpiper` was not found. Abort.')
            return False
        command = 'R --quiet -e \'library(sbpiper); sbpiper_sim(\"' + model + \
                  '\", \"' + inputdir + '\", \"' + sim_plots_dir + \
                  '\", \"' + os.path.join(outputdir, 'sim_stats_' + model + '_' + str_to_replace + '.csv') + \
                  '\", \"' + os.path.join(sim_data_by_var_dir, model + '_' + str_to_replace + '.csv') + \
                  '\", \"' + exp_dataset + \
                  '\", ' + str(plot_exp_dataset).upper() + \
                  ', \"' + str(exp_dataset_alpha)

        # we replace \\ with / otherwise subprocess complains on windows systems.
        command = command.replace('\\', '\\\\')
        # We do this to make sure that characters like [ or ] don't cause troubles.
        command += '\", \"' + xaxis_label + \
                   '\", \"' + yaxis_label + \
                   '\", \"' + str_to_replace + \
                   '\")\''

        if not parcomp(command, str_to_replace, outputdir, cluster, 1, local_cpus, False, columns):
            return False

        if len(glob.glob(os.path.join(sim_plots_dir, os.path.splitext(model)[0] + '*.pdf'))) == 0:
            return False
        return True

    @classmethod
    def generate_report(cls, model, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param outputdir: the output directory to store the report
        :param sim_plots_folder: the folder containing the plots
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error(
                "inputdir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.")
            return False

        logger.info("Generating LaTeX report")
        filename_prefix = "report__simulate_"
        latex_report_sim(outputdir, sim_plots_folder, model, filename_prefix)

        logger.info("Generating PDF report")
        pdf_report(outputdir, filename_prefix + model + ".tex")

        if len(glob.glob(os.path.join(outputdir, '*' + os.path.splitext(model)[0] + '*.pdf'))) == 0:
            return False
        return True

    def parse(self, my_dict):
        __doc__ = Pipeline.parse.__doc__

        generate_data = True
        analyse_data = True
        generate_report = True
        generate_tarball = False
        project_dir = '.'
        model = 'model'
        simulator = 'Copasi'
        cluster = 'local'
        local_cpus = 1
        runs = 1
        exp_dataset = ''
        plot_exp_dataset = False
        exp_dataset_alpha = 1.0
        xaxis_label = 'Time [min]'
        yaxis_label = 'Level [a.u.]'

        # Initialises the variables
        for key, value in my_dict.items():

            logger.info(key + ": " + str(value))

            if key == "generate_data":
                generate_data = value
            elif key == "analyse_data":
                analyse_data = value
            elif key == "generate_report":
                generate_report = value
            elif key == "generate_tarball":
                generate_tarball = value
            elif key == "project_dir":
                project_dir = value
            elif key == "model":
                model = value
            elif key == "simulator":
                simulator = value
            elif key == "cluster":
                cluster = value
            elif key == "local_cpus":
                local_cpus = value
            elif key == "runs":
                runs = value
            elif key == "exp_dataset":
                exp_dataset = value
            elif key == "plot_exp_dataset":
                plot_exp_dataset = value
            elif key == "exp_dataset_alpha":
                exp_dataset_alpha = value
            elif key == "xaxis_label":
                xaxis_label = value
            elif key == "yaxis_label":
                yaxis_label = value
            else:
                logger.warning('Found unknown option: `' + key + '`')

        return (generate_data, analyse_data, generate_report, generate_tarball,
                project_dir, simulator, model,
                cluster, local_cpus, runs,
                exp_dataset, plot_exp_dataset,
                exp_dataset_alpha,
                xaxis_label, yaxis_label)
