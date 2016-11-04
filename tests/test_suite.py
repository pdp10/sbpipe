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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-27 10:18:32 $

import os
import sys
import unittest
SBPIPE = os.environ["SBPIPE"]
# folders containing the configuration files and test file
ir_folder = os.path.join('insulin_receptor', 'Working_Folder')
# import paths to the resource folders
sys.path.append(os.path.join(SBPIPE, 'tests', ir_folder))
# import modules
from test_ir_simulate import TestIRSimulate
from test_ir_single_param_scan import TestIRSingleParamScan
from test_ir_double_param_scan import TestIRDoubleParamScan
from test_ir_param_estim import TestIRParamEstim
from test_ir_sensitivity import TestIRSensitivity
from test_ir_lsf import TestIRLSF
from test_ir_sge import TestIRSGE


# def create_suite():
# """
# Test suite and runner
# """
# Load the tests for these test cases
# suite1 = unittest.TestLoader().loadTestsFromTestCase(TestIR)
# suite2 = unittest.TestLoader().loadTestsFromTestCase("SOMETHING_ELSE")
# alltests = unittest.TestSuite([suite1, suite2])
# alltests = unittest.TestSuite([suite1])
# return alltests


def run_sbpipe_tests():
    """
    Run a suite of tests for the sbpipe package
    """
    # suite = create_suite()
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # For each test, we need to change directory.
    orig_wd = os.getcwd()  # remember our original working directory
    os.chdir(os.path.join(SBPIPE, 'tests', ir_folder))
    suite_simulate = unittest.TestLoader().loadTestsFromTestCase(TestIRSimulate)
    suite_sps = unittest.TestLoader().loadTestsFromTestCase(TestIRSingleParamScan)
    suite_dps = unittest.TestLoader().loadTestsFromTestCase(TestIRDoubleParamScan)
    suite_pe = unittest.TestLoader().loadTestsFromTestCase(TestIRParamEstim)
    suite_sens = unittest.TestLoader().loadTestsFromTestCase(TestIRSensitivity)
    suite_lsf = unittest.TestLoader().loadTestsFromTestCase(TestIRLSF)
    suite_sge = unittest.TestLoader().loadTestsFromTestCase(TestIRSGE)
    suite = unittest.TestSuite([suite_simulate, suite_sps, suite_dps, suite_pe, suite_sens, suite_lsf, suite_sge])
    unittest.TextTestRunner(verbosity=2).run(suite)
    os.chdir(orig_wd)  # get back to our original working directory


def main(args):
    # Clean the tests (note cleanup_tests has a main() so it runs when imported.
    import tests.cleanup_tests
    tests.cleanup_tests
    # Run the test suite
    run_sbpipe_tests()


main(sys.argv)
