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
from .rscript_utils import replace_str_rscript_sim_report
from sbpipe.utils.rand import get_rand_alphanum_str
from sbpipe.utils.io import replace_str_in_file
from ..simul import Simul

logger = logging.getLogger('sbpipe')


class Rscript(Simul):
    """
    R Simulator.
    """
    _rscript = None
    _rscript_not_found_msg = "Rscript not found! Please check that Rscript is installed."

    def __init__(self):
        __doc__ = Simul.__init__.__doc__

        Simul.__init__(self)
        self._rscript = which("Rscript")
        if self._rscript is None:
            logger.error(self._rscript_not_found_msg)

    def sim(self, model, inputdir, outputdir, cluster_type="pp", pp_cpus=2, runs=1):
        __doc__ = Simul.sim.__doc__

        if self._rscript is None:
            logger.error(self._rscript_not_found_msg)
            return

        # Replicate the r file and rename its report file
        groupid = "_" + get_rand_alphanum_str(20) + "_"
        group_model = os.path.splitext(model)[0] + groupid

        for i in xrange(1, runs + 1):
            shutil.copyfile(os.path.join(inputdir, model), os.path.join(inputdir, group_model) + str(i) + ".r")
            replace_str_in_file(os.path.join(inputdir, group_model) + str(i) + ".r",
                                os.path.splitext(model)[0] + ".csv",
                                group_model + str(i) + ".csv")

        # run r in parallel
        # To make things simple, the last 10 character of groupid are extracted and reversed.
        # This string will be likely different from groupid and is the string to replace with
        # the iteration number.
        str_to_replace = groupid[10::-1]
        command = self._rscript + " --vanilla " + os.path.join(inputdir, group_model + str_to_replace + ".r")
        parcomp(command, str_to_replace, cluster_type, runs, outputdir, pp_cpus)

        # move the report files from the current folder to the output folder
        # Note, R executes the model from the current folder.
        report_files = [f for f in os.listdir('.') if
                        re.match(group_model + '[0-9]+.*\.csv', f) or re.match(group_model + '[0-9]+.*\.txt', f)]
        #print(report_files)

        for file in report_files:
            # Replace some string in the report file
            replace_str_rscript_sim_report(file)
            # rename and move the output file
            shutil.move(file, os.path.join(outputdir, file.replace(groupid, "_")[:-4] + ".csv"))

        # removed repeated r files
        repeated_rscript_files = [f for f in os.listdir(inputdir) if re.match(group_model + '[0-9]+.*\.r', f)]
        for file in repeated_rscript_files:
            os.remove(os.path.join(inputdir, file))
