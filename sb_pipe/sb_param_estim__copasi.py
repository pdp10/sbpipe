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
# $Date: 2016-06-23 19:14:32 $





# for computing the pipeline elapsed time 
import time

import os
import sys
import glob
import shutil
import subprocess
import tarfile
# for generating a timestamp
import datetime

from ConfigParser import ConfigParser
from StringIO import StringIO

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + "/sb_pipe/pipelines/sb_param_estim__copasi/")
import param_estim__copasi_parallel
import param_estim__copasi_utils_randomise_start_values
import param_estim__copasi_utils_collect_results
import param_estim__copasi_utils_plot_calibration
import param_estim__gen_report


"""
This module provides the user with a complete pipeline of scripts comprising the configuration 
and execution of jobs on the cluster, results retrieval and concatenation, parameter estimation 
analyses and finally results storing. This pipeline uses CopasiSE
"""
def main(model_configuration):
  """
  Execute and collect results from parameter estimation using Copasi
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

  # The project dir
  project_dir=""
  # read the copasi model name 
  model="mymodel.cps"
  # The path to Copasi reports
  copasi_reports_path="tmp"  
  # The parallel mechanism to use (pp | sge | lsf).
  cluster="pp"
  # The number of cpus for pp
  pp_cpus=1
  # The parameter estimation round 
  round=1
  # The number of jobs to be executed
  nfits=25
  # The percent of best fits to consider
  best_fits_percent=100



  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "project_dir": 
      project_dir = line[1]
    elif line[0] == "model":
      model = line[1]     
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]
    elif line[0] == "cluster":
      cluster = line[1]      
    elif line[0] == "round":
      round = line[1]       
    elif line[0] == "nfits":
      nfits = line[1] 
    elif line[0] == "pp_cpus": 
      pp_cpus = line[1]
    elif line[0] == "best_fits_percent": 
      best_fits_percent = line[1]
      

  nfits = int(nfits)

  # INTERNAL VARIABLES
  # The folder containing the models
  models_folder="Models"
  # The folder containing the data
  data_folder="Data"
  # The folder containing the working results
  working_folder="Working_Folder"
  # The dataset working folder
  dataset_working_folder="param_estim_data"  
  
  models_dir=project_dir+"/"+models_folder+"/"
  working_dir=project_dir+"/"+working_folder+"/"
  data_dir=project_dir+"/"+data_folder+"/"
  tmp_dir=copasi_reports_path+"/"

  output_folder=model[:-4]+"_round"+round
  plots_folder="plots"
  results_dir=working_dir+"/"+output_folder
  plots_dir=results_dir+"/"+plots_folder
  data_summary_file="parameter_estimation_collected_results.csv"



  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()

    
    
  print("\n")
  print("#############################################################")
  print("#############################################################")
  print("### Parameter estimation for model "+model)
  print("#############################################################")
  print("#############################################################")
  print("")


      
  print("\n")
  print("#################")
  print("Preparing folders:")
  print("#################")
  print("\n")
  shutil.rmtree(output_folder, ignore_errors=True)   
  if not os.path.exists(models_dir):
    os.mkdir(models_dir)
  if not os.path.exists(data_dir):
    os.mkdir(data_dir)
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
  if not os.path.exists(working_dir):
    os.makedirs(working_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir)
  if not os.path.exists(results_dir+"/"+dataset_working_folder):
    os.mkdir(results_dir+"/"+dataset_working_folder) 



  print("\n")
  print("################")
  print("Configure Copasi:")
  print("################")
  param_estim__copasi_utils_randomise_start_values.main(models_dir, model, nfits)




  print("\n")
  print("###############################")
  print("Concurrent parameter estimation:")
  print("###############################")
  # for some reason, CopasiSE ignores the "../" for the data file and assumes that the Data folder is inside the Models folder..
  # Let's temporarily copy this folder and then delete it.
  if os.path.exists(models_dir+"/"+data_folder):
    os.rename(models_dir+"/"+data_folder, models_dir+"/"+data_folder+"_{:%Y%m%d%H%M%S}".format(datetime.datetime.now()))
  shutil.copytree(data_dir, models_dir+"/"+data_folder)

  
  if cluster == "sge" or cluster == "lsf":
    # Test this with echo "Copasi insulin_receptor.cps" | xargs xargs using Python environment.
    # The following works:
    # copasiCMD = "CopasiSE insulin_receptor.cps"      
    # echoCMD=["echo", copasiCMD]      
    # xargsCMD=["xargs", "xargs"]
    # echoProc = subprocess.Popen(echoCMD, stdout=subprocess.PIPE)
    # xargsProc = subprocess.Popen(xargsCMD, stdin=echoProc.stdout)
    jobs = ""
    echoSleep = ["echo", "sleep 1"]
    outDir=results_dir+"/out"
    errDir=results_dir+"/err"
    if not os.path.exists(outDir):
      os.makedirs(outDir)
    if not os.path.exists(errDir):
      os.makedirs(errDir)   
      
    if cluster == "sge":  # use SGE (Sun Grid Engine) 
      for i in xrange(0,nfits):
	  # Now the same with qsub
	  jobs = "j"+str(i)+","+jobs
	  copasiCMD = "CopasiSE -s "+models_dir+"/"+model[:-4]+str(i)+".cps "+models_dir+"/"+model[:-4]+str(i)+".cps"	  
	  echoCMD = ["echo", copasiCMD]
	  qsubCMD = ["qsub", "-cwd", "-N", "j"+str(i), "-o", outDir+"/j"+str(i), "-e", errDir+"/j"+str(i)] 
	  echoProc = subprocess.Popen(echoCMD, stdout=subprocess.PIPE)
	  qsubProc = subprocess.Popen(qsubCMD, stdin=echoProc.stdout, stdout=subprocess.PIPE)
      # Check here when these jobs are finished before proceeding
      qsubCMD = ["qsub", "-hold_jid", jobs[:-1]]
      echoProc = subprocess.Popen(echoSleep, stdout=subprocess.PIPE)
      qsubProc = subprocess.Popen(qsubCMD, stdin=echoProc.stdout, stdout=subprocess.PIPE)
      qsubProc.wait()

    elif cluster == "lsf": # use LSF (Platform Load Sharing Facility)
      for i in xrange(1,nfits):
	  jobs = "done(CopasiSE_"+model[:-4]+str(i)+")&&"+jobs
	  copasiCMD = "CopasiSE -s "+models_dir+"/"+model[:-4]+str(i)+".cps "+models_dir+"/"+model[:-4]+str(i)+".cps"
	  echoCMD = ["echo", copasiCMD]
	  bsubCMD = ["bsub", "-cwd", "-J", "j"+str(i), "-o", outDir+"/j"+str(i), "-e", errDir+"/j"+str(i)] 
	  echoProc = subprocess.Popen(echoCMD, stdout=subprocess.PIPE)
	  bsubProc = subprocess.Popen(bsubCMD, stdin=echoProc.stdout, stdout=subprocess.PIPE)
      # Check here when these jobs are finished before proceeding
      qsubCMD = ["bsub", "-w", jobs[:-2]]
      echoProc = subprocess.Popen(echoSleep, stdout=subprocess.PIPE)
      bsubProc = subprocess.Popen(bsubCMD, stdin=echoProc.stdout, stdout=subprocess.PIPE)
      bsubProc.wait()    
    
    
  else: # use pp by default (parallel python). This is configured to work locally using multi-core.
    if cluster != "pp":
      print("Warning - Variable cluster is not set correctly in the configuration file. Values are: pp, lsf, sge. Running pp by default")
    
    # Settings for PP
    # The user name
    user="sb_pipe"
    # The server to connect (e.g. localhost,my-node.abc.ac.uk)
    server_list="localhost"
    # The port to connect for the above server (e.g. 65000)
    port_list="65000"
    # The secret key to communicate for the above server
    secret="donald_duck"  
    pp_cpus = int(pp_cpus)    

    # Perform this task using python-pp (parallel python dependency). 
    # If this computation is performed on a cluster, start this on each node of the cluster. 
    # The list of servers and ports must be updated in the configuration file
    # (NOTE: It requires the installation of python-pp)
    #ppserver -p 65000 -i my-node.abc.ac.uk -s "donald_duck" -w 5 &

    # Perform this task using python-pp (parallel python dependency)
    param_estim__copasi_parallel.main(server_list, port_list, secret, models_dir, model[:-4], nfits, pp_cpus)


  # remove the previously copied Data folder
  shutil.rmtree(models_dir+"/"+data_folder, ignore_errors=True) 

  # Move the files to the results_dir
  tmpFiles = os.listdir(tmp_dir)
  for file in tmpFiles:
    shutil.move(tmp_dir+"/"+file, results_dir+"/"+dataset_working_folder+"/")
    
    


  print("\n")
  print("###############")
  print("Collect results:")
  print("###############")
  print("\n")
  # Collect and summarises the parameter estimation results
  param_estim__copasi_utils_collect_results.main(results_dir+"/"+dataset_working_folder+"/", results_dir, data_summary_file)

  # plot the fitting curve using data from the fit sequence 
  # This requires extraction of a couple of fields from the Copasi output file for parameter estimation.
  #param_estim__copasi_utils_plot_calibration.main(results_dir, results_dir)


  print("\n")
  print("###################")
  print("Plot distributions:")
  print("###################")
  print("\n")
  process = subprocess.Popen(['Rscript', SB_PIPE+"/sb_pipe/pipelines/sb_param_estim__copasi/param_estim__copasi_fit_analysis.r", results_dir+"/"+data_summary_file, plots_dir, best_fits_percent])
  process.wait()
  

  print("\n")
  print("##################")
  print("Generating reports:")
  print("##################")
  print("\n")
  param_estim__gen_report.main(model[:-4], results_dir+"/", plots_folder)


  print("\n")
  print("#####################################")
  print("Store the fits sequences in a tarball:")
  print("#####################################")
  print("\n")
  # Create a gz tarball   
  origWD = os.getcwd() # remember our original working directory
  os.chdir(working_dir) # change folder
  with tarfile.open(output_folder+".tgz", "w:gz") as tar:
    tar.add(output_folder, arcname=os.path.basename(output_folder))
  os.chdir(origWD) # get back to our original working directory
    


  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n")


  if os.path.isfile(results_dir+"/parameter_estimation_collected_results.csv") and len(glob.glob(results_dir+"/*"+model[:-4]+"*.pdf")) == 1:
      return True
  return False
    
    
