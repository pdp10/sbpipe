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


import unittest
import tests.test_copasi_lsf as copasi_lsf
import tests.test_copasi_sge as copasi_sge


class TestSuite(unittest.TestCase):

    def test_suites(self):

        # Run negative test suites
        suite_copasi_lsf = unittest.TestLoader().loadTestsFromTestCase(copasi_lsf.TestCopasiLSF)
        suite_copasi_sge = unittest.TestLoader().loadTestsFromTestCase(copasi_sge.TestCopasiSGE)

        # combine all the test suites
        suite = unittest.TestSuite([suite_copasi_lsf, suite_copasi_sge])

        # run the combined test suite
        self.assertTrue(unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())


if __name__ == "__main__":
    unittest.main(verbosity=2)
