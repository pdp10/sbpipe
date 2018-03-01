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
# Object: run a list of tests for the insulin receptor model.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2017-01-31 14:36:32 $

import sys
import os
import unittest
import subprocess

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))


class TestPs2Snake(unittest.TestCase):

    _orig_wd = os.getcwd()
    _snakemake = os.path.join('snakemake')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._snakemake))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_ps2_det_snake(self):
        try:
            subprocess.Popen(['snakemake', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            from snakemake import snakemake
            self.assertTrue(
                snakemake(os.path.join(SBPIPE, 'sbpipe_ps2.snake'), configfile='ir_model_insulin_ir_beta_dbl_inhib.yaml', cores=7, forceall=True, quiet=True))
        except OSError as e:
            sys.stdout.write("snakemake not found: SKIP ... ")
            sys.stdout.flush()

    def test_ps2_stoch_snake(self):
        try:
            subprocess.Popen(['snakemake', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            from snakemake import snakemake
            self.assertTrue(
                snakemake(os.path.join(SBPIPE, 'sbpipe_ps2.snake'), configfile='ir_model_insulin_ir_beta_dbl_stoch_inhib.yaml', cores=7, forceall=True, quiet=True))
        except OSError as e:
            sys.stdout.write("snakemake not found: SKIP ... ")
            sys.stdout.flush()

if __name__ == '__main__':
    unittest.main(verbosity=2)
