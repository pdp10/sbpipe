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
import glob
import logging
import os
import sys
import yaml
import traceback
import tarfile
from sbpipe.report.latex_reports import latex_report_pe, pdf_report
from sbpipe.utils.io import refresh
from sbpipe.utils.parcomp import parcomp
from ..pipeline import Pipeline

SBPIPE = os.environ["SBPIPE"]
sys.path.insert(0, SBPIPE)

logger = logging.getLogger('sbpipe')


class ParEst(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for running
    model parameter estimations
    """

    def __init__(self, models_folder='Models', working_folder='Results',
                 sim_data_folder='param_estim_data', sim_plots_folder='param_estim_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, models_folder, working_folder, sim_data_folder, sim_plots_folder)

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("==============================")
        logger.info("Pipeline: parameter estimation")
        logger.info("==============================")

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
        (generate_data, analyse_data, generate_report,
         generate_tarball, project_dir, simulator, model,
         cluster, local_cpus, round, runs,
         best_fits_percent, data_point_num,
         plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
         logspace, scientific_notation) = self.parse(config_dict)

        runs = int(runs)
        round = int(round)
        local_cpus = int(local_cpus)
        best_fits_percent = float(best_fits_percent)
        data_point_num = int(data_point_num)

        models_dir = os.path.join(project_dir, self.get_models_folder())
        working_dir = os.path.join(project_dir, self.get_working_folder())

        output_folder = os.path.splitext(model)[0] + "_round" + str(round)
        outputdir = os.path.join(working_dir, output_folder)
        fileout_final_estims = "final_estim_collection.csv"
        fileout_all_estims = "all_estim_collection.csv"
        fileout_param_estim_details = "param_estim_details.csv"
        fileout_param_estim_summary = "param_estim_summary.csv"

        # Get the pipeline start time
        start = datetime.datetime.now().replace(microsecond=0)

        # preprocessing
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        if generate_data:
            logger.info("\n")
            logger.info("Data generation:")
            logger.info("================")
            status = ParEst.generate_data(simulator,
                                          model,
                                          models_dir,
                                          cluster,
                                          local_cpus,
                                          runs,
                                          outputdir,
                                          os.path.join(outputdir, self.get_sim_data_folder()))
            if not status:
                return False

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("==============")
            status = ParEst.analyse_data(simulator,
                                         os.path.splitext(model)[0],
                                         os.path.join(outputdir, self.get_sim_data_folder()),
                                         outputdir,
                                         fileout_final_estims,
                                         fileout_all_estims,
                                         fileout_param_estim_details,
                                         fileout_param_estim_summary,
                                         os.path.join(outputdir, self.get_sim_plots_folder()),
                                         best_fits_percent,
                                         data_point_num,
                                         cluster,
                                         plot_2d_66cl_corr,
                                         plot_2d_95cl_corr,
                                         plot_2d_99cl_corr,
                                         logspace,
                                         scientific_notation)
            if not status:
                return False

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("==================")
            status = ParEst.generate_report(os.path.splitext(model)[0],
                                            outputdir,
                                            self.get_sim_plots_folder())
            if not status:
                return False

        if generate_tarball:
            logger.info("\n")
            logger.info("Zipping parameter estimation results:")
            logger.info("=====================================")
            # Create a gz tarball
            orig_wd = os.getcwd()  # remember our original working directory
            os.chdir(working_dir)  # change folder
            with tarfile.open(output_folder + ".tgz", "w:gz") as tar:
                tar.add(output_folder, arcname=os.path.basename(output_folder))
            os.chdir(orig_wd)  # get back to our original working directory

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        return True

    @classmethod
    def generate_data(cls, simulator, model, inputdir, cluster, local_cpus, runs, outputdir, sim_data_dir):
        """
        The first pipeline step: data generation.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param cluster: local, lsf for load sharing facility, sge for sun grid engine
        :param local_cpus: the number of cpu
        :param runs: the number of fits to perform
        :param outputdir: the directory to store the results
        :param sim_data_dir: the directory containing the simulation data sets
        :return: True if the task was completed successfully, False otherwise.
        """
        if int(local_cpus) < 1:
            logger.error("variable local_cpus must be greater than 0. Please, check your configuration file.")
            return False

        if int(runs) < 1:
            logger.error("variable nfits must be greater than 0. Please, check your configuration file.")
            return False

        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return False

        # folder preparation
        refresh(sim_data_dir, os.path.splitext(model)[0])

        try:
            sim = cls.get_simul_obj(simulator)
        except TypeError as e:
            logger.error("simulator: " + simulator + " not found.")
            logger.debug(traceback.format_exc())
            return False
        try:
            return sim.pe(model, inputdir, cluster, local_cpus, runs, outputdir, sim_data_dir)
        except Exception as e:
            logger.error(str(e))
            logger.debug(traceback.format_exc())
            return False

    @classmethod
    def analyse_data(cls, simulator, model, inputdir, outputdir, fileout_final_estims, fileout_all_estims,
                     fileout_param_estim_details, fileout_param_estim_summary, sim_plots_dir,
                     best_fits_percent, data_point_num, cluster='local',
                     plot_2d_66cl_corr=False, plot_2d_95cl_corr=False, plot_2d_99cl_corr=False,
                     logspace=True, scientific_notation=True):
        """
        The second pipeline step: data analysis.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model name
        :param inputdir: the directory containing the simulation data
        :param outputdir: the directory to store the results
        :param fileout_final_estims: the name of the file containing final parameter sets with Chi^2
        :param fileout_all_estims: the name of the file containing all the parameter sets with Chi^2
        :param fileout_param_estim_details: the name of the file containing the detailed statistics for the \
        estimated parameters
        :param fileout_param_estim_summary: the name of the file containing the summary for the parameter estimation
        :param sim_plots_dir: the directory of the simulation plots
        :param best_fits_percent: the percent to consider for the best fits
        :param data_point_num: the number of data points
        :param cluster: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param plot_2d_66cl_corr: True if 2 dim plots for the parameter sets within 66% should be plotted
        :param plot_2d_95cl_corr: True if 2 dim plots for the parameter sets within 95% should be plotted
        :param plot_2d_99cl_corr: True if 2 dim plots for the parameter sets within 99% should be plotted        
        :param logspace: True if parameters should be plotted in log space
        :param scientific_notation: True if axis labels should be plotted in scientific notation
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.exists(inputdir) or not os.listdir(inputdir):
            logger.error("inputdir " + inputdir + " does not exist or is empty. Generate some data first.")
            return False

        if int(best_fits_percent) < 1 or int(best_fits_percent) > 100:
            logger.error("variable `best_fits_percent` must be in (0, 100]. Please, check your configuration file.")
            return False

        if int(data_point_num) < 1:
            logger.error("variable `data_point_num` must be greater than 0. Please, check your configuration file.")
            return False

        refresh(sim_plots_dir, os.path.splitext(model)[0])

        logger.info("Collect results:")
        # Collect and summarises the parameter estimation results
        try:
            sim = cls.get_simul_obj(simulator)
            files_num = sim.get_best_fits(inputdir, outputdir, fileout_final_estims)
            sim.get_all_fits(inputdir, outputdir, fileout_all_estims)
            logger.info('Files retrieved: ' + str(files_num))
        except Exception as e:
            logger.error("simulator: " + simulator + " not found.")
            import traceback
            logger.debug(traceback.format_exc())
            return False

        logger.info("\n")
        logger.info("Final fits analysis:")
        command = 'Rscript --vanilla ' + os.path.join(SBPIPE, 'sbpipe', 'R', 'sbpipe_pe_main_final_fits.r') + \
            ' ' + model + ' ' + os.path.join(outputdir, fileout_final_estims) + ' ' + sim_plots_dir + \
            ' ' + str(best_fits_percent) + ' ' + str(logspace) + ' ' + str(scientific_notation)
        # we don't replace any string in files. So let's use a substring which won't even be in any file.
        str_to_replace = '//////////'
        if not parcomp(command, str_to_replace, outputdir, cluster, 1, 1, True):
            return False

        logger.info("\n")
        logger.info("All fits analysis:")
        command = 'Rscript --vanilla ' + os.path.join(SBPIPE, 'sbpipe', 'R', 'sbpipe_pe_main_all_fits.r') + \
            ' ' + model + ' ' + os.path.join(outputdir, fileout_all_estims) + ' ' + sim_plots_dir + \
            ' ' + str(data_point_num) + ' ' + os.path.join(outputdir, fileout_param_estim_details) + \
            ' ' + os.path.join(outputdir, fileout_param_estim_summary) + \
            ' ' + str(plot_2d_66cl_corr) + ' ' + str(plot_2d_95cl_corr) + ' ' + str(plot_2d_99cl_corr) + \
            ' ' + str(logspace) + ' ' + str(scientific_notation)
        if not parcomp(command, str_to_replace, outputdir, cluster, 1, 1, True):
            return False

        if len(glob.glob(os.path.join(sim_plots_dir, os.path.splitext(model)[0] + '*.png'))) == 0:
            return False
        return True


    @classmethod
    def generate_report(cls, model, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param outputdir: the directory to store the report
        :param sim_plots_folder: the folder containing the plots
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error(
                "input_dir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.")
            return False

        logger.info("Generating LaTeX report")
        filename_prefix = "report__param_estim_"
        latex_report_pe(outputdir, sim_plots_folder, model, filename_prefix)

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
        project_dir = '.'
        model = 'model'
        # The simulator
        simulator = 'Copasi'
        # Generate a zipped tarball
        generate_tarball = False
        # The parallel mechanism to use (local | sge | lsf).
        cluster = 'local'
        # The number of cpus
        local_cpus = 1
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
        for key, value in my_dict.items():

            logger.info(key + ": " + str(value))

            if key == "generate_data":
                generate_data = value
            elif key == "analyse_data":
                analyse_data = value
            elif key == "generate_report":
                generate_report = value
            elif key == "project_dir":
                project_dir = value
            elif key == "model":
                model = value
            elif key == "simulator":
                simulator = value
            elif key == "generate_tarball":
                generate_tarball = value
            elif key == "cluster":
                cluster = value
            elif key == "round":
                round = value
            elif key == "runs":
                runs = value
            elif key == "local_cpus":
                local_cpus = value
            elif key == "best_fits_percent":
                best_fits_percent = value
            elif key == "data_point_num":
                data_point_num = value
            elif key == "plot_2d_66cl_corr":
                plot_2d_66cl_corr = value
            elif key == "plot_2d_95cl_corr":
                plot_2d_95cl_corr = value
            elif key == "plot_2d_99cl_corr":
                plot_2d_99cl_corr = value
            elif key == "logspace":
                logspace = value
            elif key == "scientific_notation":
                scientific_notation = value
            else:
                logger.warning('Found unknown option: `' + key + '`')

        return (generate_data, analyse_data, generate_report, generate_tarball,
                project_dir, simulator, model, cluster, local_cpus,
                round, runs, best_fits_percent, data_point_num,
                plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
                logspace, scientific_notation)
