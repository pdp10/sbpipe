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
import os.path
import yaml
import traceback
from ..pipeline import Pipeline
from sbpipe.utils.dependencies import is_r_package_installed
from sbpipe.utils.io import refresh
from sbpipe.utils.parcomp import parcomp
from sbpipe.utils.rand import get_rand_alphanum_str
from sbpipe.report.latex_reports import latex_report_ps1, pdf_report

logger = logging.getLogger('sbpipe')


class ParScan1(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for computing 
    single parameter scans.
    """

    def __init__(self, models_folder='Models', working_folder='Results',
                 sim_data_folder='single_param_scan_data', sim_plots_folder='single_param_scan_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, models_folder, working_folder, sim_data_folder, sim_plots_folder)

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("===============================")
        logger.info("Pipeline: single parameter scan")
        logger.info("===============================")

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
         project_dir, simulator, model, scanned_par,
         cluster, local_cpus, runs, simulate__intervals,
         ps1_percent_levels, ps1_knock_down_only,
         levels_number, min_level, max_level, homogeneous_lines,
         xaxis_label, yaxis_label) = self.parse(config_dict)

        runs = int(runs)
        local_cpus = int(local_cpus)
        simulate__intervals = int(simulate__intervals)
        min_level = float(min_level)
        max_level = float(max_level)
        levels_number = int(levels_number)

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
            status = ParScan1.generate_data(simulator,
                                            model,
                                            scanned_par,
                                            cluster,
                                            local_cpus,
                                            runs,
                                            simulate__intervals,
                                            levels_number,
                                            models_dir,
                                            os.path.join(outputdir, self.get_sim_data_folder()))
            if not status:
                return False

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("==============")
            status = ParScan1.analyse_data(os.path.splitext(model)[0],
                                           ps1_knock_down_only,
                                           outputdir,
                                           self.get_sim_data_folder(),
                                           self.get_sim_plots_folder(),
                                           runs,
                                           local_cpus,
                                           ps1_percent_levels,
                                           min_level,
                                           max_level,
                                           levels_number,
                                           homogeneous_lines,
                                           cluster,
                                           xaxis_label,
                                           yaxis_label)
            if not status:
                return False

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("==================")
            status = ParScan1.generate_report(os.path.splitext(model)[0], scanned_par, outputdir, self.get_sim_plots_folder())
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
    def generate_data(cls, simulator, model, scanned_par, cluster, local_cpus, runs, simulate_intervals,
                      single_param_scan_intervals, inputdir, outputdir):
        """
        The first pipeline step: data generation.

        :param simulator: the name of the simulator (e.g. Copasi)
        :param model: the model to process
        :param scanned_par: the scanned parameter
        :param cluster: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param local_cpus: the number of CPU.
        :param runs: the number of model simulation
        :param simulate_intervals: the time step of each simulation
        :param single_param_scan_intervals: the number of scans to perform
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        :return: True if the task was completed successfully, False otherwise.
        """
        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return False

        if int(local_cpus) < 1:
            logger.error("variable local_cpus must be greater than 0. Please, check your configuration file.")
            return False

        if runs < 1:
            logger.error("variable runs must be greater than 0. Please, check your configuration file.")
            return False

        if int(simulate_intervals) < 1:
            logger.error("variable simulate_intervals must be greater than 0. Please, check your configuration file.")
            return False

        if int(single_param_scan_intervals) < 1:
            logger.error("variable single_param_scan_intervals must be greater than 0. Please, "
                         "check your configuration file.")
            return False

        refresh(outputdir, os.path.splitext(model)[0])

        logger.info("Simulating Model: " + model)
        try:
            sim = cls.get_simul_obj(simulator)
        except TypeError as e:
            logger.error("simulator: " + simulator + " not found.")
            logger.debug(traceback.format_exc())
            return False
        try:
            return sim.ps1(model, scanned_par, simulate_intervals,
                    single_param_scan_intervals, inputdir, outputdir,
                    cluster, local_cpus, runs)
        except Exception as e:
            logger.error(str(e))
            logger.debug(traceback.format_exc())
            return False

    @classmethod
    def analyse_data(cls, model, knock_down_only, outputdir,
                     sim_data_folder, sim_plots_folder, runs, local_cpus,
                     percent_levels, min_level, max_level, levels_number,
                     homogeneous_lines, cluster="local", xaxis_label='', yaxis_label=''):
        """
        The second pipeline step: data analysis.

        :param model: the model name
        :param knock_down_only: True for knock down simulation, false if also scanning over expression.
        :param outputdir: the directory containing the results
        :param sim_data_folder: the folder containing the simulated data sets
        :param sim_plots_folder: the folder containing the generated plots
        :param runs: the number of simulations
        :param local_cpus: the number of cpus
        :param percent_levels: True if the levels are percents.
        :param min_level: the minimum level
        :param max_level: the maximum level
        :param levels_number: the number of levels
        :param homogeneous_lines: True if generated line style should be homogeneous
        :param cluster: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param xaxis_label: the name of the x axis (e.g. Time [min])
        :param yaxis_label: the name of the y axis (e.g. Level [a.u.])
        :return: True if the task was completed successfully, False otherwise.
        """

        # some control
        if not os.path.exists(os.path.join(outputdir, sim_data_folder)):
            logger.error(
                "input_dir " + os.path.join(outputdir, sim_data_folder) + " does not exist. Generate some data first.")
            return False

        #if float(min_level) < 0:
        #    logger.error("min_level MUST BE non negative. Please, check your configuration file.")
        #    return False

        if float(max_level) < 0:
            logger.error("max_level MUST BE non negative. Please, check your configuration file.")
            return False

        if float(max_level) <= float(min_level):
            logger.error("min_level MUST BE lower than max_level. Please, check your configuration file.")
            return False

        if int(local_cpus) < 1:
            logger.error("variable local_cpus must be greater than 0. Please, check your configuration file.")
            return False

        if int(runs) < 1:
            logger.error("variable runs must be greater than 0. Please, check your configuration file.")
            return False

        if int(levels_number) < 1:
            logger.error("variable levels_number must be greater than 0. Please, check your configuration file.")
            return False

        if percent_levels and float(max_level) < 100:
            logger.error("max_level cannot be less than 100 (=ctrl) if option `percent_levels` is True. "
                         "Please, check your configuration file.")
            return False

        # folder preparation
        refresh(os.path.join(outputdir, sim_plots_folder), os.path.splitext(model)[0])

        str_to_replace = get_rand_alphanum_str(10)

        # requires devtools::install_github("pdp10/sbpiper")
        if not is_r_package_installed('sbpiper'):
            logger.critical('R package `sbpiper` was not found. Abort.')
            return False
        command = 'R --quiet -e \'library(sbpiper); sbpiper_ps1(\"' + model + \
                  '\", \"' + str(knock_down_only).upper() + \
                  '\", \"' + os.path.join(outputdir, sim_data_folder) + \
                  '\", \"' + os.path.join(outputdir, sim_plots_folder) + \
                  '\", \"' + str_to_replace + \
                  '\", \"' + str(percent_levels).upper() + \
                  '\", \"' + str(min_level) + \
                  '\", \"' + str(max_level) + \
                  '\", \"' + str(levels_number) + \
                  '\", \"' + str(homogeneous_lines).upper()
            # we replace \\ with / otherwise subprocess complains on windows systems.
        command = command.replace('\\', '\\\\')
        # We do this to make sure that characters like [ or ] don't cause troubles.
        command += '\", \"' + xaxis_label + \
                   '\", \"' + yaxis_label + \
                   '\")\''

        if not parcomp(command, str_to_replace, outputdir, cluster, runs, local_cpus, False):
            return False

        if len(glob.glob(os.path.join(outputdir, sim_plots_folder, os.path.splitext(model)[0] + '*.pdf'))) == 0:
            return False
        return True

    @classmethod
    def generate_report(cls, model, scanned_par, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param scanned_par: the scanned parameter
        :param outputdir: the directory containing the report
        :param sim_plots_folder: the folder containing the plots
        :return: True if the task was completed successfully, False otherwise.
        """

        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error(
                "input_dir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.")
            return False

        logger.info("Generating LaTeX report")
        logger.info(model)
        filename_prefix = "report__single_param_scan_"
        latex_report_ps1(outputdir, sim_plots_folder, filename_prefix,
                         model, scanned_par)

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
        # default values
        simulator = 'Copasi'
        # The model species to scan (e.g. mTORC1)
        scanned_par = ''
        cluster = 'local'
        local_cpus = 1
        runs = 1
        # The number of intervals for one simulation
        simulate__intervals = 100
        # The plot x axis label (e.g. Time[min])
        # The x axis label
        xaxis_label = "Time [min]"
        # The y axis label
        yaxis_label = "Level [a.u.]"
        # The scanning is performed on percent levels (true) or through a modelled inhibitor/expressor (false)
        ps1_percent_levels = False
        # if True then, plot only kd (blue), otherwise plot kd and overexpression
        ps1_knock_down_only = True
        # The number of levels of inhibition/over-expression
        levels_number = 10
        # minimum level
        min_level = 0
        # maximum level
        max_level = 250
        # True if lines should have the same colour, no linetype, no legend.
        # Useful for scanning from a confidence interval
        # If this is true, it overrides:
        # - ps1_percent_levels and
        # - ps1_knock_down_only
        homogeneous_lines = False

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
            elif key == "scanned_par":
                scanned_par = value
            elif key == "cluster":
                cluster = value
            elif key == "local_cpus":
                local_cpus = value
            elif key == "runs":
                runs = value
            elif key == "simulate__intervals":
                simulate__intervals = value
            elif key == "ps1_percent_levels":
                ps1_percent_levels = value
            elif key == "ps1_knock_down_only":
                ps1_knock_down_only = value
            elif key == "min_level":
                min_level = value
            elif key == "max_level":
                max_level = value
            elif key == "levels_number":
                levels_number = value
            elif key == "homogeneous_lines":
                homogeneous_lines = value
            elif key == "xaxis_label":
                xaxis_label = value
            elif key == "yaxis_label":
                yaxis_label = value
            else:
                logger.warning('Found unknown option: `' + key + '`')

        return (generate_data, analyse_data, generate_report, generate_tarball,
                project_dir, simulator, model, scanned_par,
                cluster, local_cpus, runs,
                simulate__intervals, ps1_percent_levels,
                ps1_knock_down_only, levels_number, min_level, max_level,
                homogeneous_lines, xaxis_label, yaxis_label)
