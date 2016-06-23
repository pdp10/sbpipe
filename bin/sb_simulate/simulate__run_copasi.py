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
# Object: Execute the model several times for stochastical analysis
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 13:45:32 $




import os
import sys
from subprocess import Popen,PIPE

SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")
from CopasiUtils import replace_str_copasi_sim_report




def main(args):
  
  # Input parameters
  # read the model
  model=args[1]
  # read the models dir
  models_dir=args[2]
  # The output dir
  output_dir=args[3]
  # read the temp dir
  tmp_dir=args[4]
  # minimum 2 (required for plotCI, otherwise, ci95 and sderr are NA -> error in ylim)
  simulate__model_simulations_number=args[5]



  if int(simulate__model_simulations_number) < 2: 
    print("ERROR: variable " + simulate__model_simulations_number + " must be >= 2");
    return
   
  model_noext=model[:-4]
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)


  print("Simulating Model: " + model)
  # execute simulate__model_simulations_number simulations. For the plot generation we need more than 1 simulation. 
  # This is likely to be a bug. For now, let's do at least two simulations.
  for idx in range(1, int(simulate__model_simulations_number) + 1):
    # run CopasiSE. Copasi must generate a (TIME COURSE) report called model_noext +'.csv' in tmp_dir
    p1 = Popen(["CopasiSE", "--nologo", models_dir+'/'+model], stdout=PIPE) 
    p1.communicate()[0]

    # Replace some string in the report file
    print("Simulation No.: " + str(idx))
    replace_str_copasi_sim_report(tmp_dir, model)
    os.rename(tmp_dir+"/"+model_noext+".csv", output_dir+"/"+model_noext+"__sim_"+str(idx)+".csv")

    
main(sys.argv)
