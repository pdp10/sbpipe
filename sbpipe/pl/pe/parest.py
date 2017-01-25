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

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='param_estim_data', sim_plots_folder='param_estim_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, data_folder, models_folder, working_folder, sim_data_folder, sim_plots_folder)
        # The folder containing the models with estimated parameters
        self.__updated_models_folder = 'updated_models'

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("==============================")
        logger.info("Pipeline: parameter estimation")
        logger.info("==============================")
        logger.info("\n")
        logger.info("Reading file " + config_file + " : \n")

        # variable initialisation
        try:
            (generate_data, analyse_data, generate_report,
             generate_tarball, project_dir, simulator, model,
             cluster, local_cpus, round, runs,
             best_fits_percent, data_point_num,
             plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
             logspace, scientific_notation) = self.config_parser(config_file, "param_estim")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return False

        runs = int(runs)
        local_cpus = int(local_cpus)
        best_fits_percent = int(best_fits_percent)
        data_point_num = int(data_point_num)

        models_dir = os.path.join(project_dir, self.get_models_folder())
        working_dir = os.path.join(project_dir, self.get_working_folder())

        output_folder = os.path.splitext(model)[0] + "_round" + round
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
                                          os.path.join(outputdir, self.get_sim_data_folder()),
                                          os.path.join(outputdir, self.__updated_models_folder))
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

        if os.path.isfile(os.path.join(outputdir, fileout_final_estims)) and \
            os.path.isfile(os.path.join(outputdir, fileout_all_estims)) and \
            len(glob.glob(os.path.join(outputdir, '*' + os.path.splitext(model)[0] + '*.pdf'))) == 1:
            return True
        return False

    @classmethod
    def generate_data(cls, simulator, model, inputdir, cluster, local_cpus, runs, outputdir, sim_data_dir,
                      updated_models_dir):
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
        :param updated_models_dir: the directory containing the models with updated parameters for
               each estimation
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
        refresh(updated_models_dir, os.path.splitext(model)[0])
        try:
            sim = cls.get_simul_obj(simulator)
            sim.pe(model, inputdir, cluster, local_cpus, runs, outputdir,
                   sim_data_dir, updated_models_dir)
        except Exception as e:
            logger.error("simulator: " + simulator + " not found.")
            import traceback
            logger.debug(traceback.format_exc())
            return False
        return True

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
            sim.get_best_fits(inputdir, outputdir, fileout_final_estims)
            sim.get_all_fits(inputdir, outputdir, fileout_all_estims)
        except Exception as e:
            logger.error("simulator: " + simulator + " not found.")
            import traceback
            logger.debug(traceback.format_exc())
            return False

        logger.info("\n")
        logger.info("Final fits analysis:")
        command = 'Rscript --vanilla ' + os.path.join(SBPIPE, 'sbpipe', 'R', 'psbpipe_pe_main_final_fits.r') + \
            ' ' + model + ' ' + os.path.join(outputdir, fileout_final_estims) + ' ' + sim_plots_dir + \
            ' ' + str(best_fits_percent) + ' ' + str(logspace) + ' ' + str(scientific_notation)
        # we don't replace any string in files. So let's use a substring which won't even be in any file.
        str_to_replace = '//////////'
        parcomp(command, str_to_replace, outputdir, cluster, 1, 1, True)

        logger.info("\n")
        logger.info("All fits analysis:")
        command = 'Rscript --vanilla ' + os.path.join(SBPIPE, 'sbpipe', 'R', 'sbpipe_pe_main_all_fits.r') + \
            ' ' + model + ' ' + os.path.join(outputdir, fileout_all_estims) + ' ' + sim_plots_dir + \
            ' ' + str(data_point_num) + ' ' + os.path.join(outputdir, fileout_param_estim_details) + \
            ' ' + os.path.join(outputdir, fileout_param_estim_summary) + \
            ' ' + str(plot_2d_66cl_corr) + ' ' + str(plot_2d_95cl_corr) + ' ' + str(plot_2d_99cl_corr) + \
            ' ' + str(logspace) + ' ' + str(scientific_notation)
        parcomp(command, str_to_replace, outputdir, cluster, 1, 1, True)

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
        return True

    def read_config(self, lines):
        __doc__ = Pipeline.read_config.__doc__

        # parse common options
        (generate_data, analyse_data, generate_report,
         project_dir, model) = self.read_common_config(lines)

        # default values
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
        for line in lines:
            logger.info(line)
            if line[0] == "simulator":
                simulator = line[1]
            elif line[0] == "generate_tarball":
                generate_tarball = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "cluster":
                cluster = line[1]
            elif line[0] == "round":
                round = line[1]
            elif line[0] == "runs":
                runs = line[1]
            elif line[0] == "local_cpus":
                local_cpus = line[1]
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
                project_dir, simulator, model, cluster, local_cpus,
                round, runs, best_fits_percent, data_point_num,
                plot_2d_66cl_corr, plot_2d_95cl_corr, plot_2d_99cl_corr,
                logspace, scientific_notation)
