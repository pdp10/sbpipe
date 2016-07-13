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




import os, sys
from subprocess import Popen,PIPE

SB_PIPE = os.environ["SB_PIPE"]

sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))
from BasicSyncCounter import *

import pp

# Desc: This program runs parallel estimation computations with pp module 

# For more information, see: http://www.parallelpython.com/content/view/15/30/#QUICKCLUSTERS
###############################################################
# You can put this into a script and run it on server side..
# on server side (here: 127.0.0.1), start:
# ppserver.py -p 65000 -i 127.0.0.1 -s "donald_duck" -w 5 &
#
# NB: -w is the number of core YOU can use. If a server is used by more users, 
# set the number lower than the number of cpus
#
# Command line options, ppserver.py
# Usage: ppserver.py [-hda] [-i interface] [-b broadcast] [-p port] [-w nworkers] [-s secret] [-t seconds]
# Options:
# -h                 : this help message
# -d                 : debug
# -a                 : enable auto-discovery service
# -i interface       : interface to listen
# -b broadcast       : broadcast address for auto-discovery service
# -p port            : port to listen
# -w nworkers        : number of workers to start
# -s secret          : secret for authentication
# -t seconds         : timeout to exit if no connections with clients exist
###############################################################



def parallel_computation(command, timestamp, cluster_type, runs, output_dir, servers="localhost:65000", secret="sb_pipe", pp_cpus=1):
  if cluster_type == "sge" or cluster_type == "lsf":
    outDir = os.path.join(output_dir, 'out')
    errDir = os.path.join(output_dir, 'err')
    if not os.path.exists(outDir):
      os.makedirs(outDir)
    if not os.path.exists(errDir):
      os.makedirs(errDir)   
    
    if cluster_type == "sge":  # use SGE (Sun Grid Engine)
      runJobsSGE(command, timestamp, outDir, errDir, runs)

    elif cluster_type == "lsf": # use LSF (Platform Load Sharing Facility)
      runJobsLSF(command, timestamp, outDir, errDir, runs)      
        
  else: # use pp by default (parallel python). This is configured to work locally using multi-core.
    if cluster_type != "pp":
      print("Warning - Variable cluster_type is not set correctly in the configuration file. Values are: pp, lsf, sge. Running pp by default")
    runJobsPP(command, timestamp, runs, pp_cpus, servers, secret)




def runCommandInstance(command):
  """ Run a command instance"""
  p1 = subprocess.Popen(command, stdout=subprocess.PIPE) 
  p1.communicate()[0]


def runCommandPP(command, commandIterSubStr, runs, server, syncCounter=BasicSyncCounter()):  
  """ Run parallel instances of a command """
  for i in xrange(1, runs+1):
    commandList = command.replace(commandIterSubStr, str(i)).split(" ")
    callbackargs = (i,)
    server.submit(runCommandInstance,
		  (commandList,),
		  depfuncs=(),
		  modules=("subprocess",),
		  callback=syncCounter.add,          
		  callbackargs=callbackargs,
		  group="my_processes")
    print("Process P" + str(i) + " started")



# Perform this task using python-pp (parallel python dependency). 
# If this computation is performed on a cluster_type, start this on each node of the cluster_type. 
# The list of servers and ports must be updated in the configuration file
# (NOTE: It requires the installation of python-pp)
#ppserver -p 65000 -i my-node.abc.ac.uk -s "donald_duck" -w 5 &
def runJobsPP(command, commandIterSubStr, runs, pp_cpus, servers, secret):
  """
  command : the full command to run as a job
  iterSubStr : the substring in command to be replaced with a number 
  runs: The number of runs to perform
  ncpus: The number of available cpus. Set ncpus to 0 if all the processes have to run on a server!
  servers: A string containing a list of servers:ports to connect (e.g. "localhost:65000,my-node.abc.ac.uk:65000")
  secret: The secret key to communicate for the above server  
  """
  ### ppserver configuration
  ppservers=tuple(servers.split(','))  
  
  # Create the Job Server.
  if pp_cpus > 0:
      # Creates jobserver with ncpus workers
      job_server = pp.Server(ncpus=pp_cpus, ppservers=ppservers, secret=secret)
  else:
      # Creates jobserver with automatically detected number of workers
      job_server = pp.Server(ppservers=ppservers, secret=secret)        
  print("ppserver will use " + str(job_server.get_ncpus()) + " cpus on these nodes:\n" + str(job_server.get_active_nodes()) + "\n")

  # Create an instance of callback class
  syncCounter = BasicSyncCounter()
  
  print("Starting parallel computation:")
  runCommandPP(command, commandIterSubStr, runs, server=job_server, syncCounter=syncCounter)        
  # Wait for jobs in all groups to finish 
  job_server.wait(group="my_processes")

  # Print the status of the parallel computation. Everything different from 0 means error.
  if syncCounter.get_value() is False: 
    print("\nParallel computation finished with status: 1 - Some computation failed. Do all output files exist?\n")
  else:
    print("\nParallel computation finished with status: 0 - If errors occur, check whether your command runs correctly.\n")
  
  # print statistics
  job_server.print_stats()
  job_server.destroy()




