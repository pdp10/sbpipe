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


class TestCopasiPS1(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _ir_folder = os.path.join('config_errors')
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._ir_folder))
        try:
            subprocess.Popen(['CopasiSE'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()[0]
        except OSError as e:
            cls._output = 'CopasiSE not found: SKIP ... '

    @classmethod
    def tearDownClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ps1_ci1(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan1.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci2(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan2.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci3(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan3.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci4(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan4.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci5(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan5.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci6(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan6.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci7(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan7.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci8(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan8.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_ci9(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(parameter_scan1="ir_model_k1_scan9.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
