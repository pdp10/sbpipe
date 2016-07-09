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
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-05-30 16:14:32 $





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


"""
This module provides the user with a complete pipeline of scripts for computing 
model sensitivity analysis using Copasi
"""

def main(model_configuration):
  """
  Execute and collect results for model sensitivity using Copasi
  Keyword arguments:
      model_configuration -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """

  print("\nReading file " + model_configuration + " : \n")
  # import the model configuration data (project, model-name, association-pattern)
  parser = ConfigParser()
  with open(model_configuration) as stream:
    stream = StringIO("[top]\n" + stream.read())  # This line does the trick.
    parser.readfp(stream)  
    
  lines=parser.items('top')
   
   
  # The project directory
  project_dir=".."
  # The copasi model
  model="mymodel.cps"
  # The path to Copasi reports
  copasi_reports_path="tmp"  


  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "project_dir":
      project_dir = line[1] 
    elif line[0] == "model": 
      model = line[1] 
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]
      
  
  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The working folder containing the results
  working_folder="Working_Folder"  
  # The folder containing the sensitivity analysis results
  sensitivities_dir="sensitivities"
  
  models_dir=project_dir+"/"+models_folder+"/"
  results_dir=project_dir+"/"+working_folder+"/"+model[:-4]+"/"+sensitivities_dir+"/"
  tmp_dir=copasi_reports_path+"/"


  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()

      

  print("\n")
  print("#############################################################")     
  print("#############################################################")
  print("### Processing model "+ model)
  print("#############################################################")
  print("#############################################################")
  print("")



  print("\n")
  print("##############################")
  print("Preparing folder "+results_dir)
  print("##############################")
  print("\n")
  # remove the folder the previous results if any
#   filesToDelete = glob.glob(sensitivities_dir+"/*.png")
#   for f in filesToDelete:
#     os.remove(f)  

  if not os.path.exists(results_dir):
    os.mkdir(results_dir)



  # print("\n")
  # print("#####################")
  # print("Executing sensitivities:\n")
  # print("#####################")
  # print("\n")
  # TODO 
  #process = subprocess.Popen(['bash', SB_PIPE+"/sb_pipe/pipelines/sb_sensitivity/sensitivities__run_copasi.sh", model, models_dir, results_dir, tmp_dir])
  #process.wait()   



  print("\n")
  print("##################")
  print("Generating plots:")
  print("##################")
  print("\n")
  process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_sensitivity/sensitivities__copasi_plot.R", results_dir])
  process.wait()    




  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n")


  if len(glob.glob(results_dir+"/"+"*.csv")) > 0:
      return 0
  return 1
    
    