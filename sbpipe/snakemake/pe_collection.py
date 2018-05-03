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

