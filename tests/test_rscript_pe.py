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


import os
import sys
import unittest
from context import sbpipe, SBPIPE
from sbpipe.utils.dependencies import is_r_package_installed


class TestRPE(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _rscript_folder = os.path.join('r_models')
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._rscript_folder))
        if not is_r_package_installed("reshape2"):
            cls._output = "R reshape2 not found: SKIP ... "
        elif not is_r_package_installed("deSolve"):
            cls._output = "R deSolve not found: SKIP ... "
        elif not is_r_package_installed("minpack.lm"):
            cls._output = "R minpack.lm not found: SKIP ... "

    @classmethod
    def tearDownClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

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
