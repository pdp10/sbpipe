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
import tests.test_ok_sens as ok_sens
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

def run_tests_suites():
    # Clean the tests (note cleanup_tests has a main() so it runs when imported.
    cleanup.main()

    # Run negative test suites
    suite_ok_sim = unittest.TestLoader().loadTestsFromTestCase(ok_sim.TestIRSimulate)
    suite_ok_ps1 = unittest.TestLoader().loadTestsFromTestCase(ok_ps1.TestIRSingleParamScan)
    suite_ok_ps2 = unittest.TestLoader().loadTestsFromTestCase(ok_ps2.TestIRDoubleParamScan)
    suite_ok_pe = unittest.TestLoader().loadTestsFromTestCase(ok_pe.TestIRParamEstim)
    suite_ok_sens = unittest.TestLoader().loadTestsFromTestCase(ok_sens.TestIRSensitivity)
    suite_ok_lsf = unittest.TestLoader().loadTestsFromTestCase(ok_lsf.TestIRLSF)
    suite_ok_sge = unittest.TestLoader().loadTestsFromTestCase(ok_sge.TestIRSGE)


    # Run positive test suites
    suite_conferr_sim = unittest.TestLoader().loadTestsFromTestCase(conf_err_sim.TestIRSimulate)
    suite_conferr_ps1 = unittest.TestLoader().loadTestsFromTestCase(conf_err_ps1.TestIRSingleParamScan)
    suite_conferr_ps2 = unittest.TestLoader().loadTestsFromTestCase(conf_err_ps2.TestIRDoubleParamScan)
    suite_conferr_pe = unittest.TestLoader().loadTestsFromTestCase(conf_err_pe.TestIRParamEstim)
    suite_conferr_sge = unittest.TestLoader().loadTestsFromTestCase(conf_err_sge.TestIRSGE)

    # Run Rscript test
    suite_rscript_sim = unittest.TestLoader().loadTestsFromTestCase(conf_rscript_sim.TestRscriptSim)
    suite_rscript_pe = unittest.TestLoader().loadTestsFromTestCase(conf_rscript_pe.TestRscriptPE)

    # Run Python test
    suite_python_sim = unittest.TestLoader().loadTestsFromTestCase(conf_python.TestPythonSim)

    # Run Java test
    suite_java_sim = unittest.TestLoader().loadTestsFromTestCase(conf_java.TestJavaSim)

    # Run Octave test
    suite_octave_sim = unittest.TestLoader().loadTestsFromTestCase(conf_octave.TestOctaveSim)

    # combine all the test suites
    suite = unittest.TestSuite([suite_ok_sim,
                                suite_ok_ps1,
                                suite_ok_ps2,
                                suite_ok_pe,
                                suite_ok_sens,
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
                                suite_octave_sim])

    # run the combined test suite
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    run_tests_suites()
