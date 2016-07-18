#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-27 10:18:32 $


import os, sys
import unittest


SB_PIPE = os.environ["SB_PIPE"]
# folders containing the configuration files and test file
ir_folder = os.path.join('insulin_receptor','Working_Folder')

# import paths to the resource folders
sys.path.append(os.path.join(SB_PIPE, 'tests', ir_folder))

# import modules
from test_ir_simulate import TestIRSimulate
from test_ir_param_scan import TestIRParamScan
from test_ir_param_estim import TestIRParamEstim
from test_ir_sensitivity import TestIRSensitivity
from test_ir_lsf import TestIRLSF
from test_ir_sge import TestIRSGE



"""
Test suite and runner
"""

#def create_suite():
  #"""A suite of tests to run."""
  ## Load the tests for these test cases
  #suite1 = unittest.TestLoader().loadTestsFromTestCase(TestIR)
  ##suite2 = unittest.TestLoader().loadTestsFromTestCase("SOMETHING_ELSE")
  ##alltests = unittest.TestSuite([suite1, suite2])
  #alltests = unittest.TestSuite([suite1])
  #return alltests



def main(args):
  """Run a suite of tests."""
  #suite = create_suite()
  #unittest.TextTestRunner(verbosity=2).run(suite)

  # For each test, we need to change directory.
  origWD = os.getcwd() # remember our original working directory
  os.chdir(os.path.join(os.path.abspath(sys.path[0]), ir_folder))
  suiteSimulate = unittest.TestLoader().loadTestsFromTestCase(TestIRSimulate)
  suiteParamScan = unittest.TestLoader().loadTestsFromTestCase(TestIRParamScan)
  suiteParamEstim = unittest.TestLoader().loadTestsFromTestCase(TestIRParamEstim)
  suiteSensitivity = unittest.TestLoader().loadTestsFromTestCase(TestIRSensitivity)  
  suiteLSF = unittest.TestLoader().loadTestsFromTestCase(TestIRLSF)  
  suiteSGE = unittest.TestLoader().loadTestsFromTestCase(TestIRSGE)  
  suite = unittest.TestSuite([suiteSimulate, suiteParamScan, suiteParamEstim, suiteSensitivity, suiteLSF, suiteSGE])
  unittest.TextTestRunner(verbosity=2).run(suite)
  os.chdir(origWD) # get back to our original working directory



main(sys.argv)

