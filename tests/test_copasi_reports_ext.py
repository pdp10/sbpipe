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
# Object: run a list of tests for the insulin receptor model.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $

import os
import sys

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(SBPIPE)
import sbpipe.main as sbmain
import unittest


class TestCopasiReportsExt(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _ir_folder = os.path.join('copasi_reports_ext')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._ir_folder))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_txt_copasi_sim(self):
        self.assertEqual(sbmain.sbpipe(simulate="ir_model_det_simul1.yaml", quiet=True), 0)

    def test_cpp_copasi_sim(self):
        self.assertEqual(sbmain.sbpipe(simulate="ir_model_det_simul2.yaml", quiet=True), 1)

    def test_txt_copasi_ps1(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_ir_beta_inhib.yaml", quiet=True), 0)

    def test_txt_copasi_ps2(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib.yaml", quiet=True), 0)

    def test_txt_copasi_pe(self):
        self.assertEqual(sbmain.sbpipe(parameter_estimation="ir_model_param_estim1.yaml", quiet=True), 0)

    def test_cpp_copasi_pe(self):
        self.assertEqual(sbmain.sbpipe(parameter_estimation="ir_model_param_estim2.yaml", quiet=True), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
