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
from subprocess import Popen,PIPE

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + "/sb_pipe/utils/python/")
from CopasiUtils import replace_str_copasi_sim_report



# Input parameters
# model: read the model
# models_dir: read the models dir
# output_dir: The output dir
# tmp_dir: read the temp dir
# simulate__model_simulations_number : minimum 2 (required for plotCI, otherwise, ci95 and sderr are NA -> error in ylim)
def main(model, models_dir, output_dir, tmp_dir, simulate__model_simulations_number):
  
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

