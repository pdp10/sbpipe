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
from sbpipe.utils.dependencies import is_py_package_installed


class TestPythonSim(unittest.TestCase):

    _orig_wd = os.getcwd()
    _python_folder = 'python_models'
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(cls._python_folder)
        if not is_py_package_installed("numpy"):
            cls._output = "Python numpy not found: SKIP ... "
        elif not is_py_package_installed("scipy"):
            cls._output = "Python scipy not found: SKIP ... "
        elif not is_py_package_installed("pandas"):
            cls._output = "Python pandas not found: SKIP ... "

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sim_python_ir(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="insulin_receptor.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

if __name__ == '__main__':
    unittest.main(verbosity=2)
