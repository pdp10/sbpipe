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
from sbpipe.utils.io import git_retrieve

import tests.test_copasi_sim as copasi_sim
import tests.test_copasi_ps1 as copasi_ps1
import tests.test_copasi_ps2 as copasi_ps2
import tests.test_copasi_pe as copasi_pe
import tests.test_copasi_lsf as copasi_lsf
import tests.test_copasi_sge as copasi_sge

import tests.test_conferr_sim as conf_err_sim
import tests.test_conferr_ps1 as conf_err_ps1
import tests.test_conferr_ps2 as conf_err_ps2
import tests.test_conferr_pe as conf_err_pe

import tests.test_interrupt_pe as interrupt_pe

import tests.test_rscript_sim as conf_rscript_sim
import tests.test_rscript_pe as conf_rscript_pe
import tests.test_python_sim as conf_python
import tests.test_java_sim as conf_java
import tests.test_octave_sim as conf_octave

import tests.test_snake_copasi_pe as snake_copasi_pe
import tests.test_snake_copasi_sim as snake_copasi_sim
import tests.test_snake_copasi_ps1 as snake_copasi_ps1
import tests.test_snake_copasi_ps2 as snake_copasi_ps2


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

        # Clean the tests (note cleanup_tests has a main() so it runs when imported.
        #cleanup.main()

        # Run negative test suites
        suite_copasi_sim = unittest.TestLoader().loadTestsFromTestCase(copasi_sim.TestCopasiSim)
        suite_copasi_ps1 = unittest.TestLoader().loadTestsFromTestCase(copasi_ps1.TestCopasiPS1)
        suite_copasi_ps2 = unittest.TestLoader().loadTestsFromTestCase(copasi_ps2.TestCopasiPS2)
        suite_copasi_pe = unittest.TestLoader().loadTestsFromTestCase(copasi_pe.TestCopasiPE)
        suite_copasi_lsf = unittest.TestLoader().loadTestsFromTestCase(copasi_lsf.TestCopasiLSF)
        suite_copasi_sge = unittest.TestLoader().loadTestsFromTestCase(copasi_sge.TestCopasiSGE)

        # Run positive test suites
        suite_conferr_sim = unittest.TestLoader().loadTestsFromTestCase(conf_err_sim.TestCopasiSim)
        suite_conferr_ps1 = unittest.TestLoader().loadTestsFromTestCase(conf_err_ps1.TestCopasiPS1)
        suite_conferr_ps2 = unittest.TestLoader().loadTestsFromTestCase(conf_err_ps2.TestCopasiPS2)
        suite_conferr_pe = unittest.TestLoader().loadTestsFromTestCase(conf_err_pe.TestCopasiPE)

        # Test cases when a parameter estimation failed.
        suite_interrupt_pe = unittest.TestLoader().loadTestsFromTestCase(interrupt_pe.TestCopasiPE)

        # Run Rscript test
        suite_rscript_sim = unittest.TestLoader().loadTestsFromTestCase(conf_rscript_sim.TestRSim)
        suite_rscript_pe = unittest.TestLoader().loadTestsFromTestCase(conf_rscript_pe.TestRPE)

        # Run Python test
        suite_python_sim = unittest.TestLoader().loadTestsFromTestCase(conf_python.TestPythonSim)

        # Run Java test
        suite_java_sim = unittest.TestLoader().loadTestsFromTestCase(conf_java.TestJavaSim)

        # Run Octave test
        suite_octave_sim = unittest.TestLoader().loadTestsFromTestCase(conf_octave.TestOctaveSim)

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
                                        suite_snake_copasi_ps2,
                                        suite_copasi_sim,
                                        suite_copasi_ps1,
                                        suite_copasi_ps2,
                                        suite_copasi_pe,
                                        suite_copasi_lsf,
                                        suite_copasi_sge,
                                        suite_conferr_sim,
                                        suite_conferr_ps1,
                                        suite_conferr_ps2,
                                        suite_conferr_pe,
                                        suite_interrupt_pe,
                                        suite_rscript_sim,
                                        suite_rscript_pe,
                                        suite_python_sim,
                                        suite_java_sim,
                                        suite_octave_sim])
        else:
            # combine all the test suites
            suite = unittest.TestSuite([suite_copasi_sim,
                                        suite_copasi_ps1,
                                        suite_copasi_ps2,
                                        suite_copasi_pe,
                                        suite_copasi_lsf,
                                        suite_copasi_sge,
                                        suite_conferr_sim,
                                        suite_conferr_ps1,
                                        suite_conferr_ps2,
                                        suite_conferr_pe,
                                        suite_interrupt_pe,
                                        suite_rscript_sim,
                                        suite_rscript_pe,
                                        suite_python_sim,
                                        suite_java_sim,
                                        suite_octave_sim])

        # run the combined test suite
        self.assertTrue(unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())


if __name__ == "__main__":
    unittest.main(verbosity=2)
