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

import logging
import os
import glob
import shutil
import re
from itertools import islice
from sbpipe.utils.re_utils import nat_sort_key
from sbpipe.utils.rand import get_rand_alphanum_str

logger = logging.getLogger('sbpipe')


class Simul(object):
    """
    Generic simulator.
    """

    def __init__(self):
        """
        Default constructor.
        """
        pass

    def sim(self, model, inputdir, outputdir, cluster_type="local", local_cpus=2, runs=1):
        """
        Time course simulator.
        
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory containing the output files
        :param cluster_type: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param local_cpus: the number of CPU.
        :param runs: the number of model simulation
        """
        pass

    def ps1(self, model, scanned_par, simulate_intervals,
            single_param_scan_intervals, inputdir, outputdir, cluster_type="local", local_cpus=2, runs=1):
        """
        Single parameter scan.
        
        :param model: the model to process
        :param scanned_par: the scanned parameter
        :param simulate_intervals: the time step of each simulation
        :param single_param_scan_intervals: the number of scans to perform
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        :param cluster_type: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param local_cpus: the number of CPU used.
        :param runs: the number of model simulation
        """
        pass

    def ps2(self, model, sim_length, inputdir, outputdir, cluster_type="local", local_cpus=2, runs=1):
        """
        Double paramter scan.
        
        :param model: the model to process
        :param sim_length: the length of the simulation
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        :param cluster_type: local, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param local_cpus: the number of CPU.
        :param runs: the number of model simulation
        """
        pass

    def pe(self, model, inputdir, cluster_type, local_cpus, nfits, outputdir, sim_data_dir,
           updated_models_dir):
        """
        parameter estimation.
        
        :param model: the model to process
        :param inputdir: the directory containing the model
        :param cluster_type: local, lsf for load sharing facility, sge for sun grid engine
        :param local_cpus: the number of cpu
        :param nfits: the number of fits to perform
        :param outputdir: the directory to store the results
        :param sim_data_dir: the directory containing the simulation data sets
        :param updated_models_dir: the directory containing the models with updated parameters for
               each estimation
        """
        pass

    def get_best_fits(self, path_in=".", path_out=".", filename_out="final_estimates.csv"):
        """
        Collect the final parameter estimates. Results
        are stored in filename_out.

        :param path_in: the path to the input files
        :param path_out: the path to the output files
        :param filename_out: a global file containing the best fits from independent parameter estimations.
        """
        # The path containing the results .csv files
        path = path_in
        # The collection of .csv files
        files = self._get_input_files(path)
        # List of estimated parameters
        col_names = self._get_params_list(files[0])
        col_names.insert(0, 'Estimation')
        col_names.insert(1, 'ObjectiveValue')
        self._write_params(col_names, path_out, filename_out)
        self._write_best_fits(files, path_out, filename_out)

    def get_all_fits(self, path_in=".", path_out=".", filename_out="all_estimates.csv"):
        """
        Collect all the parameter estimates. Results
        are stored in filename_out.

        :param path_in: the path to the input files
        :param path_out: the path to the output files
        :param filename_out: a global file containing all fits from independent parameter estimations.
        """
        # The path containing the results .csv files
        path = path_in
        # The collection of .csv files
        files = self._get_input_files(path)
        # List of estimated parameters
        col_names = self._get_params_list(files[0])
        col_names.insert(0, 'ObjectiveValue')
        self._write_params(col_names, path_out, filename_out)
        self._write_all_fits(files, path_out, filename_out)

    ##########################################################
    # utilities for parallel computation and post processing #
    ##########################################################

    def _run_par_comput(self, model, inputdir, outputdir, cluster_type="local", local_cpus=2, runs=1):
        """
        Run generic parallel computation.

        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory to store the results
        :param cluster_type: local, lsf for load sharing facility, sge for sun grid engine
        :param local_cpus: the number of cpus
        :param nruns: the number of runs to perform
        """
        pass

    def _get_groupid(self):
        """
        Get a string identifier to attach to the generated file names so that they can be recognised using pattern matching.

        :return: the identifier string of the generated files.
        """
        return "_" + get_rand_alphanum_str(20) + "_"

    def _move_reports(self, inputdir, outputdir, model, groupid):
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
            self._replace_str_in_report(os.path.join(inputdir, report))
            # rename and move the output file
            shutil.move(os.path.join(inputdir, report), os.path.join(outputdir, report.replace(groupid, "_")[:-4] + ".csv"))

    def _replace_str_in_report(self, report):
        """
        Replaces strings in a report file.

        :param report: a report file with its absolute path
        """
        pass

    #########################################################
    # utilities for collecting parameter estimation results #
    #########################################################

    def _get_input_files(self, path):
        """
        Retrieve the input files in a path.

        :param path: the path containing the input files to retrieve
        :return: the list of input files
        """
        files = glob.glob(os.path.join(path, "*.csv"))
        files.sort(key=nat_sort_key)
        return files

    def _get_params_list(self, filein):
        """
        Return the list of parameter names from filein

        :param filein: a report file
        :return: the list of parameter names
        """
        with open(filein, 'r') as myfile:
            header = myfile.readline().strip('\n')
        parameters = header.split('\t')
        parameters.remove(parameters[0])
        return parameters

    def _write_params(self, col_names, path_out, filename_out):
        """
        Write the list of parameter names to filename_out

        :param col_names: the list of parameter names
        :param path_out: the path to store filename_out
        :param filename_out: the output file to store the parameter names
        """
        with open(os.path.join(path_out, filename_out), 'w') as myfile:
            i = -1
            for param in col_names:
                i += 1
                if i < len(col_names) - 1:
                    myfile.write(param + '\t')
                else:
                    myfile.write(param + '\n')

    def _write_best_fits(self, files, path_out, filename_out):
        """
        Write the final estimates to filename_out

        :param files: the list of parameter estimation reports
        :param path_out: the path to store the file combining the final (best) estimates (filename_out)
        :param filename_out: the file containing the final (best) estimates
        """
        logger.info("\nCollecting results:")
        with open(os.path.join(path_out, filename_out), 'a') as fileout:
            for filein in files:
                with open(filein, 'r') as myfile:
                    logger.info(os.path.basename(filein))
                    lines = myfile.readlines()
                    fileout.write(os.path.basename(filein) + '\t' + lines[len(lines)-1])

    def _write_all_fits(self, files, path_out, filename_out):
        """
        Write all the estimates to filename_out

        :param files: the list of parameter estimation reports
        :param path_out: the path to store the file combining all the estimates
        :param filename_out: the file containing all the estimates
        """
        # logger.info("\nCollecting results:")
        with open(os.path.join(path_out, filename_out), 'a') as fileout:
            for file in files:
                with open(file, 'r') as filein:
                    # logger.info(os.path.basename(file))
                    # skip the first line (header)
                    filein.readline()
                    # read the remaining lines
                    lines = filein.readlines()
                    for line in lines:
                        fileout.write(line)

    ##########################################################
    # utilities for collecting single parameter scan results #
    ##########################################################

    def _ps1_header_init(self, report, scanned_par):
        """
        Header report initialisation for single parameter scan pipeline.

        :param report: a report
        :param scanned_par: the scanned parameter

        :return a list containing the header or an empty list if no header was created.
        """

        header = ['Time']
        # Find the index of scanned_par in the header file, so it is possible to read the amount at
        # the second line.
        logger.debug("Retrieving column index for " + scanned_par +
                     " from file " + report)
        # Read the first line of a file.
        with open(report) as myfile:
            # 1 is the number of lines to read, 0 is the i-th element to extract from the list.
            header = list(islice(myfile, 1))[0].replace('\n', '').split('\t')
        logger.debug(header)
        # Prepare the Header for the output files
        # Add a \t at the end of each element of the header
        header = [h + '\t' for h in header]
        # Remove the \t for the last element.
        header[-1] = header[-1].strip()
        return header

    def _ps1_postproc(self, model, scanned_par, simulate_intervals, single_param_scan_intervals, outputdir):
        """
        Perform post processing organisation to single parameter scan report files.

        :param model: the model to process
        :param scanned_par: the scanned parameter
        :param simulate_intervals: the time step of each simulation
        :param single_param_scan_intervals: the number of scans to perform
        :param outputdir: the directory to store the results
        """

        model_noext = os.path.splitext(model)[0]
        scanned_par_index = -1
        scanned_par_level = -1
        # Set the number of intervals
        intervals = int(single_param_scan_intervals) + 1
        # Set the number of timepoints
        timepoints = int(simulate_intervals) + 1

        # Re-structure the reports
        report_files = [os.path.join(outputdir, f) for f in os.listdir(outputdir) if
                        re.match(model_noext + '_[0-9]+.*\.csv', f) or re.match(model_noext + '_[0-9]+.*\.txt', f)]
        if not report_files:
            return

        header = self._ps1_header_init(report_files[0], scanned_par)
        if not header:
            return

        for j, name in enumerate(header):
            # remove \n and \t from name
            name = ''.join(name.split())
            logger.debug(str(j) + " " + name + " " + scanned_par)
            if name == scanned_par:
                scanned_par_index = j
                break
        if scanned_par_index == -1:
            logger.error("Column index for " + scanned_par + ": " + str(
                scanned_par_index) + ". Species not found! You must add " + scanned_par +
                         " to the Copasi report.")
            return
        else:
            logger.debug("Column index for " + scanned_par + ": " + str(scanned_par_index))

        for i, report in enumerate(report_files):
            logger.debug(report)

            # Prepare the table content for the output files
            for j in range(0, intervals):
                # Read the scanned_par level
                # Read the second line of a file.

                with open(report, 'r') as myfile:
                    # 2 is the number of lines to read, 1 is the i-th element to extract from the list.
                    initial_configuration = list(islice(myfile, 2))[1].replace("\n", "").split('\t')
                    # print(initial_configuration)
                    scanned_par_level = initial_configuration[scanned_par_index]

                if scanned_par_level == -1:
                    logger.error("scanned_par_level not configured!")
                    return
                else:
                    logger.debug(
                        scanned_par + " level: " + str(scanned_par_level) + " (list index: " + str(
                            scanned_par_index) + ")")

                # copy the -th run to a new file: add 1 to timepoints because of the header.
                round_scanned_par_level = scanned_par_level
                # Read the first timepoints+1 lines of a file.
                with open(report, 'r') as myfile:
                    table = list(islice(myfile, timepoints + 1))

                # Write the extracted table to a separate file
                with open(os.path.join(outputdir, model_noext) + "__scan_" + scanned_par + "__rep_" + str(i + 1) + "__level_" + str(
                        round_scanned_par_level) + ".csv", 'w') as myfile:
                    for line in table:
                        myfile.write(line)

                with open(report, 'r') as myfile:
                    # read all lines
                    lines = myfile.readlines()

                with open(report + "~", 'w') as myfile:
                    myfile.writelines(header)
                    myfile.writelines(lines[timepoints + 1:])

                shutil.move(report + "~", report)

    ##########################################################
    # utilities for collecting double parameter scan results #
    ##########################################################

    def _ps2_postproc(self, model, sim_length, outputdir):
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
