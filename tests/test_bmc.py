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
import subprocess
from tests.context import sbpipe


import unittest


class TestBMCSysBio(unittest.TestCase):
    """ Test suite for reproducing figures in Dalle Pezze and Le Novère, 2017, BMC Systems Biology. """

    _orig_wd = os.getcwd()
    _ir_folder = 'insulin_receptor'
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

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Simulation
    def test_sim_copasi(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="ir_model_det_simul.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_sim_copasi(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="ir_model_stoch_simul.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    # 1 parameter scan
    def test_ps1_ci(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan1="ir_model_k1_scan.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_inhib_only(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan1="ir_model_ir_beta_inhib.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_ps1_inhib_only(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan1="ir_model_ir_beta_inhib_stoch.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_inhib_overexp(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan1="ir_model_ir_beta_inhib_overexp.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    # 2 parameter scan
    def test_ps2_inhib_only(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_ps2_inhib_only(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_stoch_inhib.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    # parameter estimation
    def test_pe_copasi1(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_estimation="ir_model_param_estim.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_pe_copasi2(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_estimation="ir_model_non_identif_param_estim.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    # SGE
    def test_stoch_sim_copasi_sge(self):
        if self._output == 'OK':
            try:
                subprocess.Popen(['qstat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                self.assertEqual(sbpipe(simulate="sge_ir_model_stoch_simul.yaml", quiet=True), 0)
            except OSError as e:
                print("Skipping test as no SGE (Sun Grid Engine) was found.")
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_pe_copasi_sge(self):
        if self._output == 'OK':
            try:
                subprocess.Popen(['qstat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                self.assertEqual(sbpipe(parameter_estimation="sge_ir_model_param_estim.yaml", quiet=True), 0)
            except OSError as e:
                print("Skipping test as no SGE (Sun Grid Engine) was found.")
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_pe_copasi_sge(self):
        if self._output == 'OK':
            try:
                subprocess.Popen(['qstat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                self.assertEqual(sbpipe(parameter_estimation="sge_ir_model_stoch_param_estim.yaml", quiet=True), 0)
            except OSError as e:
                print("Skipping test as no SGE (Sun Grid Engine) was found.")
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    # LSF
    def test_stoch_sim_copasi_lsf(self):
        if self._output == 'OK':
            try:
                subprocess.Popen(['bjobs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                self.assertEqual(sbpipe(simulate="lsf_ir_model_stoch_simul.yaml", quiet=True), 0)
            except OSError as e:
                print("Skipping test as no LSF (Load Sharing Facility) was found.")
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_pe_copasi_lsf(self):
        if self._output == 'OK':
            try:
                subprocess.Popen(['bjobs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                self.assertEqual(sbpipe(parameter_estimation="lsf_ir_model_param_estim.yaml", quiet=True), 0)
            except OSError as e:
                print("Skipping test as no LSF (Load Sharing Facility) was found.")
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_stoch_pe_copasi_lsf(self):
        if self._output == 'OK':
            try:
                subprocess.Popen(['bjobs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                self.assertEqual(sbpipe(parameter_estimation="lsf_ir_model_stoch_param_estim.yaml", quiet=True), 0)
            except OSError as e:
                print("Skipping test as no LSF (Load Sharing Facility) was found.")
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
