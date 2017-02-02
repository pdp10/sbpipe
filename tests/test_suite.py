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
SBPIPE = os.environ["SBPIPE"]
sys.path.append(os.path.join(SBPIPE))
import tests.cleanup_tests as cleanup

import tests.test_ok_sim as ok_sim
import tests.test_ok_ps1 as ok_ps1
import tests.test_ok_ps2 as ok_ps2
import tests.test_ok_pe as ok_pe
import tests.test_ok_lsf as ok_lsf
import tests.test_ok_sge as ok_sge

import tests.test_conferr_sim as conf_err_sim
import tests.test_conferr_ps1 as conf_err_ps1
import tests.test_conferr_ps2 as conf_err_ps2
import tests.test_conferr_pe as conf_err_pe
import tests.test_conferr_sge as conf_err_sge

import tests.test_rscript_sim as conf_rscript_sim
import tests.test_rscript_pe as conf_rscript_pe
import tests.test_python_sim as conf_python
import tests.test_java_sim as conf_java
import tests.test_octave_sim as conf_octave

import tests.test_ok_ps1_snake as ok_ps1_snake
import tests.test_ok_ps2_snake as ok_ps2_snake


class TestSuite(unittest.TestCase):

    def run_tests_suites(self):

        # Clean the tests (note cleanup_tests has a main() so it runs when imported.
        #cleanup.main()

        # Run negative test suites
        suite_ok_sim = unittest.TestLoader().loadTestsFromTestCase(ok_sim.TestCopasiSim)
        suite_ok_ps1 = unittest.TestLoader().loadTestsFromTestCase(ok_ps1.TestCopasiPS1)
        suite_ok_ps2 = unittest.TestLoader().loadTestsFromTestCase(ok_ps2.TestCopasiPS2)
        suite_ok_pe = unittest.TestLoader().loadTestsFromTestCase(ok_pe.TestCopasiPE)
        suite_ok_lsf = unittest.TestLoader().loadTestsFromTestCase(ok_lsf.TestCopasiLSF)
        suite_ok_sge = unittest.TestLoader().loadTestsFromTestCase(ok_sge.TestCopasiSGE)


        # Run positive test suites
        suite_conferr_sim = unittest.TestLoader().loadTestsFromTestCase(conf_err_sim.TestCopasiSim)
        suite_conferr_ps1 = unittest.TestLoader().loadTestsFromTestCase(conf_err_ps1.TestCopasiPS1)
        suite_conferr_ps2 = unittest.TestLoader().loadTestsFromTestCase(conf_err_ps2.TestCopasiPS2)
        suite_conferr_pe = unittest.TestLoader().loadTestsFromTestCase(conf_err_pe.TestCopasiPE)
        suite_conferr_sge = unittest.TestLoader().loadTestsFromTestCase(conf_err_sge.TestCopasiSGE)

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
        suite_ok_ps1_snake = unittest.TestLoader().loadTestsFromTestCase(ok_ps1_snake.TestPs1Snake)
        suite_ok_ps2_snake = unittest.TestLoader().loadTestsFromTestCase(ok_ps2_snake.TestPs2Snake)

        # combine all the test suites
        suite = unittest.TestSuite([suite_ok_sim,
                                    suite_ok_ps1,
                                    suite_ok_ps2,
                                    suite_ok_pe,
                                    suite_ok_lsf,
                                    suite_ok_sge,
                                    suite_conferr_sim,
                                    suite_conferr_ps1,
                                    suite_conferr_ps2,
                                    suite_conferr_pe,
                                    suite_conferr_sge,
                                    suite_rscript_sim,
                                    suite_rscript_pe,
                                    suite_python_sim,
                                    suite_java_sim,
                                    suite_octave_sim,
                                    suite_ok_ps1_snake,
                                    suite_ok_ps2_snake])

        # run the combined test suite
        self.assertTrue(unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())


if __name__ == "__main__":
    unittest.main()
