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
# Object: run a list of tests for the insulin receptor model using LSF (Platform Load Sharing Facility)
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $

import os
import subprocess
import sys

SBPIPE = os.environ["SBPIPE"]
sys.path.append(SBPIPE)
from sbpipe import main as sbmain
import unittest

"""Unit test for Insulin Receptor"""


class TestIRLSF(unittest.TestCase):
    """
    A collection of tests for this example using LSF
    """

    _orig_wd = os.getcwd()  # remember our original working directory
    _ir_folder = os.path.join('insulin_receptor', 'Working_Folder')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._ir_folder))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_stoch_simul_copasi_lsf(self):
        """model simulation using LSF if found"""
        try:
            subprocess.Popen(['bjobs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(sbmain.main(["sbpipe", "--simulate", "lsf_ir_model_stoch_simul.conf"]), 0)
        except OSError as e:
            print("Skipping test as no LSF (Load Sharing Facility) was found.")

    def test_param_estim_copasi_lsf(self):
        """model parameter estimation using LSF if found"""
        try:
            subprocess.Popen(['bjobs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(sbmain.main(["sbpipe", "--param-estim", "lsf_ir_model_param_estim.conf"]), 0)
        except OSError as e:
            print("Skipping test as no LSF (Load Sharing Facility) was found.")
            
    def test_stoch_param_estim_copasi_lsf(self):
        """model stochastic parameter estimation using LSF if found"""
        try:
            subprocess.Popen(['bjobs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(sbmain.main(["sbpipe", "--param-estim", "lsf_ir_model_stoch_param_estim.conf"]), 0)
        except OSError as e:
            print("Skipping test as no LSF (Load Sharing Facility) was found.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
