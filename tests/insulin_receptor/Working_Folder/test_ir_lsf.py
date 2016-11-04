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
# Object: run a list of tests for the insulin receptor model using LSF (Platform Load Sharing Facility)
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $

import os
import subprocess
import sys
SBPIPE = os.environ["SBPIPE"]
sys.path.append(os.path.join(SBPIPE, 'scripts'))
import run_sbpipe
import unittest

"""Unit test for Insulin Receptor"""


class TestIRLSF(unittest.TestCase):
    """
    A collection of tests for this example using LSF
    """

    def test_stoch_simul_copasi_lsf(self):
        """model simulation using LSF if found"""
        try:
            subprocess.call(["qstat"])
            self.assertEqual(run_sbpipe.main(["run_sbpipe", "--simulate", "lsf_ir_model_stoch_simul.conf"]), 0)
        except OSError as e:
            print("Skipping test as no LSF (Load Sharing Facility) was found.")

    def test_param_estim_copasi_lsf(self):
        """model parameter estimation using LSF if found"""
        try:
            subprocess.call(["bjobs"])
            self.assertEqual(run_sbpipe.main(["run_sbpipe", "--param-estim", "lsf_ir_model_param_estim.conf"]), 0)
        except OSError as e:
            print("Skipping test as no LSF (Load Sharing Facility) was found.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
