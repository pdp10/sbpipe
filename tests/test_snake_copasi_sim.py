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


import sys
import os
import unittest
import subprocess
from context import sbpipe, SBPIPE
from sbpipe.utils.dependencies import is_py_package_installed


class TestSimSnake(unittest.TestCase):

    _orig_wd = os.getcwd()
    _ir_folder = os.path.join('snakemake')
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._ir_folder))
        try:
            subprocess.Popen(['CopasiSE'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()[0]
        except OSError as e:
            cls._output = 'CopasiSE not found: SKIP ... '
            return
        if not is_py_package_installed('sbpipe'):
            cls._output = 'sbpipe not installed: SKIP ... '
        if not is_py_package_installed('snakemake'):
            cls._output = 'snakemake not installed: SKIP ... '
        if not os.path.exists('sbpipe_sim.snake'):
            cls._output = 'snakemake workflow not found: SKIP ... '

    @classmethod
    def tearDownClass(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sim_det_snake(self):
        if self._output == 'OK':
            from snakemake import snakemake
            self.assertTrue(
                snakemake(snakefile='sbpipe_sim.snake',
                          configfile='ir_model_det_simul.yaml',
                          cores=7,
                          forceall=True,
                          quiet=True))
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_sim_stoch_snake(self):
        if self._output == 'OK':
            from snakemake import snakemake
            self.assertTrue(
                snakemake(snakefile='sbpipe_sim.snake',
                          configfile='ir_model_stoch_simul.yaml',
                          cores=7,
                          forceall=True,
                          quiet=True))
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