def runJobsSGE(command, commandIterSubStr, outDir, errDir, runs):
  """
  command : the full command to run as a job
  iterSubStr : the substring in command to be replaced with a number 
  outDir : the directory containing the standard output from qsub
  errDir : the directory containing the standard error from qsub
  runs : the number of runs to execute
  """
  # Test this with echo "ls -la" | xargs xargs using Python environment.
  # The following works:
  # lsCMD = "ls -la"      
  # echoCMD=["echo", lsCMD]      
  # xargsCMD=["xargs", "xargs"]
  # echoProc = subprocess.Popen(echoCMD, stdout=subprocess.PIPE)
  # xargsProc = subprocess.Popen(xargsCMD, stdin=echoProc.stdout)  
  jobs = ""
  echoSleep = ["echo", "sleep 1"]
  for i in xrange(1,runs+1):
      # Now the same with qsub
      jobs = "j"+str(i)+","+jobs
      echoCMD = ["echo", command.replace(commandIterSubStr, str(i))]
      qsubCMD = ["qsub", "-cwd", "-N", "j"+str(i), "-o", os.path.join(outDir, "j"+str(i)), "-e", os.path.join(errDir,"j"+str(i))] 
      echoProc = Popen(echoCMD, stdout=PIPE)
      qsubProc = Popen(qsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  # Check here when these jobs are finished before proceeding
  qsubCMD = ["qsub", "-sync", "y", "-hold_jid", jobs[:-1]]  
  echoProc = Popen(echoSleep, stdout=PIPE)
  qsubProc = Popen(qsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  qsubProc.communicate()[0]





def runJobsLSF(command, commandIterSubStr, outDir, errDir, runs):
  """
  command : the full command to run as a job
  iterSubStr : the substring in command to be replaced with a number 
  outDir : the directory containing the standard output from bsub
  errDir : the directory containing the standard error from bsub
  runs : the number of runs to execute
  """  
  jobs = ""
  echoSleep = ["echo", "sleep 1"]  
  for i in xrange(1,runs+1):
      jobs = "done(j"+str(i)+")&&"+jobs
      echoCMD = ["echo", command.replace(commandIterSubStr, str(i))]
      bsubCMD = ["bsub", "-cwd", "-J", "j"+str(i), "-o", os.path.join(outDir, "j"+str(i)), "-e", os.path.join(errDir, "j"+str(i))] 
      echoProc = Popen(echoCMD, stdout=PIPE)
      bsubProc = Popen(bsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  # Check here when these jobs are finished before proceeding
  import random 
  import string
  jobName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))
  bsubCMD = ["bsub", "-J", jobName, "-w", jobs[:-2]]
  echoProc = Popen(echoSleep, stdout=PIPE)
  bsubProc = Popen(bsubCMD, stdin=echoProc.stdout, stdout=PIPE)
  bsubProc.communicate()[0]
  # Something better than the following would be highly desirable
  import time
  found = True
  while found:
    time.sleep(2)
    myPoll = Popen(["bjobs", "-psr"], stdout=PIPE)
    output = myPoll.communicate()[0]    
    if not jobName in output:
      found = False
  


