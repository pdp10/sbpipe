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
insulin_receptor_folder = os.path.join('insulin_receptor','Working_Folder')

# import paths to the resource folders
sys.path.append(os.path.join(SB_PIPE, 'tests', insulin_receptor_folder))

# import modules
from test_insulin_receptor_simulate import TestInsulinReceptorSimulate
from test_insulin_receptor_param_scan import TestInsulinReceptorParamScan
from test_insulin_receptor_param_estim import TestInsulinReceptorParamEstim
from test_insulin_receptor_sensitivity import TestInsulinReceptorSensitivity
from test_insulin_receptor_lsf import TestInsulinReceptorLSF
from test_insulin_receptor_sge import TestInsulinReceptorSGE



"""
Test suite and runner
"""

#def create_suite():
  #"""A suite of tests to run."""
  ## Load the tests for these test cases
  #suite1 = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptor)
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
  os.chdir(os.path.join(os.path.abspath(sys.path[0]), insulin_receptor_folder))
  suiteSimulate = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptorSimulate)
  suiteParamScan = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptorParamScan)
  suiteParamEstim = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptorParamEstim)
  suiteSensitivity = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptorSensitivity)  
  suiteLSF = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptorLSF)  
  suiteSGE = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptorSGE)  
  suite = unittest.TestSuite([suiteSimulate, suiteParamScan, suiteParamEstim, suiteSensitivity, suiteLSF, suiteSGE])
  unittest.TextTestRunner(verbosity=2).run(suite)
  os.chdir(origWD) # get back to our original working directory



main(sys.argv)

