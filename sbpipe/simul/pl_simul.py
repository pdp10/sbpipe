#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
import os
import re
from sbpipe.utils.dependencies import which
from sbpipe.utils.parcomp import parcomp
from ..simul import Simul

logger = logging.getLogger('sbpipe')


class PLSimul(Simul):
    """
    A generic simulator for models coded in a programming language.
    """

    def __init__(self,
                 lang=None,
                 lang_err_msg="No programming language is set!",
                 options=""):
        """
        A constructor for a simulator of models coded in a programming language
        :param lang: the programming language name (e.g. python, Copasi)
        :param lang_err_msg: the message to print if lang is not found.
        :param options: the options to use when invoking the command (e.g. "" for python).
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
