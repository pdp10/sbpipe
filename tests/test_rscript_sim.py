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


class TestRSim(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _rscript_folder = os.path.join('r_models')

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._rscript_folder))

    @classmethod
    def tearDownClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sim_r_lotka_volterra(self):
        try:
            output = subprocess.Popen(['Rscript',
                                       os.path.join(SBPIPE, "scripts", "is_package_installed.r"), "deSolve"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                sys.stdout.write("R deSolve not found: SKIP ... ")
                sys.stdout.flush()
            else:
                self.assertEqual(sbmain.sbpipe(simulate="simple_lotka_volterra.yaml", quiet=True), 0)
        except OSError as e:
            sys.stdout.write("R not found: SKIP ... ")
            sys.stdout.flush()

    def test_sim_r_pde_lotka_volterra(self):
        try:
            output = subprocess.Popen(['Rscript',
                                       os.path.join(SBPIPE, "scripts", "is_package_installed.r"), "deSolve"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                sys.stdout.write("R deSolve not found: SKIP ... ")
                sys.stdout.flush()
            else:
                self.assertEqual(sbmain.sbpipe(simulate="2Dpde_lotka_volterra.yaml", quiet=True), 0)
        except OSError as e:
            sys.stdout.write("R not found: SKIP ... ")
            sys.stdout.flush()

    def test_stoch_sim_r_periodic_drift(self):
        try:
            output = subprocess.Popen(['Rscript',
                                       os.path.join(SBPIPE, "scripts", "is_package_installed.r"), "sde"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                sys.stdout.write("R sde not found: SKIP ... ")
                sys.stdout.flush()
            else:
                self.assertEqual(sbmain.sbpipe(simulate="sde_periodic_drift.yaml", quiet=True), 0)
        except OSError as e:
            sys.stdout.write("R not found: SKIP ... ")
            sys.stdout.flush()

    def test_stoch_sim_r_cox_ingersoll_ross_process(self):
        try:
            output = subprocess.Popen(['Rscript',
                                       os.path.join(SBPIPE, "scripts", "is_package_installed.r"), "sde"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(output):
                sys.stdout.write("R sde not found: SKIP ... ")
                sys.stdout.flush()
            else:
                self.assertEqual(sbmain.sbpipe(simulate="sde_cox_ingersoll_ross_process.yaml", quiet=True), 0)
        except OSError as e:
            sys.stdout.write("R not found: SKIP ... ")
            sys.stdout.flush()

    def test_sim_r(self):
        try:
            reshape2 = subprocess.Popen(['Rscript',
                                       os.path.join(SBPIPE, "scripts", "is_package_installed.r"), "reshape2"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            desolve = subprocess.Popen(['Rscript',
                                       os.path.join(SBPIPE, "scripts", "is_package_installed.r"), "deSolve"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            minpacklm = subprocess.Popen(['Rscript',
                                       os.path.join(SBPIPE, "scripts", "is_package_installed.r"), "minpack.lm"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
            if "FALSE" in str(reshape2):
                sys.stdout.write("R reshape2 not found: SKIP ... ")
                sys.stdout.flush()
            if "FALSE" in str(desolve):
                sys.stdout.write("R deSolve not found: SKIP ... ")
                sys.stdout.flush()
            elif "FALSE" in str(minpacklm):
                sys.stdout.write("R minpack.lm not found: SKIP ... ")
                sys.stdout.flush()
            else:
                self.assertEqual(sbmain.sbpipe(simulate="sim_simple_reacts.yaml", quiet=True), 0)
        except OSError as e:
            sys.stdout.write("R not found: SKIP ... ")
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
