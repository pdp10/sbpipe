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
import shutil
import re
from sbpipe.utils.io import refresh
from sbpipe.utils.parcomp import parcomp
from sbpipe.utils.rand import get_rand_alphanum_str
from sbpipe.utils.io import replace_str_in_file
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









def generate_data(simulator, model, sim_length, inputdir, outputdir, cluster, local_cpus, runs):
    """
    The first pipeline step: data generation.

    :param simulator: the name of the simulator (e.g. Copasi)
    :param model: the model to process
    :param sim_length: the length of the simulation
    :param inputdir: the directory containing the model
    :param outputdir: the directory to store the results
    :param cluster: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
    :param local_cpus: the number of CPU.
    :param runs: the number of model simulation
    :return: True if the task was completed successfully, False otherwise.
    """

    # Some controls
    if not os.path.isfile(os.path.join(inputdir, model)):
        logger.error(os.path.join(inputdir, model) + " does not exist.")
        return False
    if runs < 1:
        logger.error("variable `runs` must be greater than 0. Please, check your configuration file.")
        return False
    if int(sim_length) < 1:
        logger.error("variable sim_length must be greater than 0. Please, check your configuration file.")
        return False

    refresh(outputdir, os.path.splitext(model)[0])

    logger.info("Simulating Model: " + model)
    try:
        ps2(model, sim_length, inputdir, outputdir, cluster, local_cpus, runs)
    except Exception as e:
        logger.error("simulator: " + simulator + " not found.")
        import traceback
        logger.debug(traceback.format_exc())
        return False
    return True


def analyse_data(model, scanned_par1, scanned_par2, inputdir, outputdir, cluster='local', runs=1):
    """
    The second pipeline step: data analysis.

    :param model: the model name
    :param scanned_par1: the first scanned parameter
    :param scanned_par2: the second scanned parameter
    :param inputdir: the directory containing the simulated data sets to process
    :param outputdir: the directory to store the performed analysis
    :param cluster: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
    :param runs: the number of model simulation
    :return: True if the task was completed successfully, False otherwise.
    """
    if not os.path.exists(inputdir):
        logger.error("input_dir " + inputdir + " does not exist. Generate some data first.")
        return False

    # folder preparation
    refresh(outputdir, os.path.splitext(model)[0])
    if runs < 1:
        logger.error("variable `runs` must be greater than 0. Please, check your configuration file.")
        return False

    command = 'Rscript --vanilla ' + os.path.join(os.path.dirname(__file__), 'ps2_analysis.r') + \
        ' ' + model + ' ' + scanned_par1 + ' ' + scanned_par2 + ' ' + inputdir + \
        ' ' + outputdir + ' ' + str(runs)
    # we don't replace any string in files. So let's use a substring which won't even be in any file.
    str_to_replace = '//////////'
    parcomp(command, str_to_replace, outputdir, cluster, 1, 1, True)
    return True


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



def ps2(model, sim_length, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):

    # Replicate the copasi file and rename its report file
    groupid = get_groupid()
    group_model = os.path.splitext(model)[0] + groupid

    # replicate the models
    for i in range(1, runs + 1):
        shutil.copyfile(os.path.join(inputdir, model), os.path.join(inputdir, group_model) + str(i) + ".cps")
        replace_str_in_file(os.path.join(inputdir, group_model) + str(i) + ".cps",
                            os.path.splitext(model)[0] + ".csv",
                            group_model + str(i) + ".csv")

    # run copasi in parallel
    # To make things simple, the last 10 character of groupid are extracted and reversed.
    # This string will be likely different from groupid and is the string to replace with
    # the iteration number.
    str_to_replace = groupid[10::-1]
    command = copasi + " " + os.path.join(inputdir, group_model + str_to_replace + ".cps")
    parcomp(command, str_to_replace, outputdir, cluster, runs, local_cpus, output_msg)
    move_reports(inputdir, outputdir, model, groupid)
    return groupid, group_model


    (groupid, group_model) = run_par_comput(inputdir, model, outputdir, cluster, local_cpus, runs, output_msg)
    # removed repeated copasi files
    repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]


