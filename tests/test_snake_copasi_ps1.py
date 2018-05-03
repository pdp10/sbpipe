#!/usr/bin/env python3
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


import sys
import os
import unittest
import subprocess
from tests.context import sbpipe
from sbpipe.utils.dependencies import is_py_package_installed


class TestPs1Snake(unittest.TestCase):

    _orig_wd = os.getcwd()
    _ir_folder = 'snakemake'
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
        if not is_py_package_installed('sbpipe'):
            cls._output = 'sbpipe not installed: SKIP ... '
        if not is_py_package_installed('snakemake'):
            cls._output = 'snakemake not installed: SKIP ... '
        if not os.path.exists('sbpipe_pe.snake'):
            cls._output = 'snakemake workflow not found: SKIP ... '

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ps1_det1_snake(self):
        if self._output == 'OK':
            from snakemake import snakemake
            self.assertTrue(
                snakemake(snakefile='sbpipe_ps1.snake',
                          configfile='ir_model_k1_scan.yaml',
                          cores=7,
                          forceall=True,
                          quiet=True))
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_det2_snake(self):
        if self._output == 'OK':
            from snakemake import snakemake
            self.assertTrue(
                snakemake(snakefile='sbpipe_ps1.snake',
                          configfile='ir_model_ir_beta_inhib.yaml',
                          cores=7,
                          forceall=True,
                          quiet=True))
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_det3_snake(self):
        if self._output == 'OK':
            from snakemake import snakemake
            self.assertTrue(
                snakemake(snakefile='sbpipe_ps1.snake',
                          configfile='ir_model_ir_beta_inhib_overexp.yaml',
                          cores=7,
                          forceall=True,
                          quiet=True))
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps1_stoch_snake(self):
        if self._output == 'OK':
            from snakemake import snakemake
            self.assertTrue(
                snakemake(snakefile='sbpipe_ps1.snake',
                          configfile='ir_model_ir_beta_inhib_stoch.yaml',
                          cores=7,
                          forceall=True,
                          quiet=True))
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
