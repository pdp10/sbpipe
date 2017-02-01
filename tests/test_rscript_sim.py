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

SBPIPE = os.environ["SBPIPE"]
sys.path.append(SBPIPE)
from sbpipe import main as sbmain
import unittest
import subprocess

"""Unit test for R simulator"""


class TestRscriptSim(unittest.TestCase):
    """
    A collection of tests for this example.
    """

    _orig_wd = os.getcwd()  # remember our original working directory
    _rscript = os.path.join('r_models')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._rscript))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_simple_lotka_volterra_simulation(self):
        """Simple Lotka-Volterra model simulation"""
        try:
            output = subprocess.Popen(['Rscript', \
                                       os.path.join(SBPIPE, "sbpipe", "R", "is_package_installed.r"), "deSolve"], \
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                print("Skipping test as R deSolve was not found.")
            else:
                self.assertEqual(sbmain.main(["sbpipe", "--simulate", "simple_lotka_volterra.conf"]), 0)
        except OSError as e:
            print("Skipping test as R was not found.")

    def test_2Dpde_lotka_volterra_simulation(self):
        """2D partial differential equation Lotka-Volterra model simulation"""
        try:
            output = subprocess.Popen(['Rscript', \
                                       os.path.join(SBPIPE, "sbpipe", "R", "is_package_installed.r"), "deSolve"], \
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                print("Skipping test as R deSolve was not found.")
            else:
                self.assertEqual(sbmain.main(["sbpipe", "--simulate", "2Dpde_lotka_volterra.conf"]), 0)
        except OSError as e:
            print("Skipping test as R was not found.")

    def test_sde_periodic_drift(self):
        """Stochastic differential equation simulation - periodic drift"""
        try:
            output = subprocess.Popen(['Rscript', \
                                       os.path.join(SBPIPE, "sbpipe", "R", "is_package_installed.r"), "sde"], \
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                print("Skipping test as R sde was not found.")
            else:
                self.assertEqual(sbmain.main(["sbpipe", "--simulate", "sde_periodic_drift.conf"]), 0)
        except OSError as e:
            print("Skipping test as R was not found.")

    def test_sde_cox_ingersoll_ross_process(self):
        """Stochastic differential equation simulation - cox_ingersoll_ross_process"""
        try:
            output = subprocess.Popen(['Rscript', \
                                       os.path.join(SBPIPE, "sbpipe", "R", "is_package_installed.r"), "sde"], \
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                print("Skipping test as R sde was not found.")
            else:
                self.assertEqual(sbmain.main(["sbpipe", "--simulate", "sde_cox_ingersoll_ross_process.conf"]), 0)
        except OSError as e:
            print("Skipping test as R was not found.")

    def test_sim_simple_reacts(self):
        """A simple R model whose parameters have been estimated using sbpipe"""
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
                self.assertEqual(sbmain.main(["sbpipe", "--simulate", "sim_simple_reacts.conf"]), 0)
        except OSError as e:
            print("Skipping test as R was not found.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