def get_groupid(self):
    """
    Get a string identifier to attach to the generated file names so that they can be recognised using pattern matching.

    :return: the identifier string of the generated files.
    """
    return "_" + get_rand_alphanum_str(20) + "_"


def move_reports(inputdir, outputdir, model, groupid):
    """
    Move the report files

    :param inputdir: the directory containing the model
    :param outputdir: the directory containing the output files
    :param model: the model to process
    :param groupid: a string identifier in the file name characterising the batch of simulated models.
    """
    group_model = os.path.splitext(model)[0] + groupid
    report_files = [f for f in os.listdir(inputdir) if
                    re.match(group_model + '[0-9]+.*\.csv', f) or re.match(group_model + '[0-9]+.*\.txt', f)]
    for report in report_files:
        # Replace some string in the report file
        replace_str_in_report(os.path.join(inputdir, report))
        # rename and move the output file
        shutil.move(os.path.join(inputdir, report), os.path.join(outputdir, report.replace(groupid, "_")[:-4] + ".csv"))


def replace_str_in_report(report):

    # `with` ensures that the file is closed correctly
    # re.sub(pattern, replace, string) is the equivalent of s/pattern/replace/ in sed.
    with open(report, 'r') as file:
        lines = file.readlines()
    with open(report, 'w') as file:
        # for idx, line in lines:
        for i in range(len(lines)):
            if i < 1:
                # First remove non-alphanumerics and non-underscores.
                # Then replaces whites with TAB.
                # Finally use rstrip to remove the TAB at the end.
                # [^\w] matches anything that is not alphanumeric or underscore
                lines[i] = lines[i].replace("Values[", "").replace("]", "")
                file.write(
                    re.sub(r"\s+", '\t', re.sub(r'[^\w]', " ", lines[i])).rstrip('\t') + '\n')
            else:
                file.write(lines[i].rstrip('\t'))


def clean_copasi_files(inputdir, files):
    for report in files:
        os.remove(os.path.join(inputdir, report))


def ps2_postproc(model, sim_length, outputdir):
    """
    Perform post processing organisation to double parameter scan report files.

    :param model: the model to process
    :param sim_length: the length of the simulation
    :param outputdir: the directory to store the results
    """

    model_noext = os.path.splitext(model)[0]

    # Re-structure the reports
    report_files = [os.path.join(outputdir, f) for f in os.listdir(outputdir) if
                    re.match(model_noext + '_[0-9]+.*\.csv', f) or re.match(model_noext + '_[0-9]+.*\.txt', f)]
    if not report_files:
        return

    for i, report in enumerate(report_files):
        logger.debug(report)

        # copy file removing empty lines
        with open(report, 'r') as filein, \
                open(report + "~", 'w') as fileout:
            for line in filein:
                if not line.isspace():
                    fileout.write(line)
        shutil.move(report + '~', report)

        # Extract a selected time point from all perturbed time courses contained in the report file
        with open(report, 'r') as filein:
            lines = filein.readlines()
            header = lines[0]
            lines = lines[1:]
            timepoints = list(range(0, sim_length + 1))
            filesout = []
            try:
                filesout = [open(os.path.join(outputdir, model_noext + '__rep_' + str(i+1) + '__tp_%d.csv' % k), 'w') for k in timepoints]
                # copy the header
                for fileout in filesout:
                    fileout.write(header)
                # extract the i-th time point and copy it to the corresponding i-th file
                for line in lines:
                    tp = line.rstrip().split('\t')[0]
                    if '.' not in tp and int(tp) in timepoints:
                        filesout[int(tp)].write(line)
            finally:
                for fileout in filesout:
                    fileout.close()
