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
# Object: run a list of tests for octave models.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $

import os
import sys

SBPIPE = os.environ["SBPIPE"]
sys.path.append(os.path.join(SBPIPE, 'scripts'))
import run_sbpipe
import unittest
import subprocess

"""Unit test for Octave simulator"""


class TestOctaveSim(unittest.TestCase):
    """
    A collection of tests for this example.
    """

    _orig_wd = os.getcwd()  # remember our original working directory
    _octave = os.path.join('octave_models', 'Working_Folder')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._octave))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_octave_model_simulation(self):
        """A non linear octave model - simulation"""
        try:
            subprocess.Popen(['octave', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(run_sbpipe.main(["sbpipe", "--simulate", "nonlinear_octave_model_sim.conf"]), 0)
        except OSError as e:
            print("Skipping test as Octave was not found.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
