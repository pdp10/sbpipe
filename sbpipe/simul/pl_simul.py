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
from sbpipe.sb_config import which
from sbpipe.utils.parcomp import parcomp
from ..simul import Simul

logger = logging.getLogger('sbpipe')


class PLSimul(Simul):
    """
    A generic simulator for models coded in a programming language.
    """
    _language = None
    _language_not_found_msg = "Programming language not found! Please check that python is installed."
    _options = None

    def __init__(self, lang, lang_err_msg, options):
        """
        A constructor for a simulator of models coded in a programming language
        :param lang: the programming language name (e.g. python, Rscript, java, octave, ..)
        :param lang_err_msg: the message to print if lang is not found.
        :param options: the options to use when invoking the command (e.g. "-jar" for java, "--vanilla" for Rscript, "" for python, "" for octave).
        """
        __doc__ = Simul.__init__.__doc__
        Simul.__init__(self)
        self._language = which(lang)
        self._language_not_found_msg = lang_err_msg
        self._options = options
        logger.debug("Invoking simulator " + self._language + " with options " + self._options)
        if self._language is None:
            logger.error(self._language_not_found_msg)

    def get_lang(self):
        """
        Return the programming language name
        :return: the name
        """
        return self._language

    def get_lang_err_msg(self):
        """
        Return the error if the programming language is not found
        :return: the error message
        """
        return self._language_not_found_msg

    def get_lang_options(self):
        """
        Return the options for the programming language command
        :return: the options. Return None, if no options are used.
        """
        return self._options

    def sim(self, model, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul.sim.__doc__

        return self._run_par_comput(model, inputdir, outputdir, cluster, local_cpus, runs, output_msg)

    def ps1(self, model, scanned_par, simulate_intervals,
            single_param_scan_intervals, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul.ps1.__doc__

        if not self._run_par_comput(inputdir, model, outputdir, cluster, local_cpus, runs, output_msg):
            return False
        self.ps1_postproc(model, scanned_par, simulate_intervals, single_param_scan_intervals, outputdir)
        return True

    def ps2(self, model, sim_length, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul.ps2.__doc__

        if not self._run_par_comput(inputdir, model, outputdir, cluster, local_cpus, runs, output_msg):
            return False
        self.ps2_postproc(model, sim_length, outputdir)
        return True

    def pe(self, model, inputdir, cluster, local_cpus, runs, outputdir, sim_data_dir, output_msg=False):
        __doc__ = Simul.pe.__doc__

        return self._run_par_comput(model, inputdir, sim_data_dir, cluster, local_cpus, runs, output_msg)

    def _run_par_comput(self, model, inputdir, outputdir, cluster="local", local_cpus=1, runs=1, output_msg=False):
        __doc__ = Simul._run_par_comput.__doc__

        if self._language is None:
            logger.error(self._language_not_found_msg)
            return False

        model_group = self._get_model_group(model)

        # run in parallel
        # To make things simple, the last 10 character of groupid are extracted and reversed.
        # This string will be likely different from groupid and is the string to replace with
        # the iteration number.
        str_to_replace = self._groupid[10::-1]

        opts = " "
        if self._options:
            opts = " " + self._options + " "
        command = self._language + opts + os.path.join(inputdir, model) + \
                  " " + model_group + str_to_replace + ".csv"
        command = command.replace('\\', '\\\\')
        if not parcomp(command, str_to_replace, outputdir, cluster, runs, local_cpus, output_msg):
            return False
        if not self._move_reports('.', outputdir, model, self._groupid):
            return False
        return True

    def replace_str_in_report(self, report):
        __doc__ = Simul.replace_str_in_report.__doc__

        # `with` ensures that the file is closed correctly
        # re.sub(pattern, replace, string) is the equivalent of s/pattern/replace/ in sed.
        with open(report, "r") as file:
            lines = file.readlines()
        with open(report, "w") as file:
            # for idx, line in lines:
            for i in range(len(lines)):
                if i < 1:
                    # First remove non-alphanumerics and non-underscores.
                    # Then replaces whites with TAB.
                    # Finally use rstrip to remove the TAB at the end.
                    # [^\w] matches anything that is not alphanumeric or underscore
                    lines[i] = lines[i].replace("\"", "").replace("time", "Time")
                    file.write(
                        re.sub(r"\s+", '\t', re.sub(r'[^\w]', " ", lines[i])).rstrip('\t') + '\n')
                else:
                    file.write(lines[i].rstrip('\t'))
