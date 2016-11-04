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
sys.path.append(os.path.join(SBPIPE, 'scripts'))
import run_sbpipe
import unittest

"""Unit test for Insulin Receptor"""


class TestIRSimulate(unittest.TestCase):
    """
    A collection of tests for this example.
    """

    def test_det_simulation(self):
        """model deterministic simulation"""
        self.assertEqual(run_sbpipe.main(["run_sbpipe", "--simulate", "ir_model_det_simul.conf"]), 0)

    def test_stoch_simulation(self):
        """model stochastic simulation"""
        self.assertEqual(run_sbpipe.main(["run_sbpipe", "--simulate", "ir_model_stoch_simul.conf"]), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
