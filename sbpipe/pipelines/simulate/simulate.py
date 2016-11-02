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
import os
import sys
import glob
import logging
import subprocess

logger = logging.getLogger('sbpipe')

SBPIPE = os.environ["SBPIPE"]
from pipelines.pipeline import Pipeline

# locate is used to dynamically load a class by its name.
from pydoc import locate
import pipelines.simulator

from io_util_functions import refresh_directory
from latex_reports import latex_report_simulate, pdf_report


class Simulate(Pipeline):
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

        # Initialises the variables for this pipeline
        try:
            (generate_data, analyse_data, generate_report,
             project_dir, simulator, model, cluster, pp_cpus, runs,
             exp_dataset, plot_exp_dataset, 
             xaxis_label, yaxis_label) = self.config_parser(config_file, "simulate")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return 2

        runs = int(runs)
        pp_cpus = int(pp_cpus)

        # Some controls
        if runs < 1:
            logger.error("variable `runs` must be greater than 0. Please, check your configuration file.")
            return 1

        models_dir = os.path.join(project_dir, self.get_models_folder())
        outputdir = os.path.join(project_dir, self.get_working_folder(), model[:-4])
        data_dir = os.path.join(project_dir, self.get_data_folder())

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
            Simulate.generate_data(simulator, 
                                   model, 
                                   models_dir, 
                                   os.path.join(outputdir, self.get_sim_data_folder()),
                                   cluster, 
                                   pp_cpus, 
                                   runs)

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("##############")
            Simulate.analyse_data(model[:-4], 
                                  os.path.join(outputdir, self.get_sim_data_folder()), 
                                  outputdir,
                                  os.path.join(outputdir, self.get_sim_plots_folder()), 
                                  os.path.join(models_dir, exp_dataset), 
                                  plot_exp_dataset, 
                                  xaxis_label, 
                                  yaxis_label)

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("##################")
            Simulate.generate_report(model[:-4], 
                                     outputdir, 
                                     self.get_sim_plots_folder())

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        if len(glob.glob(os.path.join(outputdir, self.get_sim_plots_folder(), model[:-4] + '*.png'))) > 0 and len(
                glob.glob(os.path.join(outputdir, '*' + model[:-4] + '*.pdf'))) == 1:
            return 0
        return 1

    @staticmethod
    def generate_data(simulator, model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        """
        The first pipeline step: data generation.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory containing the output files
        :param cluster_type: pp for local Parallel Python, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param pp_cpus: the number of CPU used by Parallel Python.
        :param runs: the number of model simulation
        """
        if runs < 1:
            logger.error("variable " + str(runs) + " must be greater than 0. Please, check your configuration file.")
            return

        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return

        # folder preparation
        refresh_directory(outputdir, model[:-4])
        
        # execute runs simulations.
        logger.info("Simulating model " + model + " for " + str(runs) + " time(s)")
        try:
            # use reflection to dynamically load the simulator class by name
            sim = locate('simulator.' + simulator.lower() + '.' + simulator)()
            sim.simulate(model, inputdir, outputdir, cluster_type, pp_cpus, runs)
        except Exception as e:
            logger.error("simulator: " + simulator + " not found.")            
            import traceback
            logger.debug(traceback.format_exc())
            return

    @staticmethod
    def analyse_data(model, inputdir, outputdir, sim_plots_dir, exp_dataset, plot_exp_dataset, xaxis_label, yaxis_label):
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
        """
        if not os.path.exists(inputdir):
            logger.error("inputdir " + inputdir + " does not exist. Generate some data first.")
            return

        # folder preparation
        files_to_delete = glob.glob(os.path.join(sim_plots_dir, model + "*"))
        for f in files_to_delete:
            os.remove(f)

        if not os.path.exists(sim_plots_dir):
            os.mkdir(sim_plots_dir)

        logger.info("Generating statistics from simulations:")
        process = subprocess.Popen(
            ['Rscript', os.path.join(SBPIPE, 'sbpipe', 'pipelines', 'simulate', 'simulate__plot_error_bars.r'),
             model, inputdir, sim_plots_dir,
             os.path.join(outputdir, 'sim_stats_' + model + '.csv'), exp_dataset, str(plot_exp_dataset), xaxis_label, yaxis_label])
        process.wait()

    @staticmethod
    def generate_report(model, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param outputdir: the output directory to store the report
        :param sim_plots_folder: the folder containing the plots
        """
        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error(
                "inputdir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.")
            return

        logger.info("Generating LaTeX report")
        filename_prefix = "report__simulate_"
        latex_report_simulate(outputdir, sim_plots_folder, model, filename_prefix)

        logger.info("Generating PDF report")
        pdf_report(outputdir, filename_prefix + model + ".tex")

    def read_configuration(self, lines):
        __doc__ = Pipeline.read_configuration.__doc__

        # parse common options
        (generate_data, analyse_data, generate_report,
         project_dir, model) = self.read_common_configuration(lines)

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
