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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 21:43:32 $

# for computing the pipeline elapsed time 
import datetime

import glob
import os
import os.path
import sys
import shutil
import subprocess
import logging

logger = logging.getLogger('sbpipe')

SBPIPE = os.environ["SBPIPE"]

sys.path.append(os.path.join(SBPIPE, "sbpipe", "pipelines"))
from pipeline import Pipeline

sys.path.append(os.path.join(SBPIPE, "sbpipe", "pipelines", "simulator"))
from simulator import Simulator
### NOTE: an instance of simulator should be retrieved dynamically.
from copasi import Copasi

sys.path.append(os.path.join(SBPIPE, "sbpipe", "utils", "python"))
from io_util_functions import refresh_directory
from latex_reports import latex_report_single_param_scan, pdf_report


class SingleParamScan(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for computing 
    a single parameter scan using copasi.
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='single_param_scan_data', sim_plots_folder='single_param_scan_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, data_folder, models_folder, working_folder, sim_data_folder, sim_plots_folder)

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("Reading file " + config_file + " : \n")

        # Initialises the variables for this pipeline
        try:
            (generate_data, analyse_data, generate_report,
             project_dir, simulator, model, scanned_par,
             simulate__intervals, single_param_scan_simulations_number, 
             single_param_scan_percent_levels, single_param_scan_knock_down_only, 
             levels_number, min_level, max_level, homogeneous_lines,
             xaxis_label, yaxis_label) = self.config_parser(config_file, "single_param_scan")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return 2

        models_dir = os.path.join(project_dir, self.get_models_folder())
        outputdir = os.path.join(project_dir, self.get_working_folder(), model[:-4])

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
            SingleParamScan.generate_data(simulator, 
                                          model,
                                          scanned_par,
                                          single_param_scan_simulations_number,
                                          simulate__intervals,
                                          levels_number,
                                          models_dir,
                                          os.path.join(outputdir, self.get_sim_data_folder()))

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("##############")
            SingleParamScan.analyse_data(model[:-4], scanned_par, single_param_scan_knock_down_only, outputdir,
                                         self.get_sim_data_folder(), self.get_sim_plots_folder(),                     single_param_scan_simulations_number,
                                         single_param_scan_percent_levels,
                                         min_level, max_level, levels_number,
                                         homogeneous_lines, xaxis_label, yaxis_label)

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("##################")
            SingleParamScan.generate_report(model[:-4], scanned_par, outputdir, self.get_sim_plots_folder())

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        if (len(glob.glob(os.path.join(outputdir, "*" + model[:-4] + "*.pdf"))) == 1 and
                    len(glob.glob(os.path.join(outputdir, self.get_sim_plots_folder(), model[:-4] + "*.png"))) > 0):
            return 0
        return 1

    @staticmethod
    def generate_data(simulator, model, scanned_par, sim_number, simulate_intervals,
                      single_param_scan_intervals, inputdir, outputdir):
        """
        The first pipeline step: data generation.

        :param simulator: the name of the simulator (e.g. copasi)
        :param model: the model to process
        :param scanned_par: the scanned parameter
        :param sim_number: the number of simulations (for det sim: 1, for stoch sim: n>1)
        :param simulate_intervals: the time step of each simulation
        :param single_param_scan_intervals: the number of scans to perform
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        """
        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return

        refresh_directory(outputdir, model[:-4])

        logger.info("Simulating Model: " + model)
        ## TODO : this should be done dynamically instead of creating an instance of Copasi here..
        if simulator == "copasi":
            sim = Copasi()
            sim.single_param_scan(model, scanned_par, sim_number, simulate_intervals,
                                  single_param_scan_intervals, inputdir, outputdir)
        else:
            logger.error("simulator: " + simulator + " not found.")

    @staticmethod
    def analyse_data(model, scanned_par, knock_down_only, outputdir,
                     sim_data_folder, sim_plots_folder, simulations_number,
                     percent_levels, min_level, max_level, levels_number,
                     homogeneous_lines, xaxis_label, yaxis_label):
        """
        The second pipeline step: data analysis.

        :param model: the model name
        :param scanned_par: the scanned parameter
        :param knock_down_only: True for knock down simulation, false if also scanning over expression.
        :param outputdir: the directory containing the results
        :param sim_data_folder: the folder containing the simulated data sets
        :param sim_plots_folder: the folder containing the generated plots
        :param simulations_number: the number of simulations
        :param percent_levels: True if the levels are percents.
        :param min_level: the minimum level
        :param max_level: the maximum level
        :param levels_number: the number of levels
        :param homogeneous_lines: True if generated line style should be homogeneous
        :param xaxis_label: the name of the x axis (e.g. Time [min])
        :param yaxis_label: the name of the y axis (e.g. Level [a.u.])        
        """

        # some control
        if not os.path.exists(os.path.join(outputdir, sim_data_folder)):
            logger.error(
                "input_dir " + os.path.join(outputdir, sim_data_folder) + " does not exist. Generate some data first.")
            return

        if float(min_level) < 0:
            logger.error("min_level MUST BE non negative.")
            return

        if percent_levels and float(max_level) < 100:
            logger.error("max_level cannot be less than 100 (=ctrl) if option `percent_levels` is True .")
            return

        # folder preparation
        refresh_directory(os.path.join(outputdir, sim_plots_folder), model[:-4])

        process = subprocess.Popen(['Rscript', os.path.join(SBPIPE, 'sbpipe', 'pipelines', 'single_param_scan',
                                                            'single_param_scan__analyse_data.r'),
                                    model, scanned_par, str(knock_down_only), outputdir, sim_data_folder,
                                    sim_plots_folder, simulations_number, str(percent_levels), str(min_level), str(max_level), str(levels_number), str(homogeneous_lines), 
                                    xaxis_label, yaxis_label])
        process.wait()

    @staticmethod
    def generate_report(model, scanned_par, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param scanned_par: the scanned parameter
        :param outputdir: the directory containing the report
        :param sim_plots_folder: the folder containing the plots
        """

        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error(
                "input_dir " + os.path.join(outputdir, sim_plots_folder) + " does not exist. Analyse the data first.")
            return

        logger.info("Generating LaTeX report")
        logger.info(model)
        filename_prefix = "report__single_param_scan_"
        latex_report_single_param_scan(outputdir, sim_plots_folder, filename_prefix,
                                       model, scanned_par)

        logger.info("Generating PDF report")
        pdf_report(outputdir, filename_prefix + model + ".tex")


    def read_configuration(self, lines):
        __doc__ = Pipeline.read_configuration.__doc__

        # parse common options
        (generate_data, analyse_data, generate_report,
         project_dir, model) = self.read_common_configuration(lines)

        # default values
        simulator = 'copasi'
        # The model species to scan (e.g. mTORC1)
        scanned_par = ""
        # The number of intervals for one simulation
        simulate__intervals = 100
        # The plot x axis label (e.g. Time[min])
        # The x axis label
        xaxis_label = "Time [min]"
        # The y axis label
        yaxis_label = "Level [a.u.]"        
        # The number of simulations (e.g. 1 for deterministic simulations, n for stochastic simulations)
        single_param_scan_simulations_number = 1
        # The scanning is performed on percent levels (true) or through a modelled inhibitor/expressor (false)
        single_param_scan_percent_levels = False
        # if True then, plot only kd (blue), otherwise plot kd and overexpression
        single_param_scan_knock_down_only = True
        # The number of levels of inhibition/over-expression
        levels_number = 10
        # minimum level
        min_level = 0
        # maximum level
        max_level = 250
        # True if lines should have the same colour, no linetype, no legend.
        # Useful for scanning from a confidence interval
        # If this is true, it overrides:
        # - single_param_scan_percent_levels and
        # - single_param_scan_knock_down_only
        homogeneous_lines = False

        # Initialises the variables
        for line in lines:
            logger.info(line)
            if line[0] == "simulator":
                simulator = line[1]            
            elif line[0] == "scanned_par":
                scanned_par = line[1]
            elif line[0] == "simulate__intervals":
                simulate__intervals = line[1]
            elif line[0] == "single_param_scan_simulations_number":
                single_param_scan_simulations_number = line[1]
            elif line[0] == "single_param_scan_percent_levels":
                single_param_scan_percent_levels = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "single_param_scan_knock_down_only":
                single_param_scan_knock_down_only = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "min_level":
                min_level = line[1]
            elif line[0] == "max_level":
                max_level = line[1]
            elif line[0] == "levels_number":
                levels_number = line[1]
            elif line[0] == "homogeneous_lines":
                homogeneous_lines = {'True': True, 'False': False}.get(line[1], False)
            elif line[0] == "xaxis_label":
                xaxis_label = line[1]
            elif line[0] == "yaxis_label":
                yaxis_label = line[1]

        return (generate_data, analyse_data, generate_report,
                project_dir, simulator, model, scanned_par,
                simulate__intervals, single_param_scan_simulations_number, single_param_scan_percent_levels,
                single_param_scan_knock_down_only, levels_number, min_level, max_level,
                homogeneous_lines, xaxis_label, yaxis_label)
