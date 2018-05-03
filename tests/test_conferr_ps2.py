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
import subprocess
from tests.context import sbpipe


class TestCopasiPS2(unittest.TestCase):

    _orig_wd = os.getcwd()
    _ir_folder = 'config_errors'
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

    # skip this test because it is:
    # 0, if the optional Python binding code for COPASI is not found,
    # 1, otherwise
    #def test_ps2_inhib_only1(self):
    #    if self._output == 'OK':
    #        self.assertEqual(
    #           sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib1.yaml", quiet=True), 1)
    #    else:
    #        sys.stdout.write(self._output)
    #        sys.stdout.flush()

    def test_ps2_inhib_only2(self):
        if self._output == 'OK':
            self.assertEqual(
                sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib2.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps2_inhib_only3(self):
        if self._output == 'OK':
            self.assertEqual(
                sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib3.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
