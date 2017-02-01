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

SBPIPE = os.environ["SBPIPE"]
sys.path.append(SBPIPE)
from sbpipe import main as sbmain
import unittest
from sbpipe.sb_config import isPyPackageInstalled

"""Unit test for Python simulator"""


class TestPythonSim(unittest.TestCase):
    """
    A collection of tests for this example.
    """

    _orig_wd = os.getcwd()  # remember our original working directory
    _python = os.path.join('python_models')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._python))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_python_insulin_receptor_simulation(self):
        """Insulin receptor model in python - simulation"""
        if not isPyPackageInstalled("numpy"):
            print("Skipping test as Python numpy was not found.")
        elif not isPyPackageInstalled("scipy"):
            print("Skipping test as Python scipy was not found.")
        elif not isPyPackageInstalled("pandas"):
            print("Skipping test as Python pandas was not found.")
        else:
            self.assertEqual(sbmain.main(["sbpipe", "--simulate", "insulin_receptor.conf"]), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
