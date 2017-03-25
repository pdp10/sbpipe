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


class TestSuiteManuscript(unittest.TestCase):
    """ Test suite for reproducing figures in Dalle Pezze and Le Novère, 2017, BMC Systems Biology. """

    _orig_wd = os.getcwd()  # remember our original working directory
    _ir_folder = os.path.join('insulin_receptor')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._ir_folder))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    # Simulation
    def test_sim_copasi(self):
        self.assertEqual(sbmain.sbpipe(simulate="ir_model_det_simul.yaml"), 0)

    def test_stoch_sim_copasi(self):
        self.assertEqual(sbmain.sbpipe(simulate="ir_model_stoch_simul.yaml"), 0)

    # 1 parameter scan
    def test_ps1_ci(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan.yaml"), 0)

    def test_ps1_inhib_only(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_ir_beta_inhib.yaml"), 0)

    def test_stoch_ps1_inhib_only(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_ir_beta_inhib_stoch.yaml"), 0)

    def test_ps1_inhib_overexp(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_ir_beta_inhib_overexp.yaml"), 0)

    # 2 parameter scan
    def test_ps2_inhib_only(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib.yaml"), 0)

    def test_stoch_ps2_inhib_only(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_stoch_inhib.yaml"), 0)

    # 3 parameter estimation
    def test_pe_copasi1(self):
        self.assertEqual(sbmain.sbpipe(parameter_estimation="ir_model_param_estim.yaml"), 0)

    def test_pe_copasi2(self):
        self.assertEqual(sbmain.sbpipe(parameter_estimation="ir_model_non_identif_param_estim.yaml"), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
