#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: run a list of tests for the insulin receptor model using SGE (Sun Grid Engine) 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $


import os
import sys
import subprocess
from distutils.dir_util import copy_tree

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + '/sb_pipe/')

import run_sb_pipe

import unittest


"""Unit test for Insulin Receptor"""

class TestInsulinReceptorSGE(unittest.TestCase):
  """
  A collection of tests for this example using SGE
  """

  def test_param_estim_copasi_sge(self):        
    """model parameter estimation using SGE if found"""
    try:
	subprocess.call(["qstat"])
	self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "param_estim", "sge_insulin_receptor_param_estim_copasi.conf"]))	
    except OSError as e:
	print("Skipping test as no SGE (Sun Grid Engine) was found.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
    
    