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

import tests.test_snake_copasi_pe as snake_copasi_pe
import tests.test_snake_copasi_sim as snake_copasi_sim
import tests.test_snake_copasi_ps1 as snake_copasi_ps1
import tests.test_snake_copasi_ps2 as snake_copasi_ps2


class TestSuite(unittest.TestCase):

    def test_suites(self):

        # Run Snakemake tests
        suite_snake_copasi_pe = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_pe.TestPeSnake)
        suite_snake_copasi_sim = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_sim.TestSimSnake)
        suite_snake_copasi_ps1 = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_ps1.TestPs1Snake)
        suite_snake_copasi_ps2 = unittest.TestLoader().loadTestsFromTestCase(snake_copasi_ps2.TestPs2Snake)

        # combine all the test suites
        suite = unittest.TestSuite([suite_snake_copasi_pe,
                                    suite_snake_copasi_sim,
                                    suite_snake_copasi_ps1,
                                    suite_snake_copasi_ps2])

        # run the combined test suite
        self.assertTrue(unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())


if __name__ == "__main__":
    unittest.main(verbosity=2)
