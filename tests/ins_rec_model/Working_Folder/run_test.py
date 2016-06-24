#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: run a list of tests.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $


import os
import sys
import subprocess
from distutils.dir_util import copy_tree

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + '/bin/')
#import sb_simulate


def main(args):

  # model parameter estimation    
  process = subprocess.Popen(['python', SB_PIPE + '/bin/sb_param_estim__copasi.py', 'model_ins_rec_v1_param_estim_copasi.conf', '1'])
  process.wait() 

  # model simulation (simple)
  process = subprocess.Popen(['python', SB_PIPE + '/bin/sb_simulate.py', 'model_ins_rec_v1_det_simul.conf'])
  process.wait()
  
  process = subprocess.Popen(['python', SB_PIPE + '/bin/sb_simulate.py', 'model_ins_rec_v1_stoch_simul.conf'])
  process.wait()
  
  # model simulation (perturbation)  
  process = subprocess.Popen(['python', SB_PIPE + '/bin/sb_param_scan__single_perturb.py', 'model_ins_rec_v1_single_perturbations_inhibitions.conf'])
  process.wait() 



  # TODO TO CONVERT TO Python
  # model sensitivities    
  #print "The script sb_sensitivity.sh does not run Copasi, but generates a plot for each file containing a square matrix in PROJECT/simulation/MODEL/SENSITIVITIES_FOLDER (here: ins_rec_model/simulation/insulin_receptor/sensitivities/)"
  #print "Let's copy some files containing sensitivity matrices into the folder SENSITIVITIES_FOLDER (here: sensitivities)"
  #copy_tree("../Data/sb_sensitivity_for_testing", "../simulations/insulin_receptor/sensitivities")

  #process = subprocess.Popen(['sb_sensitivity.sh', 'model_ins_rec_v1_sensitivities.conf'])
  #process.wait() 


main(sys.argv)