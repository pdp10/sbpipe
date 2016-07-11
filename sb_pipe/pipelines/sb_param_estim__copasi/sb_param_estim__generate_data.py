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
import shutil
from subprocess import Popen,PIPE
# for generating a timestamp
import datetime

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
import sb_param_estim__copasi_utils_randomise_start_values
import sb_param_estim__copasi_parallel

# TODO: IT REQUIRES THE FULL PATH FOR COPASI. IT WOULD BE BETTER
# IF THE COPASI COMMAND WERE READ FROM A SB_CONFIGURATION_FILE.
# MAYBE __init__.py could be used for this purpose

def runCopasiSGE(models_dir, model, outDir, errDir, nfits):
  jobs = ""
  echoSleep = ["echo", "sleep 1"]  
  for i in xrange(0,nfits):
      # Now the same with qsub
      jobs = "j"+str(i)+","+jobs
      copasiCMD = "/bi/home/dallepep/copasi/bin/CopasiSE -s "+os.path.join(models_dir, model+str(i)+".cps")+" "+os.path.join(models_dir, model+str(i)+".cps")
      echoCMD = ["echo", copasiCMD]
      qsubCMD = ["qsub", "-cwd", "-N", "j"+str(i), "-o", os.path.join(outDir, "j"+str(i)), "-e", os.path.join(errDir,"j"+str(i))] 
      echoProc = Popen(echoCMD, stdout=PIPE)
      qsubProc = Popen(qsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  # Check here when these jobs are finished before proceeding
  qsubCMD = ["qsub", "-sync", "y", "-hold_jid", jobs[:-1]]
  echoProc = Popen(echoSleep, stdout=PIPE)
  qsubProc = Popen(qsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  qsubProc.communicate()[0]


def runCopasiLSF(models_dir, model, outDir, errDir, nfits):
  print("WARNING - runCopasiLSF() is untested. Some problem can occur.\n"\
    "The function should compute the estimations but the following analysis may be compromised.\n"\
    "In particular, the function might complete before the estimations are finished.\n"\
    "Possibly retrieve the estimations and compute the analysis from your machine instead of from here.\n"\
    "Sorry for the inconvenient. We are working on it. To report additional bugs: https://github.com/pdp10/sb_pipe/issues .")
  jobs = ""
  echoSleep = ["echo", "sleep 1"]  
  for i in xrange(1,nfits):
      jobs = "done(CopasiSE_"+model[:-4]+str(i)+")&&"+jobs
      copasiCMD = "/bi/home/dallepep/copasi/bin/CopasiSE -s "+os.path.join(models_dir, model+str(i)+".cps")+""+os.path.join(models_dir, model+str(i)+".cps")
      echoCMD = ["echo", copasiCMD]
      bsubCMD = ["bsub", "-cwd", "-J", "j"+str(i), "-o", os.path.join(outDir, "j"+str(i)), "-e", os.path.join(errDir, "j"+str(i))] 
      echoProc = Popen(echoCMD, stdout=PIPE)
      bsubProc = Popen(bsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  # Check here when these jobs are finished before proceeding
  qsubCMD = ["bsub", "-w", jobs[:-2]]
  echoProc = Popen(echoSleep, stdout=PIPE)
  bsubProc = Popen(bsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  bsubProc.communicate()[0]


def runCopasiPP(models_dir, model, nfits, pp_cpus):
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
  # If this computation is performed on a cluster_type, start this on each node of the cluster_type. 
  # The list of servers and ports must be updated in the configuration file
  # (NOTE: It requires the installation of python-pp)
  #ppserver -p 65000 -i my-node.abc.ac.uk -s "donald_duck" -w 5 &

  # Perform this task using python-pp (parallel python dependency)
  sb_param_estim__copasi_parallel.main(server_list, port_list, secret, models_dir, model, nfits, pp_cpus)





# Input parameters
# model: read the model
# models_dir: read the models dir
# output_dir: The output dir
# tmp_dir: read the temp dir
# sim_number: the number of simulations to perform
def main(model, models_dir, data_dir, data_folder, cluster_type, pp_cpus, nfits, results_dir, output_folder, tmp_dir):
  
  if int(nfits) < 1: 
    print("ERROR: variable " + nfits + " must be greater than 0. Please, check your configuration file.");
    return

  if not os.path.exists(data_dir):
    print(data_dir + " does not exist.") 
    return  

  if not os.path.isfile(os.path.join(models_dir,model)):
    print(os.path.join(models_dir, model) + " does not exist.") 
    return  
  
  if not os.path.exists(os.path.join(results_dir, output_folder)):
    os.mkdir(os.path.join(results_dir, output_folder)) 


  print("Configure Copasi:")
  sb_param_estim__copasi_utils_randomise_start_values.main(models_dir, model, nfits)

  print("\n")
  print("Concurrent parameter estimation:")
  # for some reason, CopasiSE ignores the "../" for the data file and assumes that the Data folder is inside the Models folder..
  # Let's temporarily copy this folder and then delete it.
  if os.path.exists(os.path.join(models_dir, data_folder)):
    os.rename(os.path.join(models_dir, data_folder), os.path.join(models_dir, data_folder+"_{:%Y%m%d%H%M%S}".format(datetime.datetime.now())))
  shutil.copytree(data_dir, os.path.join(models_dir, data_folder))

  
  if cluster_type == "sge" or cluster_type == "lsf":
    # Test this with echo "Copasi insulin_receptor.cps" | xargs xargs using Python environment.
    # The following works:
    # copasiCMD = "CopasiSE insulin_receptor.cps"      
    # echoCMD=["echo", copasiCMD]      
    # xargsCMD=["xargs", "xargs"]
    # echoProc = subprocess.Popen(echoCMD, stdout=subprocess.PIPE)
    # xargsProc = subprocess.Popen(xargsCMD, stdin=echoProc.stdout)
    outDir = os.path.join(results_dir, 'out')
    errDir = os.path.join(results_dir, 'err')
    if not os.path.exists(outDir):
      os.makedirs(outDir)
    if not os.path.exists(errDir):
      os.makedirs(errDir)   
      
    if cluster_type == "sge":  # use SGE (Sun Grid Engine)
      runCopasiSGE(models_dir, model[:-4], outDir, errDir, nfits)

    elif cluster_type == "lsf": # use LSF (Platform Load Sharing Facility)
      runCopasiLSF(models_dir, model[:-4], outDir, errDir, nfits)      
        
  else: # use pp by default (parallel python). This is configured to work locally using multi-core.
    if cluster_type != "pp":
      print("Warning - Variable cluster_type is not set correctly in the configuration file. Values are: pp, lsf, sge. Running pp by default")    
    runCopasiPP(models_dir, model[:-4], nfits, pp_cpus)

  # remove the previously copied Data folder
  shutil.rmtree(os.path.join(models_dir, data_folder), ignore_errors=True) 

  # Move the files to the results_dir
  tmpFiles = os.listdir(tmp_dir)
  for file in tmpFiles:
    shutil.move(os.path.join(tmp_dir, file), os.path.join(results_dir, output_folder, file))

