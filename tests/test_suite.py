#!/usr/bin/env python3
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
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-27 10:18:32 $

import os
import sys
import unittest

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(SBPIPE)
import tests.cleanup_tests as cleanup

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

        # Run Snakemake tests
        suite_snake_copasi_pe = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_pe.TestPeSnake)
        suite_snake_copasi_sim = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_sim.TestSimSnake)
        suite_snake_copasi_ps1 = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_ps1.TestPs1Snake)
        suite_snake_copasi_ps2 = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_ps2.TestPs2Snake)

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
                                    suite_octave_sim,
                                    suite_snake_copasi_pe,
                                    suite_snake_copasi_sim,
                                    suite_snake_copasi_ps1,
                                    suite_snake_copasi_ps2])

        # run the combined test suite
        self.assertTrue(unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())


if __name__ == "__main__":
    unittest.main(verbosity=2)
