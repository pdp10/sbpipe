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
import subprocess
import logging

logger = logging.getLogger('sbpipe')

SBPIPE = os.environ["SBPIPE"]
from sb_config import get_copasi, which

sys.path.append(os.path.join(SBPIPE, "sbpipe", "pipelines"))
from pipeline import Pipeline

sys.path.append(os.path.join(SBPIPE, "sbpipe", "utils", "python"))
from copasi_utils import replace_str_copasi_sim_report
from io_util_functions import refresh_directory
from latex_reports import latex_report_double_param_scan, pdf_report


class DoubleParamScan(Pipeline):
    """
    This module provides the user with a complete pipeline of scripts for computing 
    a double parameter scan using copasi.
    """

    def __init__(self, data_folder='Data', models_folder='Models', working_folder='Working_Folder',
                 sim_data_folder='double_param_scan_data', sim_plots_folder='double_param_scan_plots'):
        __doc__ = Pipeline.__init__.__doc__

        Pipeline.__init__(self, data_folder, models_folder, working_folder, sim_data_folder, sim_plots_folder)

    def run(self, config_file):
        __doc__ = Pipeline.run.__doc__

        logger.info("Reading file " + config_file + " : \n")

        # Initialises the variables for this pipeline
        try:
            (generate_data, analyse_data, generate_report,
             project_dir, model, scanned_par1, scanned_par2,
             sim_length) = self.config_parser(config_file, "double_param_scan")
        except Exception as e:
            logger.error(e.message)
            import traceback
            logger.debug(traceback.format_exc())
            return 2

        sim_length = int(sim_length)

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
            DoubleParamScan.generate_data(model,
                                          sim_length,
                                          models_dir,
                                          os.path.join(outputdir, self.get_sim_data_folder()))

        if analyse_data:
            logger.info("\n")
            logger.info("Data analysis:")
            logger.info("##############")
            DoubleParamScan.analyse_data(model[:-4],
                                         scanned_par1,
                                         scanned_par2,
                                         os.path.join(outputdir, self.get_sim_data_folder()),
                                         os.path.join(outputdir, self.get_sim_plots_folder()))

        if generate_report:
            logger.info("\n")
            logger.info("Report generation:")
            logger.info("##################")
            DoubleParamScan.generate_report(model[:-4],
                                            scanned_par1,
                                            scanned_par2,
                                            outputdir,
                                            self.get_sim_plots_folder())

        # Print the pipeline elapsed time
        end = datetime.datetime.now().replace(microsecond=0)
        logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end - start))

        if (len(glob.glob(os.path.join(outputdir, "*" + model[:-4] + "*.pdf"))) == 1 and
                    len(glob.glob(os.path.join(outputdir, self.get_sim_plots_folder(), model[:-4] + "*.png"))) > 0):
            return 0
        return 1

    @staticmethod
    def generate_data(model, sim_length, inputdir, outputdir):
        """
        The first pipeline step: data generation.

        :param model: the model to process
        :param sim_length: the length of the simulation
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        """

        if not os.path.isfile(os.path.join(inputdir, model)):
            logger.error(os.path.join(inputdir, model) + " does not exist.")
            return

        refresh_directory(outputdir, model[:-4])

        logger.info("Simulating Model: " + model)

        model_noext = model[:-4]

        copasi = get_copasi()
        if copasi is None:
            logger.error("CopasiSE not found! Please check that CopasiSE is "
                         "installed and in the PATH environmental variable.")
            return

        # run CopasiSE. Copasi must generate a (TIME COURSE) report
        process = subprocess.Popen([copasi, '--nologo', os.path.join(inputdir, model)])
        process.wait()

        if (not os.path.isfile(os.path.join(inputdir, model_noext + ".csv")) and
                not os.path.isfile(os.path.join(inputdir, model_noext + ".txt"))):
            logger.warn(os.path.join(inputdir, model_noext + ".csv") + " (or .txt) does not exist!")
            return

        if os.path.isfile(os.path.join(inputdir, model_noext + ".txt")):
            os.rename(os.path.join(inputdir, model_noext + ".txt"), os.path.join(inputdir, model_noext + ".csv"))

        # Replace some string in the report file
        replace_str_copasi_sim_report(os.path.join(inputdir, model_noext + ".csv"))

        # copy file removing empty lines
        with open(os.path.join(inputdir, model_noext + ".csv"), 'r') as filein, \
                open(os.path.join(outputdir, model_noext + ".csv"), 'w') as fileout:
            for line in filein:
                if not line.isspace():
                    fileout.write(line)
        os.remove(os.path.join(inputdir, model_noext + ".csv"))

        # Extract a selected time point from all perturbed time courses contained in the report file
        with open(os.path.join(outputdir, model_noext + ".csv"), 'r') as filein:
            lines = filein.readlines()
            header = lines[0]
            lines = lines[1:]
            timepoints = range(0, sim_length + 1)
            filesout = []
            try:
                filesout = [open(os.path.join(outputdir, model_noext + "__tp_%d.csv" % i), "w") for i in timepoints]
                # copy the header
                for fileout in filesout:
                    fileout.write(header)
                # extract the i-th time point and copy it to the corresponding i-th file
                for line in lines:
                    tp = line.rstrip().split('\t')[0]
                    if not '.' in tp and int(tp) in timepoints:
                        filesout[int(tp)].write(line)
            finally:
                for fileout in filesout:
                    fileout.close()

    @staticmethod
    def analyse_data(model, scanned_par1, scanned_par2, inputdir, outputdir):
        """
        The second pipeline step: data analysis.

        :param model: the model name
        :param scanned_par1: the first scanned parameter
        :param scanned_par2: the second scanned parameter
        :param inputdir: the directory containing the simulated data sets to process
        :param outputdir: the directory to store the performed analysis
        """

        if not os.path.exists(inputdir):
            logger.error("input_dir " + inputdir + " does not exist. Generate some data first.")
            return

        # folder preparation
        refresh_directory(outputdir, model[:-4])

        process = subprocess.Popen(['Rscript', os.path.join(SBPIPE, 'sbpipe', 'pipelines', 'double_param_scan',
                                                            'double_param_scan__analyse_data.r'),
                                    model, scanned_par1, scanned_par2, inputdir, outputdir])
        process.wait()

    @staticmethod
    def generate_report(model, scanned_par1, scanned_par2, outputdir, sim_plots_folder):
        """
        The third pipeline step: report generation.

        :param model: the model name
        :param scanned_par1: the first scanned parameter
        :param scanned_par2: the second scanned parameter
        :param outputdir: the directory containing the report
        :param sim_plots_folder: the folder containing the plots.
        """

        if not os.path.exists(os.path.join(outputdir, sim_plots_folder)):
            logger.error("input_dir " + os.path.join(outputdir, sim_plots_folder) +
                         " does not exist. Analyse the data first.")
            return

        logger.info("Generating LaTeX report")
        logger.info(model)
        filename_prefix = "report__double_param_scan_"
        latex_report_double_param_scan(outputdir, sim_plots_folder, filename_prefix,
                                       model, scanned_par1, scanned_par2)

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
        # the first scanned param
        scanned_par1 = ""
        # the second scanned param
        scanned_par2 = ""
        # the simulation length
        sim_length = 1

        # Initialises the variables
        for line in lines:
            logger.info(line)            
            if line[0] == "scanned_par1":
                scanned_par1 = line[1]
            elif line[0] == "scanned_par2":
                scanned_par2 = line[1]
            elif line[0] == "sim_length":
                sim_length = line[1]

        return (generate_data, analyse_data, generate_report,
                project_dir, model, scanned_par1, scanned_par2,
                sim_length)
