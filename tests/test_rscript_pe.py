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
import subprocess


class TestRPE(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _rscript = os.path.join('r_models')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._rscript))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_pe_r(self):
        try:
            reshape2 = subprocess.Popen(['Rscript', \
                                       os.path.join(SBPIPE, "sbpipe", "R", "is_package_installed.r"), "reshape2"], \
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            desolve = subprocess.Popen(['Rscript', \
                                       os.path.join(SBPIPE, "sbpipe", "R", "is_package_installed.r"), "deSolve"], \
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            minpacklm = subprocess.Popen(['Rscript', \
                                       os.path.join(SBPIPE, "sbpipe", "R", "is_package_installed.r"), "minpack.lm"], \
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(reshape2):
                print("Skipping test as R reshape2 was not found.")
            if "FALSE" in str(desolve):
                print("Skipping test as R deSolve was not found.")
            elif "FALSE" in str(minpacklm):
                print("Skipping test as R minpack.lm was not found.")
            else:
                self.assertEqual(sbmain.sbpipe(parameter_estimation="pe_simple_reacts.yaml", quiet=True), 0)
        except OSError as e:
            print("Skipping test as R was not found.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
