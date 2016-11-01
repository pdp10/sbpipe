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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 19:14:32 $


# for computing the pipeline elapsed time 
import datetime

import os
import sys
import glob
import re
import subprocess
import tarfile
import logging

logger = logging.getLogger('sbpipe')

SBPIPE = os.environ["SBPIPE"]

from collect_results import retrieve_final_estimates
from collect_results import retrieve_all_estimates

sys.path.append(os.path.join(SBPIPE, "sbpipe", "pipelines"))
from pipeline import Pipeline

sys.path.append(os.path.join(SBPIPE, "sbpipe", "pipelines", "simulator"))
from simulator import Simulator
### NOTE: an instance of simulator should be retrieved dynamically.
from copasi import Copasi

sys.path.append(os.path.join(SBPIPE, "sbpipe", "utils", "python"))
from io_util_functions import refresh_directory
from latex_reports import latex_report_param_estim, pdf_report


class ParamEstim(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for running
    a model parameter estimation using copasi
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='param_estim_data', sim_plots_folder='param_estim_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, data_folder, models_folder, working_folder, sim_data_folder, sim_plots_folder)
        # The folder containing the updated Copasi models
        self.__updated_models_folder = 'updated_models'

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("Reading file " + config_file + " : \n")

        # Initialises the variables for this pipeline
        try:
            (generate_data, analyse_data, generate_report,
             generate_tarball, project_dir, model,
             cluster, pp_cpus, round, runs,
             best_fits_percent, data_point_num,
             plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
             logspace, scientific_notation) = self.config_parser(config_file, "param_estim")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return 2

        runs = int(runs)
        pp_cpus = int(pp_cpus)
        best_fits_percent = int(best_fits_percent)
        data_point_num = int(data_point_num)

        models_dir = os.path.join(project_dir, self.get_models_folder())
        working_dir = os.path.join(project_dir, self.get_working_folder())

        output_folder = model[:-4] + "_round" + round
        outputdir = os.path.join(working_dir, output_folder)
        fileout_final_estims = "final_estim_collection.csv"
        fileout_all_estims = "all_estim_collection.csv"
        fileout_param_estim_details = "param_estim_details.csv"
        fileout_param_estim_summary = "param_estim_summary.csv"

        # Get the pipeline start time
        start = datetime.datetime.now().replace(microsecond=0)

        logger.info("\n")
        logger.info("Parameter estimation for model " + model)
        logger.info("#############################################################")
        logger.info("")

        # preprocessing
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        if generate_data:
            logger.info("\n")
            logger.info("Generate data:")
            logger.info("##############")
            ParamEstim.generate_data(model,
                                       models_dir,
                                       cluster,
                                       pp_cpus,
                                       runs,
                                       outputdir,
                                       os.path.join(outputdir, self.get_sim_data_folder()),
                                       os.path.join(outputdir, self.__updated_models_folder))

        if analyse_data:
            logger.info("\n")
            logger.info("Analyse data:")
            logger.info("#############")
            self.analyse_data(model[:-4],
                              os.path.join(outputdir, self.get_sim_data_folder()),
                              outputdir,
                              fileout_final_estims,
                              fileout_all_estims,
                              fileout_param_estim_details,
                              fileout_param_estim_summary,
                              os.path.join(outputdir, self.get_sim_plots_folder()),
                              best_fits_percent,
                              data_point_num,
                              plot_2d_66cl_corr,
                              plot_2d_95cl_corr,
                              plot_2d_99cl_corr,
                              logspace,
                              scientific_notation)

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("##################")
            self.generate_report(model[:-4], outputdir, self.get_sim_plots_folder())

        if generate_tarball:
            logger.info("\n")
            logger.info("Store the fits sequences in a tarball:")
            logger.info("#####################################")
            # Create a gz tarball
            origWD = os.getcwd()  # remember our original working directory
            os.chdir(working_dir)  # change folder
            with tarfile.open(output_folder + ".tgz", "w:gz") as tar:
                tar.add(output_folder, arcname=os.path.basename(output_folder))
            os.chdir(origWD)  # get back to our original working directory

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        if os.path.isfile(os.path.join(outputdir, fileout_final_estims)) and \
            os.path.isfile(os.path.join(outputdir, fileout_all_estims)) and \
            len(glob.glob(os.path.join(outputdir, '*' + model[:-4] + '*.pdf'))) == 1:
            return 0
        return 1

    @staticmethod
    def generate_data(model, inputdir, cluster_type, pp_cpus, nfits, outputdir, sim_data_dir,
                      updated_models_dir):
        """
        The first pipeline step: data generation.

        :param model: the model to process
        :param inputdir: the directory containing the model
        :param cluster_type: pp for parallel python, lsf for load sharing facility, sge for sun grid engine
        :param pp_cpus: the number of cpu for parallel python
        :param nfits: the number of fits to perform
        :param outputdir: the directory to store the results
        :param sim_data_dir: the directory containing the simulation data sets
        :param updated_models_dir: the directory containing the Copasi models with updated parameters for
               each estimation
        """

        if int(nfits) < 1:
            logger.error("variable " + nfits + " must be greater than 0. Please, check your configuration file.")
            return

        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return

        # folder preparation
        refresh_directory(sim_data_dir, model[:-4])
        refresh_directory(updated_models_dir, model[:-4])

        sim = Copasi()
        sim.parameter_estimation(model, inputdir, cluster_type, pp_cpus, nfits, outputdir, 
                                 sim_data_dir, updated_models_dir)

    @staticmethod
    def analyse_data(model, inputdir, outputdir, fileout_final_estims, fileout_all_estims,
                     fileout_param_estim_details, fileout_param_estim_summary, sim_plots_dir, best_fits_percent, data_point_num,
                     plot_2d_66cl_corr=False, plot_2d_95cl_corr=False, plot_2d_99cl_corr=False,
                     logspace=True, scientific_notation=True):
        """
        The second pipeline step: data analysis.

        :param model: the model name
        :param inputdir: the directory containing the simulation data
        :param outputdir: the directory to store the results
        :param fileout_final_estims: the name of the file containing final parameter sets with Chi^2
        :param fileout_all_estims: the name of the file containing all the parameter sets with Chi^2
        :param fileout_param_estim_details: the name of the file containing the detailed statistics for the estimated parameters
        :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation
        :param sim_plots_dir: the directory of the simulation plots
        :param best_fits_percent: the percent to consider for the best fits
        :param data_point_num: the number of data points
        :param plot_2d_66cl_corr: True if 2 dim plots for the parameter sets within 66% should be plotted
        :param plot_2d_95cl_corr: True if 2 dim plots for the parameter sets within 95% should be plotted
        :param plot_2d_99cl_corr: True if 2 dim plots for the parameter sets within 99% should be plotted        
        :param logspace: True if parameters should be plotted in log space
        :param scientific_notation: True if axis labels should be plotted in scientific notation        
        """

        if not os.path.exists(inputdir) or not os.listdir(inputdir):
            logger.error("inputdir " + inputdir + " does not exist or is empty. Generate some data first.")
            return

        refresh_directory(sim_plots_dir, model[:-4])

        logger.info("Collect results:")
        # Collect and summarises the parameter estimation results
        retrieve_final_estimates(inputdir, outputdir, fileout_final_estims)
        retrieve_all_estimates(inputdir, outputdir, fileout_all_estims)

        logger.info("\n")
        logger.info("Plot results:")
        logger.info("\n")
        process = subprocess.Popen(['Rscript',
                         os.path.join(SBPIPE, 'sbpipe', 'pipelines', 'param_estim', 'main_final_fits_analysis.r'),
                         model,
                         os.path.join(outputdir, fileout_final_estims),
                         sim_plots_dir,
                         str(best_fits_percent), str(logspace), str(scientific_notation)])
        process.wait()
        process = subprocess.Popen(
            ['Rscript', os.path.join(SBPIPE, 'sbpipe', 'pipelines', 'param_estim', 'main_all_fits_analysis.r'),
             model,
             os.path.join(outputdir, fileout_all_estims),
             sim_plots_dir,
             str(data_point_num),
             os.path.join(outputdir, fileout_param_estim_details),
             os.path.join(outputdir, fileout_param_estim_summary),
             str(plot_2d_66cl_corr), str(plot_2d_95cl_corr), str(plot_2d_99cl_corr), 
             str(logspace), str(scientific_notation)])
        process.wait()

    @staticmethod
    def generate_report(model, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param outputdir: the directory to store the report
        :param sim_plots_folder: the folder containing the plots
        """

        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error(
                "input_dir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.")
            return

        logger.info("Generating LaTeX report")
        filename_prefix = "report__param_estim_"
        latex_report_param_estim(outputdir, sim_plots_folder, model, filename_prefix)

        logger.info("Generating PDF report")
        pdf_report(outputdir, filename_prefix + model + ".tex")

    def read_configuration(self, lines):
        __doc__ = Pipeline.read_configuration.__doc__

        # parse copasi common options
        (generate_data, analyse_data, generate_report,
         project_dir, model) = self.read_common_configuration(lines)

        # default values
        # The parallel mechanism to use (pp | sge | lsf).
        cluster = "pp"
        # The number of cpus for pp
        pp_cpus = 1
        # The parameter estimation round
        round = 1
        # The number of jobs to be executed
        runs = 25
        # The percent of best fits to consider
        best_fits_percent = 100
        # The number of available data points
        data_point_num = 10
        # Plot 2D correlations using data from 66% confidence levels
        # This can be very time/memory consuming
        plot_2d_66cl_corr = False
        # Plot 2D correlations using data from 95% confidence levels
        # This can be very time/memory consuming
        plot_2d_95cl_corr = False
        # Plot 2D correlations using data from 99% confidence levels
        # This can be very time/memory consuming
        plot_2d_99cl_corr = False        
        # True if the parameters should be plotted in log10 space.
        logspace = True
        # True if axis labels should be plotted in scientific notation
        scientific_notation = True

        # Initialises the variables
        for line in lines:
            logger.info(line)
            if line[0] == "generate_tarball":
                generate_tarball = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "cluster":
                cluster = line[1]
            elif line[0] == "round":
                round = line[1]
            elif line[0] == "runs":
                runs = line[1]
            elif line[0] == "pp_cpus":
                pp_cpus = line[1]
            elif line[0] == "best_fits_percent":
                best_fits_percent = line[1]
            elif line[0] == "data_point_num":
                data_point_num = line[1]
            elif line[0] == "plot_2d_66cl_corr":
                plot_2d_66cl_corr = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "plot_2d_95cl_corr":
                plot_2d_95cl_corr = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "plot_2d_99cl_corr":
                plot_2d_99cl_corr = {'True': True, 'False': False}.get(line[1], False)                
            elif line[0] == "logspace":
                logspace = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "scientific_notation":
                scientific_notation = {'True': True, 'False': False}.get(line[1], False)

        return (generate_data, analyse_data, generate_report, generate_tarball,
                project_dir, model, cluster, pp_cpus,
                round, runs, best_fits_percent, data_point_num, 
                plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
                logspace, scientific_notation)



