#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
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

SB_PIPE = os.environ["SB_PIPE"]

from sb_config import get_copasi, which
from collect_results import retrieve_final_estimates
from collect_results import retrieve_all_estimates

sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines"))
from pipeline import Pipeline

sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from randomise_parameters import *
from parallel_computation import parallel_computation
from random_functions import get_rand_num_str, get_rand_alphanum_str
from io_util_functions import refresh_directory
from latex_reports import latex_report, pdf_report


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
             plot_2d_66_95cl_corr, logspace) = self.config_parser(config_file, "param_estim")
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
        fileout_approx_ple_stats = "approx_ple_stats.csv"
        fileout_conf_levels = "conf_levels.csv"

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
                              fileout_approx_ple_stats,
                              fileout_conf_levels,
                              os.path.join(outputdir, self.get_sim_plots_folder()),
                              best_fits_percent,
                              data_point_num,
                              plot_2d_66_95cl_corr,
                              logspace)

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

        copasi = get_copasi()
        if copasi is None:
            logger.error(
                "CopasiSE not found! Please check that CopasiSE is installed and in the PATH environmental variable.")
            return

        logger.info("Configure Copasi:")
        logger.info(
            "Replicate a Copasi file configured for parameter estimation and randomise the initial parameter values")
        groupid = "_" + get_rand_alphanum_str(20) + "_"
        group_model = model[:-4] + groupid
        pre_param_estim = RandomiseParameters(inputdir, model)
        pre_param_estim.print_parameters_to_estimate()
        pre_param_estim.generate_instances_from_template(nfits, groupid)

        logger.info("\n")
        logger.info("Parallel parameter estimation:")
        # To make things simple, the last 10 character of groupid are extracted and reversed.
        # This string will be likely different from groupid and is the string to replace with
        # the iteration number.
        str_to_replace = groupid[10::-1]
        command = copasi + " -s " + os.path.join(inputdir, group_model + str_to_replace + ".cps") + \
                  " " + os.path.join(inputdir, group_model + str_to_replace + ".cps")
        parallel_computation(command, str_to_replace, cluster_type, nfits, outputdir, pp_cpus)

        # Move the report files to the outputdir
        report_files = [f for f in os.listdir(inputdir) if
                       re.match(group_model + '[0-9]+.*\.csv', f) or re.match(group_model + '[0-9]+.*\.txt', f)]
        for file in report_files:
            # copy report and remove the groupid
            shutil.move(os.path.join(inputdir, file),
                        os.path.join(sim_data_dir, file.replace(groupid, "_")))

        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for file in repeated_copasi_files:
            # os.remove(os.path.join(inputdir, file))
            shutil.move(os.path.join(inputdir, file),
                        os.path.join(updated_models_dir, file.replace(groupid, "_")))

    @staticmethod
    def analyse_data(model, inputdir, outputdir, fileout_final_estims, fileout_all_estims,
                     fileout_approx_ple_stats, fileout_conf_levels, sim_plots_dir, best_fits_percent, data_point_num,
                     plot_2d_66_95cl_corr=False, logspace=True):
        """
        The second pipeline step: data analysis.

        :param model: the model name
        :param inputdir: the directory containing the simulation data
        :param outputdir: the directory to store the results
        :param fileout_final_estims: the name of the file containing final parameter sets with Chi^2
        :param fileout_all_estims: the name of the file containing all the parameter sets with Chi^2
        :param fileout_approx_ple_stats: the file name of the PLE results
        :param fileout_conf_levels: the file name of the confidence levels results
        :param sim_plots_dir: the directory of the simulation plots
        :param best_fits_percent: the percent to consider for the best fits
        :param data_point_num: the number of data points
        :param plot_2d_66_95cl_corr: True if 2 dim plots for the parameter sets within 66% and 95% should be plotted
        :param logspace: True if parameters should be plotted in log space
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
        process = Popen(['Rscript',
                         os.path.join(SB_PIPE, 'sb_pipe', 'pipelines', 'param_estim', 'main_final_fits_analysis.r'),
                         model,
                         os.path.join(outputdir, fileout_final_estims),
                         sim_plots_dir,
                         str(best_fits_percent), str(logspace)])
        process.wait()
        process = Popen(
            ['Rscript', os.path.join(SB_PIPE, 'sb_pipe', 'pipelines', 'param_estim', 'main_all_fits_analysis.r'),
             model,
             os.path.join(outputdir, fileout_all_estims),
             sim_plots_dir,
             str(data_point_num),
             os.path.join(outputdir, fileout_approx_ple_stats),
             os.path.join(outputdir, fileout_conf_levels),
             str(plot_2d_66_95cl_corr), str(logspace)])
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
        latex_report(outputdir, sim_plots_folder, model, filename_prefix)

        pdflatex = which("pdflatex")
        if pdflatex is None:
            logger.error("pdflatex not found! pdflatex must be installed for pdf reports.")
            return

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
        # Plot 2D correlations using data from 66% or 95% confidence levels
        # This can be very time/memory consuming
        plot_2d_66_95cl_corr = False
        # True if the parameters should be plotted in log10 space.
        logspace = True

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
            elif line[0] == "plot_2d_66_95cl_corr":
                plot_2d_66_95cl_corr = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "logspace":
                logspace = {'True': True, 'False': False}.get(line[1], False)

        return (generate_data, analyse_data, generate_report, generate_tarball,
                project_dir, model, cluster, pp_cpus,
                round, runs, best_fits_percent, data_point_num, plot_2d_66_95cl_corr, logspace)



