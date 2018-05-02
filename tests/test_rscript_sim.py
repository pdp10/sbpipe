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
