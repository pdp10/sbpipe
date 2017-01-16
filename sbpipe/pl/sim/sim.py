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
#
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 16:14:32 $

# for computing the pipeline elapsed time
import datetime
import glob
import logging
import os
import subprocess
from ..pipeline import Pipeline
from sbpipe.utils.io import refresh
from sbpipe.report.latex_reports import latex_report_sim, pdf_report

logger = logging.getLogger('sbpipe')


class Sim(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for running 
    model simulations
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='simulate_data', sim_plots_folder='simulate_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, data_folder, models_folder, working_folder, sim_data_folder, sim_plots_folder)

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("Reading file " + config_file + " : \n")

        # variable initialisation
        try:
            (generate_data, analyse_data, generate_report,
             project_dir, simulator, model, cluster, pp_cpus, runs,
             exp_dataset, plot_exp_dataset,
             xaxis_label, yaxis_label) = self.config_parser(config_file, "simulate")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return False

        runs = int(runs)
        pp_cpus = int(pp_cpus)

        # Some controls
        if runs < 1:
            logger.error("variable `runs` must be greater than 0. Please, check your configuration file.")
            return False

        models_dir = os.path.join(project_dir, self.get_models_folder())
        outputdir = os.path.join(project_dir, self.get_working_folder(), os.path.splitext(model)[0])

        # Get the pipeline start time
        start = datetime.datetime.now().replace(microsecond=0)

        logger.info("\n")
        logger.info("Processing model " + model)
        logger.info("#############################################################")
        logger.info("")

        # preprocessing
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        if generate_data:
            logger.info("\n")
            logger.info("Data generation:")
            logger.info("################")
            status = Sim.generate_data(simulator,
                                       model,
                                       models_dir,
                                       os.path.join(outputdir, self.get_sim_data_folder()),
                                       cluster,
                                       pp_cpus,
                                       runs)
            if not status:
                return False

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("##############")
            status = Sim.analyse_data(os.path.splitext(model)[0],
                                      os.path.join(outputdir, self.get_sim_data_folder()),
                                      outputdir,
                                      os.path.join(outputdir, self.get_sim_plots_folder()),
                                      os.path.join(models_dir, exp_dataset),
                                      plot_exp_dataset,
                                      xaxis_label,
                                      yaxis_label)
            if not status:
                return False

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("##################")
            status = Sim.generate_report(os.path.splitext(model)[0],
                                         outputdir,
                                         self.get_sim_plots_folder())
            if not status:
                return False

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        if len(glob.glob(os.path.join(outputdir, self.get_sim_plots_folder(), os.path.splitext(model)[0] + '*.png'))) > 0 and len(
                glob.glob(os.path.join(outputdir, '*' + os.path.splitext(model)[0] + '*.pdf'))) == 1:
            return True
        return False

    @classmethod
    def generate_data(cls, simulator, model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        """
        The first pipeline step: data generation.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory containing the output files
        :param cluster_type: pp for local Parallel Python, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param pp_cpus: the number of CPU used by Parallel Python.
        :param runs: the number of model simulation
        :return: True if the task was completed successfully, False otherwise.
        """

        if int(pp_cpus) < 1:
            logger.error("variable pp_cpus must be greater than 0. Please, check your configuration file.")
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
            sim.sim(model, inputdir, outputdir, cluster_type, pp_cpus, runs)
        except Exception as e:
            logger.error("simulator: " + simulator + " not found.")
            import traceback
            logger.debug(traceback.format_exc())
            return False
        return True

    @classmethod
    def analyse_data(cls, model, inputdir, outputdir, sim_plots_dir, exp_dataset, plot_exp_dataset, xaxis_label,
                     yaxis_label):
        """
        The second pipeline step: data analysis.

        :param model: the model name
        :param inputdir: the directory containing the data to analyse
        :param outputdir: the output directory containing the results
        :param sim_plots_dir: the directory to save the plots
        :param exp_dataset: the full path of the experimental data set
        :param plot_exp_dataset: True if the experimental data set should also be plotted
        :param xaxis_label: the label for the x axis (e.g. Time [min])
        :param yaxis_label: the label for the y axis (e.g. Level [a.u.])
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.exists(inputdir):
            logger.error("inputdir " + inputdir + " does not exist. Generate some data first.")
            return False

        # folder preparation
        files_to_delete = glob.glob(os.path.join(sim_plots_dir, model + "*"))
        for f in files_to_delete:
            os.remove(f)

        sim_data_per_var_dir = os.path.join(outputdir, "simulate_data_per_var")
        if not os.path.exists(sim_data_per_var_dir):
            os.mkdir(sim_data_per_var_dir)

        if not os.path.exists(sim_plots_dir):
            os.mkdir(sim_plots_dir)

        logger.info("Analysing generated simulations:")
        process = subprocess.Popen(
            ['Rscript', os.path.join(os.path.dirname(__file__), 'gen_stats_table.r'),
             model, inputdir, sim_plots_dir,
             os.path.join(outputdir, 'sim_stats_' + model + '.csv'), xaxis_label,
             yaxis_label])
        process.wait()
        logger.info("Plotting simulations:")
        process = subprocess.Popen(
            ['Rscript', os.path.join(os.path.dirname(__file__), 'plot_sep_sims.r'),
             model, inputdir, sim_plots_dir,
             os.path.join(sim_data_per_var_dir, model + '.csv'), exp_dataset, str(plot_exp_dataset), xaxis_label,
             yaxis_label])
        process.wait()
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
        return True

    def read_config(self, lines):
        __doc__ = Pipeline.read_config.__doc__

        # parse common options
        (generate_data, analyse_data, generate_report,
         project_dir, model) = self.read_common_config(lines)

        # default values
        simulator = 'Copasi'
        cluster = 'pp'
        pp_cpus = 1
        runs = 1
        exp_dataset = ''
        plot_exp_dataset = False
        xaxis_label = 'Time [min]'
        yaxis_label = 'Level [a.u.]'

        # Initialises the variables
        for line in lines:
            logger.info(line)
            if line[0] == "simulator":
                simulator = line[1]
            elif line[0] == "cluster":
                cluster = line[1]
            elif line[0] == "pp_cpus":
                pp_cpus = line[1]
            elif line[0] == "runs":
                runs = line[1]
            elif line[0] == "exp_dataset":
                exp_dataset = line[1]
            elif line[0] == "plot_exp_dataset":
                plot_exp_dataset = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "xaxis_label":
                xaxis_label = line[1]
            elif line[0] == "yaxis_label":
                yaxis_label = line[1]

        return (generate_data, analyse_data, generate_report,
                project_dir, simulator, model,
                cluster, pp_cpus, runs,
                exp_dataset, plot_exp_dataset,
                xaxis_label, yaxis_label)
