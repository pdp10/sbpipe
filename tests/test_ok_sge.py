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
# Object: run a list of tests for the insulin receptor model using SGE (Sun Grid Engine) 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $

import os
import subprocess
import sys

SBPIPE = os.environ["SBPIPE"]
sys.path.append(SBPIPE)
from sbpipe import main as sbmain
import unittest


class TestCopasiSGE(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _ir_folder = os.path.join('insulin_receptor')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._ir_folder))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_stoch_sim_copasi_sge(self):
        try:
            subprocess.Popen(['qstat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(sbmain.sbpipe(simulate="sge_ir_model_stoch_simul.yaml"), 0)
        except OSError as e:
            print("Skipping test as no SGE (Sun Grid Engine) was found.")

    def test_pe_copasi_sge(self):
        try:
            subprocess.Popen(['qstat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(sbmain.sbpipe(param_estim="sge_ir_model_param_estim.yaml"), 0)
        except OSError as e:
            print("Skipping test as no SGE (Sun Grid Engine) was found.")

    def test_stoch_pe_copasi_sge(self):
        try:
            subprocess.Popen(['qstat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            self.assertEqual(sbmain.sbpipe(param_estim="sge_ir_model_stoch_param_estim.yaml"), 0)
        except OSError as e:
            print("Skipping test as no SGE (Sun Grid Engine) was found.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
