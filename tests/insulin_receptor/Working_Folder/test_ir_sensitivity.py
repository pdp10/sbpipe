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


class TestIRSensitivity(unittest.TestCase):
    """
    A collection of tests for this example.
    """
    # TODO TO TEST
    # print "The script sb_sensitivity.py does not run Copasi, but generates a plot for
    # each file containing a square matrix in PROJECT/simulation/MODEL/SENSITIVITIES_FOLDER (here: ins_rec_model/simulation/insulin_receptor/sensitivities/)"
    # print "Let's copy some files containing sensitivity matrices into the folder
    # SENSITIVITIES_FOLDER (here: sensitivities)"
    # copy_tree("../Data/sb_sensitivity_for_testing", "../simulations/insulin_receptor/sensitivities")

    # def test_model_sensitivity(self):
    #  """model sensitivities"""
    #  self.assertEqual(run_sbpipe.main(["run_sbpipe", "--sensitivity", "ir_model_sensitivities.conf"]), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
