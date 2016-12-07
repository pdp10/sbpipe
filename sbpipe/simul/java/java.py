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
from .java_utils import replace_str_java_sim_report
from sbpipe.utils.rand import get_rand_alphanum_str
from sbpipe.utils.io import replace_str_in_file
from ..simul import Simul

logger = logging.getLogger('sbpipe')


class Java(Simul):
    """
    Java Simulator.
    """
    _java = None
    _java_not_found_msg = "Java not found! Please check that java is installed."

    def __init__(self):
        __doc__ = Simul.__init__.__doc__

        Simul.__init__(self)
        self._java = which("java")
        if self._java is None:
            logger.error(self._java_not_found_msg)

    def sim(self, model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        __doc__ = Simul.sim.__doc__

        if self._java is None:
            logger.error(self._java_not_found_msg)
            return

        # Replicate the r file and rename its report file
        groupid = "_" + get_rand_alphanum_str(20) + "_"
        group_model = os.path.splitext(model)[0] + groupid

        # run Java in parallel
        # To make things simple, the last 10 character of groupid are extracted and reversed.
        # This string will be likely different from groupid and is the string to replace with
        # the iteration number.
        str_to_replace = groupid[10::-1]
        # The jar file must accept one parameter which is the report filename
        command = self._java + " -jar " + os.path.join(inputdir, model) + \
                  " " + group_model + str_to_replace + ".csv"
        parcomp(command, str_to_replace, cluster_type, runs, outputdir, pp_cpus)

        # move the report files from the current folder to the output folder
        # Note, R executes the model from the current folder.
        report_files = [f for f in os.listdir('.') if
                        re.match(group_model + '[0-9]+.*\.csv', f) or re.match(group_model + '[0-9]+.*\.txt', f)]
        #print(report_files)

        for file in report_files:
            # Replace some string in the report file
            replace_str_java_sim_report(file)
            # rename and move the output file
            shutil.move(file, os.path.join(outputdir, file.replace(groupid, "_")[:-4] + ".csv"))

        # removed repeated java files
        repeated_java_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.jar', f)]
        for file in repeated_java_files:
            os.remove(os.path.join(inputdir, file))
