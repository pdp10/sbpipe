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
import re
import shutil
import subprocess
from itertools import islice
from sbpipe.sb_config import which
from randomise import Randomise
from .copasi_utils import replace_str_copasi_sim_report
from .copasi_utils import get_all_fits
from .copasi_utils import get_best_fits
from sbpipe.utils.parcomp import parcomp
from sbpipe.utils.rand import get_rand_alphanum_str
from sbpipe.utils.io import replace_str_in_file
from ..simul import Simul

logger = logging.getLogger('sbpipe')


class Copasi(Simul):
    """
    Copasi simulator.
    """
    _copasi = None
    _copasi_not_found_msg = "CopasiSE not found! Please check that CopasiSE is installed and in the PATH " \
                            "environmental variable."

    def __init__(self):
        __doc__ = Simul.__init__.__doc__

        Simul.__init__(self)
        self._copasi = which("CopasiSE")
        if self._copasi is None:
            logger.error(self._copasi_not_found_msg)

    def sim(self, model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        __doc__ = Simul.sim.__doc__

        if self._copasi is None:
            logger.error(self._copasi_not_found_msg)
            return

        # run copasi in parallel
        (groupid, group_model) = self._par_comp(inputdir, model, outputdir, cluster_type, runs, pp_cpus)
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))

    def ps1(self, model, scanned_par, cluster_type, pp_cpus, runs, simulate_intervals,
            single_param_scan_intervals, inputdir, outputdir):
        __doc__ = Simul.ps1.__doc__

        if self._copasi is None:
            logger.error(self._copasi_not_found_msg)
            return

        # run copasi in parallel
        (groupid, group_model) = self._par_comp(inputdir, model, outputdir, cluster_type, runs, pp_cpus)
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))

        # TODO MOVE THE FOLLOWING CODE TO A FUNCTION in simul.py probably

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

        header = Copasi._ps1_header_init(report_files[0], scanned_par)
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
            for j in xrange(0, intervals):
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
                with open(os.path.join(outputdir, model_noext) + "__sim_" + str(i + 1) + "__level_" + str(
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

            # remove the file
            os.remove(report)


    def ps2(self, model, sim_length, inputdir, outputdir):
        __doc__ = Simul.ps2.__doc__

        model_noext = os.path.splitext(model)[0]

        if self._copasi is None:
            logger.error(self._copasi_not_found_msg)
            return

        # run CopasiSE. Copasi must generate a (TIME COURSE) report
        process = subprocess.Popen([self._copasi, '--nologo', os.path.join(inputdir, model)])
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
                    if '.' not in tp and int(tp) in timepoints:
                        filesout[int(tp)].write(line)
            finally:
                for fileout in filesout:
                    fileout.close()

    def pe(self, model, inputdir, cluster_type, pp_cpus, runs, outputdir, sim_data_dir,
           updated_models_dir):
        __doc__ = Simul.pe.__doc__

        if self._copasi is None:
            logger.error(self._copasi_not_found_msg)
            return

        # run copasi in parallel
        (groupid, group_model) = self._par_comp(inputdir, model, sim_data_dir, cluster_type, runs, pp_cpus)
        # move_models
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for file in repeated_copasi_files:
            shutil.move(os.path.join(inputdir, file),
                        os.path.join(updated_models_dir, file.replace(groupid, "_")))

    def sens(self, model, inputdir, outputdir):
        __doc__ = Simul.sens.__doc__

        # execute runs simulations.
        logger.info("Sensitivity analysis for " + model)
        pass

    def collect_pe_results(self, inputdir, outputdir, fileout_all_fits, file_out_best_fits):
        __doc__ = Simul.collect_pe_results.__doc__

        get_best_fits(inputdir, outputdir, file_out_best_fits)
        get_all_fits(inputdir, outputdir, fileout_all_fits)

    @classmethod
    def _ps1_header_init(cls, report, scanned_par):
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

    def _par_comp(self, inputdir, model, outputdir, cluster_type, runs, pp_cpus):
        """
        Run parallel computation for Copasi

        :param model: the model to process
        :param inputdir: the directory containing the model
        :param outputdir: the directory containing the output files
        :param cluster_type: pp for local Parallel Python, lsf for Load Sharing Facility, sge for Sun Grid Engine.
        :param pp_cpus: the number of CPU used by Parallel Python.
        :param runs: the number of model simulation
        """

        # Replicate the copasi file and rename its report file
        groupid = "_" + get_rand_alphanum_str(20) + "_"
        group_model = os.path.splitext(model)[0] + groupid

        for i in xrange(1, runs + 1):
            shutil.copyfile(os.path.join(inputdir, model), os.path.join(inputdir, group_model) + str(i) + ".cps")
            replace_str_in_file(os.path.join(inputdir, group_model) + str(i) + ".cps",
                                os.path.splitext(model)[0] + ".csv",
                                group_model + str(i) + ".csv")

        # run copasi in parallel
        # To make things simple, the last 10 character of groupid are extracted and reversed.
        # This string will be likely different from groupid and is the string to replace with
        # the iteration number.
        str_to_replace = groupid[10::-1]
        command = self._copasi + " " + os.path.join(inputdir, group_model + str_to_replace + ".cps")
        parcomp(command, str_to_replace, cluster_type, runs, outputdir, pp_cpus)

        # move the report files
        report_files = [f for f in os.listdir(inputdir) if
                        re.match(group_model + '[0-9]+.*\.csv', f) or re.match(group_model + '[0-9]+.*\.txt', f)]
        for report in report_files:
            # Replace some string in the report file
            replace_str_copasi_sim_report(os.path.join(inputdir, report))
            # rename and move the output file
            shutil.move(os.path.join(inputdir, report), os.path.join(outputdir, report.replace(groupid, "_")))

        return (groupid, group_model)

