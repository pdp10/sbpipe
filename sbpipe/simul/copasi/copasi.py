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

    def sim(self, model, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul.sim.__doc__

        if not self._run_par_comput(inputdir, model, outputdir, cluster, local_cpus, runs, output_msg):
            return False
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(self._get_model_group(model) + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))
        return True

    def ps1(self, model, scanned_par, simulate_intervals,
            single_param_scan_intervals, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul.ps1.__doc__

        if not self._run_par_comput(inputdir, model, outputdir, cluster, local_cpus, runs, output_msg):
            return False
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(self._get_model_group(model) + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))
        self.ps1_postproc(model, scanned_par, simulate_intervals, single_param_scan_intervals, outputdir)
        return True

    def ps2(self, model, sim_length, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul.ps2.__doc__

        if not self._run_par_comput(inputdir, model, outputdir, cluster, local_cpus, runs, output_msg):
            return False
        # removed repeated copasi files
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(self._get_model_group(model) + '[0-9]+.*\.cps', f)]
        for report in repeated_copasi_files:
            os.remove(os.path.join(inputdir, report))
        self.ps2_postproc(model, sim_length, outputdir)
        return True

    def pe(self, model, inputdir, cluster, local_cpus, runs, outputdir, sim_data_dir, output_msg=False):
        __doc__ = Simul.pe.__doc__

        if not self._run_par_comput(inputdir, model, sim_data_dir, cluster, local_cpus, runs, output_msg):
            return False
        # move_models
        repeated_copasi_files = [f for f in os.listdir(inputdir) if re.match(self._get_model_group(model) + '[0-9]+.*\.cps', f)]
        for file in repeated_copasi_files:
            os.remove(os.path.join(inputdir, file))
        return True

    def _run_par_comput(self, inputdir, model, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul._run_par_comput.__doc__

        if self._copasi is None:
            logger.error(self._copasi_not_found_msg)
            return False

        model_group = self._get_model_group(model)

        # replicate the models
        for i in range(1, runs + 1):
            shutil.copyfile(os.path.join(inputdir, model), os.path.join(inputdir, model_group) + str(i) + ".cps")
            replace_str_in_file(os.path.join(inputdir, model_group) + str(i) + ".cps",
                                os.path.splitext(model)[0] + ".csv",
                                model_group + str(i) + ".csv")
            replace_str_in_file(os.path.join(inputdir, model_group) + str(i) + ".cps",
                                os.path.splitext(model)[0] + ".txt",
                                model_group + str(i) + ".csv")
            replace_str_in_file(os.path.join(inputdir, model_group) + str(i) + ".cps",
                                os.path.splitext(model)[0] + ".tsv",
                                model_group + str(i) + ".csv")
            replace_str_in_file(os.path.join(inputdir, model_group) + str(i) + ".cps",
                                os.path.splitext(model)[0] + ".dat",
                                model_group + str(i) + ".csv")

        # run copasi in parallel
        # To make things simple, the last 10 character of groupid are extracted and reversed.
        # This string will be likely different from groupid and is the string to replace with
        # the iteration number.
        str_to_replace = self._groupid[10::-1]
        command = self._copasi + " " + os.path.join(inputdir, model_group + str_to_replace + ".cps")
        command = command.replace('\\', '/')
        if not parcomp(command, str_to_replace, outputdir, cluster, runs, local_cpus, output_msg):
            return False
        if not self._move_reports(inputdir, outputdir, model, self._groupid):
            return False
        return True

    def replace_str_in_report(self, report):
        __doc__ = Simul.replace_str_in_report.__doc__

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
                    lines[i] = lines[i].replace("Values[", "").replace("]", "").replace(".InitialValue", "")
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
                if len(split_line) > 0 and split_line[0].find('List of Fitting Items:') != -1:
                    # retrieve parameters
                    line_num += 1
                    if line_num < len(lines):
                        split_line = lines[line_num].rstrip().split("\t")
                    while len(split_line) > 0:
                        split_line = split_line[0]
                        if not split_line:
                            break
                        if split_line.find('<=') != -1:
                            # extract the name which is between ' <= ' and  ' <= '
                            param = re.search(' <= (.*) <= ', split_line).group(1)
                            parameters.append(param)
                        line_num += 1
                        if line_num < len(lines):
                            split_line = lines[line_num].rstrip().split("\t")
                        else:
                            break
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
                            # Retrieve the best fit.
                            best_fit = []
                            while line_num + 1 < len(lines):
                                line_num += 1
                                split_line = lines[line_num].replace("\t(", "").replace("\t)", "").rstrip().split("\t")
                                if len(split_line) == 1:
                                    break
                                best_fit = split_line
                            # print(best_fit)
                            fileout.write('\t'.join(map(str, best_fit)) + '\n')
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
                            # retrieve all fits
                            while line_num + 1 < len(lines):
                                line_num += 1
                                split_line = lines[line_num].replace("\t(", "").replace("\t)", "").rstrip().split("\t")
                                if len(split_line) == 1:
                                    break
                                # print(split_line[1:])
                                fileout.write('\t'.join(map(str, split_line[1:])) + '\n')
                            break
