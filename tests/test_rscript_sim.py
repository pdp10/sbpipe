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


import os
import sys
import unittest
from tests.context import sbpipe
from sbpipe.utils.dependencies import is_r_package_installed


class TestRSim(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _rscript_folder = 'r_models'

    @classmethod
    def setUpClass(cls):
        os.chdir(cls._rscript_folder)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sim_r_lotka_volterra(self):
        if not is_r_package_installed("deSolve"):
            sys.stdout.write("R deSolve not found: SKIP ... ")
            sys.stdout.flush()
        else:
            self.assertEqual(sbpipe(simulate="simple_lotka_volterra.yaml", quiet=True), 0)

    def test_sim_r_pde_lotka_volterra(self):
        if not is_r_package_installed("deSolve"):
            sys.stdout.write("R deSolve not found: SKIP ... ")
            sys.stdout.flush()
        else:
            self.assertEqual(sbpipe(simulate="2Dpde_lotka_volterra.yaml", quiet=True), 0)

    def test_stoch_sim_r_periodic_drift(self):
        if not is_r_package_installed("sde"):
            sys.stdout.write("R sde not found: SKIP ... ")
            sys.stdout.flush()
        else:
            self.assertEqual(sbpipe(simulate="sde_periodic_drift.yaml", quiet=True), 0)

    def test_stoch_sim_r_cox_ingersoll_ross_process(self):
        if not is_r_package_installed("sde"):
            sys.stdout.write("R sde not found: SKIP ... ")
            sys.stdout.flush()
        else:
            self.assertEqual(sbpipe(simulate="sde_cox_ingersoll_ross_process.yaml", quiet=True), 0)

    def test_sim_r(self):
        if not is_r_package_installed("reshape2"):
            sys.stdout.write("R reshape2 not found: SKIP ... ")
            sys.stdout.flush()
        elif not is_r_package_installed("deSolve"):
            sys.stdout.write("R deSolve not found: SKIP ... ")
            sys.stdout.flush()
        elif not is_r_package_installed("minpack.lm"):
            sys.stdout.write("R minpack.lm not found: SKIP ... ")
            sys.stdout.flush()
        else:
            self.assertEqual(sbpipe(simulate="sim_simple_reacts.yaml", quiet=True), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
