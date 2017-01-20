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
from sbpipe.sb_config import which
from sbpipe.utils.parcomp import parcomp
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

        (groupid, group_model) = self._run_par_comput(inputdir, model, outputdir, cluster_type, runs, pp_cpus)
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))

    def ps1(self, model, scanned_par, simulate_intervals,
            single_param_scan_intervals, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        __doc__ = Simul.ps1.__doc__

        (groupid, group_model) = self._run_par_comput(inputdir, model, outputdir, cluster_type, runs, pp_cpus)
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))
        self._ps1_postproc(model, scanned_par, simulate_intervals, single_param_scan_intervals, outputdir)

    def ps2(self, model, sim_length, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        __doc__ = Simul.ps2.__doc__

        (groupid, group_model) = self._run_par_comput(inputdir, model, outputdir, cluster_type, runs, pp_cpus)
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))
        self._ps2_postproc(model, sim_length, outputdir)

    def pe(self, model, inputdir, cluster_type, pp_cpus, runs, outputdir, sim_data_dir,
           updated_models_dir):
        __doc__ = Simul.pe.__doc__

        (groupid, group_model) = self._run_par_comput(inputdir, model, sim_data_dir, cluster_type, runs, pp_cpus)
        # move_models
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.cps', f)]
        for file in repeated_copasi_files:
            shutil.move(os.path.join(inputdir, file),
                        os.path.join(updated_models_dir, file.replace(groupid, "_")))

    def _run_par_comput(self, inputdir, model, outputdir, cluster_type, runs, pp_cpus):
        __doc__ = Simul._run_par_comput.__doc__

        if self._copasi is None:
            logger.error(self._copasi_not_found_msg)
            return

        # Replicate the copasi file and rename its report file
        groupid = self._get_groupid()
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
        command = self._copasi + " " + os.path.join(inputdir, group_model + str_to_replace + ".cps")
        logger.debug(command)
        parcomp(command, str_to_replace, cluster_type, runs, outputdir, pp_cpus)
        self._move_reports(inputdir, outputdir, model, groupid)
        return groupid, group_model

    def _replace_str_in_report(self, report):
        __doc__ = Simul._replace_str_in_report.__doc__

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

    # utilities for collecting parameter estimation results
    #######################################################

    def _get_params_list(self, filein):
        """
        Return the list of parameter names from filein

        :param filein: a Copasi parameter estimation report file
        :return: the list of parameter names
        """
        parameters = []
        with open(filein, 'r') as file:
            lines = file.readlines()
            line_num = -1
            for line in lines:
                line_num += 1
                split_line = line.split('\t')
                if len(split_line) > 2 and split_line[1] == 'Parameter' and split_line[2] == 'Value':
                    # add to _data the parameter values
                    for result in lines[line_num + 1:]:
                        split_result = result.split("\t")
                        # Check whether this is the last sequence to read. If so, break
                        if len(split_result) == 1 and split_result[0] == '\n':
                            break
                        parameters.append(str(split_result[1]))
                    # Nothing else to do
                    break
        return parameters

    def _write_best_fits(self, files, path_out, filename_out):
        """
        Write the final estimates to filename_out

        :param files: the list of Copasi parameter estimation reports
        :param path_out: the path to store the file combining the final (best) estimates (filename_out)
        :param filename_out: the file containing the final (best) estimates
        """
        file_num = -1
        logger.info("\nCollecting results:")
        with open(os.path.join(path_out, filename_out), 'a') as fileout:
            for filein in files:
                file_num += 1
                with open(filein, 'r') as file:
                    logger.info(os.path.basename(filein))
                    lines = file.readlines()
                    entry = []
                    line_num = -1
                    for line in lines:
                        finished = False
                        line_num += 1
                        split_line = line.rstrip().split('\t')
                        # Retrieve the estimated values of the _parameters
                        # Retrieve the objective function value
                        if len(split_line) > 1 and split_line[0] == 'Objective Function Value:':
                            entry.append(os.path.basename(filein))
                            entry.append(split_line[1].rstrip())

                        if len(split_line) > 2 and split_line[1] == 'Parameter' and split_line[2] == 'Value':
                            param_num = 0
                            for result in lines[line_num + 1:]:
                                param_num += 1
                                split_result = result.split("\t")
                                if len(split_result) >= 0 and split_result[0] == "\n":
                                    # All the parameters are retrieved, then exit
                                    finished = True
                                    break
                                entry.append(str(split_result[2]))
                        if finished:
                            fileout.write('\t'.join(map(str, entry)) + '\n')
                            break

    def _write_all_fits(self, files, path_out, filename_out):
        """
        Write all the estimates to filename_out

        :param files: the list of Copasi parameter estimation reports
        :param path_out: the path to store the file combining all the estimates
        :param filename_out: the file containing all the estimates
        """
        file_num = -1
        # logger.info("\nCollecting results:")
        with open(os.path.join(path_out, filename_out), 'a') as fileout:
            for file in files:
                file_num += 1
                with open(file, 'r') as filein:
                    # logger.info(os.path.basename(file))
                    lines = filein.readlines()
                    line_num = -1
                    for line in lines:
                        line_num += 1
                        split_line = line.rstrip().split("\t")
                        # Retrieve the estimated values of the parameters
                        if len(split_line) > 2 and split_line[0] == '[Function Evaluations]' and \
                                        split_line[1] == '[Best Value]' and split_line[2] == '[Best Parameters]':
                            # add to data the parameter values
                            line_num += 1
                            if line_num < len(lines):
                                split_line = lines[line_num].replace("\t(", "").replace("\t)", "").rstrip().split("\t")

                            while len(split_line) > 2:
                                for k in range(1, len(split_line)):
                                    if k < len(split_line) - 1:
                                        fileout.write(str(split_line[k]) + '\t')
                                    else:
                                        fileout.write(str(split_line[k]) + '\n')
                                line_num += 1
                                if line_num < len(lines):
                                    split_line = lines[line_num].replace("\t(", "").replace("\t)", "").rstrip().split("\t")

                            break


