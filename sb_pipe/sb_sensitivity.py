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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-05-30 16:14:32 $

# This scripts provides the user with a complete pipeline of scripts for computing 
# model sensitivity analysis using Copasi



# for computing the pipeline elapsed time 
import time

import os
import sys
import glob
import shutil
import subprocess

from ConfigParser import ConfigParser
from StringIO import StringIO

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + "/sb_pipe/pipelines/sb_sensitivity/")




# The file containing the model configuration, usually in working_folder (e.g. model.conf)
def main(model_configuration):


  print("\nReading file " + model_configuration + " : \n")
  # import the model configuration data (project, model-name, association-pattern)
  parser = ConfigParser()
  with open(model_configuration) as stream:
    stream = StringIO("[top]\n" + stream.read())  # This line does the trick.
    parser.readfp(stream)  
    
  lines=parser.items('top')
   
   
  # The project name (e.g. "p3__mtor_foxo_ros")
  project=""
  # read the main model name (e.g. mtor_mito_ros_model_v27_pw3.m)
  model=""
  # Sensitivity copasi model file (e.g mtor_mito_ros_model_v27_copasi_sens.cps ...)
  sensitivities__copasi_model=""
  # The folder containing the sensitivity analysis results
  sensitivities_dir=""
  # The folder containing the models (e.g. Models)
  models_folder=""
  # The folder containing the models simulations (e.g. simulations)
  simulations_folder=""



  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "project":
      project = line[1] 
    elif line[0] == "model":
      model = line[1] 
    elif line[0] == "sensitivities__copasi_model": 
      sensitivities__copasi_model = line[1] 
    elif line[0] == "sensitivities_dir": 
      sensitivities_dir = line[1]
    elif line[0] == "models_folder": 
      models_folder = line[1] 
    elif line[0] == "simulations_folder": 
      simulations_folder = line[1] 

      
  models_dir=project+"/"+models_folder+"/"
  sensitivities_path=project+"/"+simulations_folder+"/"+model+"/"+sensitivities_dir+"/"



  print("\n\n\n<START PIPELINE>\n\n\n")
  # Get the pipeline start time
  start = time.clock()

      

  print("\n\n\n")
  print("##############################################################\n")     
  print("##############################################################\n")
  print("### Processing model "+ sensitivities__copasi_model+"\n")
  print("##############################################################\n")
  print("##############################################################\n")
  print("\n\n")



  print("\n\n\n")
  print("###############################\n")
  print("Preparing folder "+sensitivities_path +":\n")
  print("###############################\n")
  print("\n")
  # remove the folder the previous results if any
#   filesToDelete = glob.glob(sensitivities_dir+"/*.png")
#   for f in filesToDelete:
#     os.remove(f)  

  if not os.path.exists(sensitivities_path):
    os.mkdir(sensitivities_path)



  # print("\n\n\n")
  # print("######################\n")
  # print("Executing sensitivities:\n")
  # print("######################\n")
  # print("\n")
  # TODO 
  #process = subprocess.Popen(['bash', SB_PIPE+"/sb_pipe/pipelines/sb_sensitivity/sensitivities__run_copasi.sh", sp_model, models_dir, results_dir, tmp_dir])
  #process.wait()   



  print("\n\n\n")
  print("###################\n")
  print("Generating plots:\n")
  print("###################\n")
  print("\n")
  process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_sensitivity/sensitivities__copasi_plot.R", sensitivities_path])
  process.wait()    




  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n\n\n")

