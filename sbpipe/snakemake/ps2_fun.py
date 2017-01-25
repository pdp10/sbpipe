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
# $Date: 2016-11-01 15:43:32 $



# for computing the pipeline elapsed time
import datetime
import glob
import logging
import os
import os.path
from parsing_configfile import config_parser
from sbpipe.report.latex_reports import latex_report_ps2, pdf_report

logger = logging.getLogger('sbpipe')


"""
This module provides the user with a complete pipeline of scripts for computing
double parameter scans.
"""


def run(self, config_file):
    data_folder = 'Data'
    models_folder = 'Models'
    working_folder = 'Working_Folder',
    sim_data_folder = 'double_param_scan_data'
    sim_plots_folder = 'double_param_scan_plots'

    logger.info("===============================")
    logger.info("Pipeline: double parameter scan")
    logger.info("===============================")
    logger.info("\n")
    logger.info("Reading file " + config_file + " : \n")

    # variable initialisation
    try:
        (generate_data, analyse_data, generate_report,
         project_dir, simulator, model, scanned_par1, scanned_par2,
         cluster, local_cpus, runs,
         sim_length) = config_parser(config_file, "double_param_scan")
    except Exception as e:
        logger.error(e.message)
        import traceback
        logger.debug(traceback.format_exc())
        return False

    runs = int(runs)
    local_cpus = int(local_cpus)
    sim_length = int(sim_length)

    # Some controls
    if runs < 1:
        logger.error("variable `runs` must be greater than 0. Please, check your configuration file.")
        return False
    if sim_length < 1:
        logger.error("variable `sim_length` must be greater than 0. Please, check your configuration file.")
        return False

    models_dir = os.path.join(project_dir, self.get_models_folder())
    outputdir = os.path.join(project_dir, self.get_working_folder(), os.path.splitext(model)[0])

    # Get the pipeline start time
    start = datetime.datetime.now().replace(microsecond=0)

    # preprocessing
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    if generate_data:
        logger.info("\n")
        logger.info("Data generation:")
        logger.info("================")
        status = generate_data(simulator,
                                        model,
                                        sim_length,
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
        status = analyse_data(os.path.splitext(model)[0],
                                       scanned_par1,
                                       scanned_par2,
                                       os.path.join(outputdir, self.get_sim_data_folder()),
                                       os.path.join(outputdir, self.get_sim_plots_folder()),
                                       cluster,
                                       runs)
        if not status:
            return False

    if generate_report:
        logger.info("\n")
        logger.info("Report generation:")
        logger.info("==================")
        status = generate_report(os.path.splitext(model)[0],
                                          scanned_par1,
                                          scanned_par2,
                                          outputdir,
                                          self.get_sim_plots_folder())
        if not status:
            return False

    # Print the pipeline elapsed time
    end = datetime.datetime.now().replace(microsecond=0)
    logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

    if len(glob.glob(os.path.join(outputdir, "*" + os.path.splitext(model)[0] + "*.pdf"))) == 1 and \
                    len(glob.glob(os.path.join(outputdir, self.get_sim_plots_folder(), os.path.splitext(model)[0] + "*.png"))) > 0:
        return True
    return False



def generate_report(model, scanned_par1, scanned_par2, outputdir, sim_plots_folder):
    """
    The third pipeline step: report generation.

    :param model: the model name
    :param scanned_par1: the first scanned parameter
    :param scanned_par2: the second scanned parameter
    :param outputdir: the directory containing the report
    :param sim_plots_folder: the folder containing the plots.
    :return: True if the task was completed successfully, False otherwise.
    """
    if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
        logger.error("input_dir " + os.path.join(outputdir, sim_plots_folder) +
                     " does not exist. Analyse the data first.")
        return False

    logger.info("Generating LaTeX report")
    logger.info(model)
    filename_prefix = "report__double_param_scan_"
    latex_report_ps2(outputdir, sim_plots_folder, filename_prefix,
                     model, scanned_par1, scanned_par2)

    logger.info("Generating PDF report")
    pdf_report(outputdir, filename_prefix + model + ".tex")
    return True
