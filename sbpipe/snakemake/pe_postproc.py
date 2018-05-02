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


import shutil
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def generic_postproc(infile,
                     outfile,
                     copasi=True):
    """
    Perform post processing file editing for the `pe` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    shutil.copy(infile, outfile)
    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()
    simulator.replace_str_in_report(outfile)
    # print(outfile)


def pe_postproc(infile,
                outfile,
                copasi=True):
    """
    Perform post processing file editing for the `pe` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    generic_postproc(infile, outfile, copasi)

