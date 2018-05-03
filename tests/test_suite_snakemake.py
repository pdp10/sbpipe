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


import os
import shutil
import unittest

from tests.context import sbpipe
from sbpipe.utils.dependencies import which
import tests.test_snake_copasi_pe as snake_copasi_pe
import tests.test_snake_copasi_ps1 as snake_copasi_ps1
import tests.test_snake_copasi_ps2 as snake_copasi_ps2
import tests.test_snake_copasi_sim as snake_copasi_sim
from sbpipe.utils.io import git_retrieve


class TestSuite(unittest.TestCase):

    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        sbpipe_snake_folder = 'sbpipe_snake'
        orig_wd = os.getcwd()
        os.chdir('snakemake')
        if which('git') is None and os.path.isdir(sbpipe_snake_folder):
            cls._output = 'git was not found. SKIP snakemake tests'
            return
        print('retrieving Snakemake workflows for SBpipe')
        git_retrieve('https://github.com/pdp10/sbpipe_snake.git')
        source = os.listdir(sbpipe_snake_folder)
        destination = os.getcwd()
        for f in source:
            if f.endswith('.snake'):
                shutil.move(os.path.join(os.path.abspath(sbpipe_snake_folder), f),
                            os.path.join(destination, f))
        shutil.rmtree(sbpipe_snake_folder)
        os.chdir(orig_wd)

    def test_suites(self):

        if self._output == 'OK':
            # Run Snakemake tests
            suite_snake_copasi_sim = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_sim.TestSimSnake)
            suite_snake_copasi_pe = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_pe.TestPeSnake)
            suite_snake_copasi_ps1 = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_ps1.TestPs1Snake)
            suite_snake_copasi_ps2 = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_ps2.TestPs2Snake)

            # combine all the test suites
            suite = unittest.TestSuite([suite_snake_copasi_sim,
                                        suite_snake_copasi_pe,
                                        suite_snake_copasi_ps1,
                                        suite_snake_copasi_ps2])
        else:
            suite = unittest.TestSuite()

        # run the combined test suite
        self.assertTrue(unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())


if __name__ == "__main__":
    unittest.main(verbosity=2)
