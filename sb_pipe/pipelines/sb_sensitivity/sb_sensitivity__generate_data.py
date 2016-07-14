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
# Object: Execute the model several times for deterministic or stochastical analysis
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 13:45:32 $




import os
import sys
import glob
from subprocess import Popen,PIPE

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))



# Input parameters
# model, models_dir, output_dir, tmp_dir
def main(model, models_dir, output_dir, tmp_dir):

  if not os.path.isfile(os.path.join(models_dir,model)):
    print(os.path.join(models_dir, model) + " does not exist.") 
    return  

  # folder preparation
  filesToDelete = glob.glob(os.path.join(output_dir, model[:-4]+"*"))
  for f in filesToDelete:
    os.remove(f)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # execute runs simulations.
  print("Sensitivity analysis for " + model)
  
  # run copasi
  copasi = getCopasi()  
  command = [copasi, os.path.join(models_dir, model[:-4]+".cps")]

  p = Popen(command)
  p.wait()
 
  # move the output file
  move(os.path.join(tmp_dir, model[:-4]+".csv"), output_dir)

    
