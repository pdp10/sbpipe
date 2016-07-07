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
# Object: run a list of tests for the insulin receptor model.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $


import os
import sys
from distutils.dir_util import copy_tree

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + '/sb_pipe/')

import run_sb_pipe

import unittest


"""Unit test for Insulin Receptor"""

class TestInsulinReceptor(unittest.TestCase):
  """
  A collection of tests for this example.
  """
  
  def test_det_simulation(self):
    """model deterministic simulation"""
    self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "simulate", "insulin_receptor_det_simul_copasi.conf"]))

  def test_stoch_simulation(self):    
    """model stochastic simulation"""    
    self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "simulate", "insulin_receptor_stoch_simul_copasi.conf"])) 



  def test_param_scan_single_perturb_inhib(self):    
    """model single perturbation"""
    self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "single_perturb", "insulin_receptor_ir_beta_inhib_copasi.conf"])) 

  def test_param_scan_single_perturb_inhib_overexp(self):    
    """model single perturbation"""
    self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "single_perturb", "insulin_receptor_ir_beta_inhib_overexp_copasi.conf"])) 



  def test_param_estim_copasi(self):        
    """model parameter estimation"""
    self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "param_estim", "insulin_receptor_param_estim_copasi.conf"]))    
    
  def test_non_identif_param_estim_copasi(self):        
    """model parameter estimation with identifiability issues """
    self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "param_estim", "insulin_receptor_non_identif_param_estim_copasi.conf"]))    


  # TODO TO TEST
  #print "The script sb_sensitivity.py does not run Copasi, but generates a plot for each file containing a square matrix in PROJECT/simulation/MODEL/SENSITIVITIES_FOLDER (here: ins_rec_model/simulation/insulin_receptor/sensitivities/)"
  #print "Let's copy some files containing sensitivity matrices into the folder SENSITIVITIES_FOLDER (here: sensitivities)"
  #copy_tree("../Data/sb_sensitivity_for_testing", "../simulations/insulin_receptor/sensitivities")

  #def test_model_sensitivity(self):
  #  """model sensitivities"""
  #  self.assertTrue(run_sb_pipe.main(["run_sb_pipe", "sensitivity", "insulin_receptor_sensitivities_copasi.conf"]))



if __name__ == '__main__':
    unittest.main(verbosity=2)
    
    