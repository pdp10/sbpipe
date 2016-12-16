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
from sbpipe.sb_config import which
from sbpipe.utils.parcomp import parcomp
from sbpipe.utils.rand import get_rand_alphanum_str
from .report_utils import move_sim_report_files
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

    def sim(self, model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        __doc__ = PLSimul.sim.__doc__

        if self._language is None:
            logger.error(self._language_not_found_msg)
            return

        # Replicate the r file and rename its report file
        groupid = "_" + get_rand_alphanum_str(20) + "_"
        group_model = os.path.splitext(model)[0] + groupid

        # run in parallel
        # To make things simple, the last 10 character of groupid are extracted and reversed.
        # This string will be likely different from groupid and is the string to replace with
        # the iteration number.
        str_to_replace = groupid[10::-1]

        opts = " "
        if self._options:
            opts = " " + self._options + " "
        command = self._language + opts + os.path.join(inputdir, model) + \
                  " " + group_model + str_to_replace + ".csv"
        print(command)
        parcomp(command, str_to_replace, cluster_type, runs, outputdir, pp_cpus)
        move_sim_report_files(outputdir, group_model, groupid)

