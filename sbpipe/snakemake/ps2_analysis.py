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


from sbpipe.utils.parcomp import run_cmd


def ps2_analyse_plot(model,
                     scanned_par1,
                     scanned_par2,
                     inputdir,
                     outputdir,
                     id):
    """
    Plot model double parameter scan time courses (Python wrapper).

    :param model: the model name without extension
    :param scanned_par1: the 1st scanned parameter
    :param scanned_par2: the 2nd scanned parameter
    :param inputdir: the input directory
    :param outputdir: the output directory
    :param run: the simulation number
    """
    # requires devtools::install_github("pdp10/sbpiper")
    command = 'R --quiet -e \'library(sbpiper); plot_double_param_scan_data(\"' + model + \
              '\", \"' + scanned_par1 + '\", \"' + scanned_par2 + \
              '\", \"' + inputdir + \
              '\", \"' + outputdir + \
              '\", \"' + str(id)
    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')
    # We do this to make sure that characters like [ or ] don't cause troubles.
    command += '\")\''
    # print(command)
    run_cmd(command)

