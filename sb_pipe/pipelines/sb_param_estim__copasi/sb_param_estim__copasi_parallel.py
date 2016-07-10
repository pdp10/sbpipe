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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $
#
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



# execute: python run_parallel_param_estim.py [path] [model_pattern] [nfits] [ncpus]

# On client side, run this program

import math
import time
import shutil
import shlex
import subprocess
import sys
import os
SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE,'sb_pipe','utils','python'))

from BasicSyncCounter import *

# apt-get install python-pp
import pp



# Run a Copasi instance
def run_copasi_instance(filename):
  if os.path.isfile(filename) is not True: 
    return False
  # Command output=`CopasiSE -s filename filename`
  p1 = subprocess.Popen(["CopasiSE", "-s", filename, filename], stdout=subprocess.PIPE) 
  p1.communicate()[0]
  return True


# Run parallel instances of Copasi
def run_parallel_copasi(server, args=("","", 1), syncCounter=BasicSyncCounter()):
    (path, model, nfits) = args
    start_time = time.time()
    for index in range(0, nfits):
        # Submit a Copasi Job
        filename = os.path.join(path, model + str(index + 1) + ".cps")

        callbackargs = (index,)
        server.submit(run_copasi_instance,
		      (filename,),
		      depfuncs=(),
		      modules=("subprocess","shlex","os.path"),
		      callback=syncCounter.add,          
		      callbackargs=callbackargs,
		      group="my_processes")
        print("Process P" + str(index) + " started (model: "+ filename +")")



# Main function
# servers: The servers to connect
# ports: The server ports
# secret: The server secret
# path: The path of the models
# model: Them model name pattern
# nfits: The number of calibration to perform
# ncpus: The number of available cpus. Set ncpus to 0 if all the processes have to run on a server!
def main(servers, ports, secret, path, model, nfits, ncpus):
        
    ### ppserver configuration
    # tuple of all parallel python servers to connect with
    # server tuple
    server_list = servers.split(',')
    port_list = ports.split(',')
    resources = min(len(server_list), len(port_list))
    ppservers=()
    for idx in range(0, resources):
      print("Adding server: " + server_list[idx]+":"+port_list[idx] + "\n")
      ppservers=ppservers + (server_list[idx]+":"+port_list[idx],)
    
    # Create an instance of callback class
    syncCounter = BasicSyncCounter()

    # Create the Job Server.
    if ncpus > 0:
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus=ncpus, ppservers=ppservers, secret=secret)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers, secret=secret)        
            
        
    print("ppserver will use " + str(job_server.get_ncpus()) + " cores locally.\n")        

    print("\nComputing Parallel Parameter Estimation using Copasi\n")
    run_parallel_copasi(server=job_server, args=(path, model, nfits), syncCounter=syncCounter)        
    # Wait for jobs in all groups to finish 
    job_server.wait(group="my_processes")

    # Print the status of the parallel computation. Everything different from 0 means error.
    if syncCounter.get_value() is False: 
      print("\nParallel computation finished with status: 1 - Some computation failed. Do all Copasi files exist?\n")
    else:
      print("\nParallel computation finished with status: 0 - If errors occur, check whether CopasiSE runs correctly\n")
    
    # print statistics
    job_server.print_stats()
    job_server.destroy()

