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


from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def pe_collect(inputdir,
               outputdir,
               fileout_final_estims,
               fileout_all_estims,
               copasi=True):
    """
    Collect the results so that they can be processed.

    :param inputdir: the input folder containing the data
    :param outputdir: the output folder to stored the collected results
    :param fileout_final_estims: the name of the file containing the best estimations
    :param fileout_all_estims: the name of the file containing all the estimations
    :param copasi: True if COPASI was used to generate the data.
    """
    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()


    # Collect and summarises the parameter estimation results
    try:
        files_num = simulator.get_best_fits(inputdir, outputdir, fileout_final_estims)
        simulator.get_all_fits(inputdir, outputdir, fileout_all_estims)
        # print('Files retrieved: ' + str(files_num))
    except Exception as e:
        print("simulator: " + simulator + " not found.")
        import traceback
        print(traceback.format_exc())

