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


class TestRPE(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _rscript_folder = 'r_models'
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(cls._rscript_folder)
        if not is_r_package_installed("reshape2"):
            cls._output = "R reshape2 not found: SKIP ... "
        elif not is_r_package_installed("deSolve"):
            cls._output = "R deSolve not found: SKIP ... "
        elif not is_r_package_installed("minpack.lm"):
            cls._output = "R minpack.lm not found: SKIP ... "

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pe_r(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(parameter_estimation="pe_simple_reacts.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    # Commented as it can take too much time on Travis-CI.
    #def test_insulin_receptor_pe_r(self):
    #   if self._output == 'OK':
    #       self.assertEqual(sbpipe(parameter_estimation="insulin_receptor_param_estim.yaml", quiet=True), 0)
    #   else:
    #       sys.stdout.write(self._output)
    #       sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
