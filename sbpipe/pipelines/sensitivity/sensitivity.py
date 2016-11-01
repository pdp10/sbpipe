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
# $Date: 2015-05-30 16:14:32 $


# for computing the pipeline elapsed time 
import datetime

import os
import sys
import glob
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
from latex_reports import latex_report_simulate, pdf_report


class Sensitivity(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for computing 
    model sensitivity analysis using Copasi
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='sensitivity_data', sim_plots_folder='sensitivity_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, data_folder, models_folder, working_folder, sim_data_folder, sim_plots_folder)
        self.__sensitivities_dir="sensitivities"

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("Reading file " + config_file + " : \n")

        # Initialises the variables for this pipeline
        try:
            (generate_data, analyse_data, generate_report,
              project_dir, model) = self.config_parser(config_file, "sensitivity")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return 2

        models_dir = os.path.join(project_dir, self.get_models_folder())
        outputdir = os.path.join(project_dir, self.get_working_folder(), model[:-4], self.__sensitivities_dir)

        # Get the pipeline start time
        start = datetime.datetime.now().replace(microsecond=0)

        logger.info("\n")
        logger.info("Processing model " + model)
        logger.info("#############################################################")
        logger.info("")

        # preprocessing
        # remove the folder the previous results if any
        # filesToDelete = glob.glob(os.path.join(sensitivities_dir, "*.png"))
        # for f in filesToDelete:
        #     os.remove(f)
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)

        if generate_data:
            logger.info("\n")
            logger.info("Data generation:")
            logger.info("################")
            Sensitivity.generate_data(model, self.get_models_dir(), outputdir)

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("##############")
            Sensitivity.analyse_data(outputdir)

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("##################")
            Sensitivity.generate_report()

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end-start))

        if len(glob.glob(os.path.join(outputdir, '*.csv'))) > 0:
            return 0
        return 1

    @staticmethod
    def generate_data(model, inputdir, outputdir):
        """
        The first pipeline step: data generation.

        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        """        

        if not os.path.isfile(os.path.join(inputdir,model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return

        # folder preparation
        refresh_directory(outputdir, model[:-4])

        # execute runs simulations.
        logger.info("Sensitivity analysis for " + model)
        sim = Copasi()
        sim.sensitivity_analysis(model, inputdir, outputdir)

    # Input parameters
    # outputdir
    @staticmethod
    def analyse_data(outputdir):
        """
        The second pipeline step: data analysis.

        :param outputdir: the directory to store the performed analysis
        """        
        p = subprocess.Popen(['Rscript', os.path.join(SBPIPE,'sbpipe','pipelines', \
                                                      'sensitivity','plot_sensitivity.r'),
                              outputdir])
        p.wait()

    @staticmethod
    def generate_report(model, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param outputdir: the directory to store the report
        :param sim_plots_folder: the directory containing the time courses results combined with experimental data
        """        

        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error("input_dir " + os.path.join(outputdir, sim_plots_folder) +
                         " does not exist. Analyse the data first.")
            return

        logger.info("Generating LaTeX report")
        filename_prefix="report__sensitivity_"
        latex_report_simulate(outputdir, sim_plots_folder, model, filename_prefix)

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

        # Initialises the variables
        for line in lines:
            logger.info(line)
            break

        return (generate_data, analyse_data, generate_report,
                project_dir, model)
