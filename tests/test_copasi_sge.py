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
import subprocess
import sys
import unittest
from tests.context import sbpipe


class TestCopasiSGE(unittest.TestCase):

    _orig_wd = os.getcwd()
    _ir_folder = 'sge'
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(cls._ir_folder)
        try:
            subprocess.Popen(['CopasiSE'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()[0]
        except OSError as e:
            cls._output = 'CopasiSE not found: SKIP ... '
            return
        try:
            subprocess.Popen(['qstat'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()[0]
        except OSError as e:
            cls._output = 'SGE not found: SKIP ... '

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_stoch_sim_copasi_sge(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="sge_ir_model_stoch_simul.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_pe_copasi_sge(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_estimation="sge_ir_model_param_estim.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_pe_copasi_sge(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_estimation="sge_ir_model_stoch_param_estim.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_ps1_copasi_sge(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan1="sge_ir_model_ir_beta_inhib_stoch.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_ps2_copasi_sge(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan2="sge_ir_model_insulin_ir_beta_dbl_stoch_inhib.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
