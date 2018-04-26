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
# Object: run a list of tests for the insulin receptor model.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $

import os
import sys

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(SBPIPE)
import sbpipe.main as sbmain
import unittest
from sbpipe.sbpipe_config import isPyPackageInstalled


class TestPythonSim(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _python_folder = os.path.join('python_models')
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._python_folder))
        if not isPyPackageInstalled("numpy"):
            cls._output = "Python numpy not found: SKIP ... "
        elif not isPyPackageInstalled("scipy"):
            cls._output = "Python scipy not found: SKIP ... "
        elif not isPyPackageInstalled("pandas"):
            cls._output = "Python pandas not found: SKIP ... "

    @classmethod
    def tearDownClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sim_python_ir(self):
        if self._output == 'OK':
            self.assertEqual(sbmain.sbpipe(simulate="insulin_receptor.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

if __name__ == '__main__':
    unittest.main(verbosity=2)
