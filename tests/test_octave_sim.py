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

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(SBPIPE)
import sbpipe.main as sbmain
import unittest
import subprocess


class TestOctaveSim(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _octave = os.path.join('octave_models')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._octave))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_octave_model_simulation(self):
        try:
            subprocess.Popen(['octave', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(sbmain.sbpipe(simulate="nonlinear_octave_model_sim.yaml", quiet=True), 0)
        except OSError as e:
            print("Skipping test as Octave was not found.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
