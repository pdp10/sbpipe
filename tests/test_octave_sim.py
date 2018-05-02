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
import subprocess
from context import sbpipe, SBPIPE


class TestOctaveSim(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _octave_folder = os.path.join('octave_models')
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._octave_folder))
        try:
            subprocess.Popen(['octave', '-v'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()[0]
        except OSError as e:
            cls._output = 'Octave not found: SKIP ... '

    @classmethod
    def tearDownClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_octave_model_simulation(self):
        if self._output == 'OK':
            self.assertEqual(sbpipe(simulate="nonlinear_octave_model_sim.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
