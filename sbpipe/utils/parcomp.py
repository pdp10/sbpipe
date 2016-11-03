#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Execute the model several times for deterministic or stochastical analysis
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 13:45:32 $

import logging
import os
import sys
import subprocess

logger = logging.getLogger('sbpipe')

SBPIPE = os.environ["SBPIPE"]

sys.path.append(os.path.join(SBPIPE, 'sbpipe', 'utils', 'python'))
from monitor import *

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



def parcomp(command, command_iter_substr, cluster_type, runs, output_dir, pp_cpus=1):
    """
  Generic funcion to run a command in parallel
  
  :param command: the command string to run in parallel
  :param command_iter_substr: the substring of the iteration number. This will be replaced in a number automatically
  :param cluster_type: the cluster type among pp (multithreading), sge, or lsf
  :param runs: the number of runs
  :param output_dir: the output directory
  :param pp_cpus: the number of cpus that pp should use at most
  """
    if cluster_type == "sge" or cluster_type == "lsf":
        outDir = os.path.join(output_dir, 'out')
        errDir = os.path.join(output_dir, 'err')
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        if not os.path.exists(errDir):
            os.makedirs(errDir)

        if cluster_type == "sge":  # use SGE (Sun Grid Engine)
            run_jobs_sge(command, command_iter_substr, outDir, errDir, runs)

        elif cluster_type == "lsf":  # use LSF (Platform Load Sharing Facility)
            run_jobs_lsf(command, command_iter_substr, outDir, errDir, runs)

    else:  # use pp by default (parallel python). This is configured to work locally using multi-core.
        if cluster_type != "pp":
            logger.warn(
                "Variable cluster_type is not set correctly in the configuration file. Values are: pp, lsf, sge. Running pp by default")
        run_jobs_pp(command, command_iter_substr, runs, pp_cpus)


def run_cmd_instance(command):
    """
    Run a command using Python subprocess.

    :param command: the string of the command to run
    """
    p1 = subprocess.Popen(command, stdout=subprocess.PIPE)
    p1.communicate()[0]


def run_command_pp(command, command_iter_substr, runs, server, syncCounter=Monitor()):
    """
    Run instances of a command in multithreading using parallel python (pp).

    :param command: the command string to run in parallel
    :param command_iter_substr: the substring of the iteration number. This will be replaced in a number automatically
    :param runs: the number of runs
    :param server: the server that pp should use
    :param syncCounter: the mutex object to count the jobs
    """
    for i in xrange(1, runs + 1):
        commandList = command.replace(command_iter_substr, str(i)).split(" ")
        callbackargs = (i,)
        server.submit(run_cmd_instance,
                      (commandList,),
                      depfuncs=(),
                      modules=("subprocess",),
                      callback=syncCounter.add,
                      callbackargs=callbackargs,
                      group="my_processes")


def run_jobs_pp(command, command_iter_substr, runs, pp_cpus=1):
    """
    Run jobs using parallel python (pp) locally.

    :param command: the full command to run as a job
    :param command_iter_substr: the substring in command to be replaced with a number
    :param runs: the number of runs to execute
    :param pp_cpus: The number of available cpus. If pp_cpus <=0, all the available cores will be used.
    """

    # If this computation is performed on a cluster_type, start pp-server on each node.
    # The list of servers and ports must be updated in the configuration file

    ### ppserver configuration
    # servers: A string containing a list of servers:ports to connect (e.g. "localhost:65000,my-node.abc.ac.uk:65000")
    # secret: The secret key to communicate for the above server
    # servers = ''  # we run this locally and we didn't start ppserver process. so no need for this.
    secret = ''
    # ppservers=tuple(servers.split(','))
    ppservers = ()

    # Create the Job Server.
    if pp_cpus > 0:
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus=pp_cpus, ppservers=ppservers, secret=secret)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers, secret=secret)
    logger.info("ppserver will use " + str(job_server.get_ncpus()) + " cpus on these nodes: " + str(
        job_server.get_active_nodes()) + "\n")

    # Create an instance of callback class
    syncCounter = Monitor()

    logger.info("Starting parallel computation:")
    run_command_pp(command, command_iter_substr, runs, server=job_server, syncCounter=syncCounter)
    # Wait for jobs in all groups to finish
    job_server.wait(group="my_processes")

    # Print the status of the parallel computation. Everything different from 0 means error.
    if syncCounter.get_value() is False:
        logger.error("Some computation failed. Do all output files exist?")
    else:
        logger.info("Parallel computation terminated. If errors occur, check whether that " + command.split(" ")[
            0] + " runs correctly.")

    # print statistics
    job_server.print_stats()
    job_server.destroy()


def run_jobs_sge(command, command_iter_substr, outDir, errDir, runs):
    """
    Run jobs using a Sun Grid Engine (SGE) cluster.

    :param command: the full command to run as a job
    :param command_iter_substr: the substring in command to be replaced with a number
    :param outDir: the directory containing the standard output from qsub
    :param errDir: the directory containing the standard error from qsub
    :param runs: the number of runs to execute
    """
    # Test this with echo "ls -la" | xargs xargs using Python environment.
    # The following works:
    # lsCMD = "ls -la"
    # echo_cmd=["echo", lsCMD]
    # xargsCMD=["xargs", "xargs"]
    # echo_proc = subprocess.Popen(echo_cmd, stdout=subprocess.PIPE)
    # xargsProc = subprocess.Popen(xargsCMD, stdin=echo_proc.stdout)
    jobs = ""
    echo_sleep = ["echo", "sleep 1"]
    for i in xrange(1, runs + 1):
        # Now the same with qsub
        jobs = "j" + str(i) + "," + jobs
        echo_cmd = ["echo", command.replace(command_iter_substr, str(i))]
        qsub_cmd = ["qsub", "-cwd", "-N", "j" + str(i), "-o", os.path.join(outDir, "j" + str(i)), "-e",
                   os.path.join(errDir, "j" + str(i))]
        echo_proc = subprocess.Popen(echo_cmd, stdout=subprocess.PIPE)
        qsub_proc = subprocess.Popen(qsub_cmd, stdin=echo_proc.stdout, stdout=subprocess.PIPE)
    # Check here when these jobs are finished before proceeding
    # don't add names for output and error files as they can generate errors..
    qsub_cmd = ["qsub", "-sync", "y", "-hold_jid",
               jobs[:-1]]  # , "-o", os.path.join(outDir, "wait"), "-e", os.path.join(errDir, "wait")]
    echo_proc = subprocess.Popen(echo_sleep, stdout=subprocess.PIPE)
    qsub_proc = subprocess.Popen(qsub_cmd, stdin=echo_proc.stdout, stdout=subprocess.PIPE)
    qsub_proc.communicate()[0]


def run_jobs_lsf(command, command_iter_substr, outDir, errDir, runs):
    """
    Run jobs using a Load Sharing Facility (LSF) cluster.

    :param command: the full command to run as a job
    :param command_iter_substr: the substring in command to be replaced with a number
    :param outDir: the directory containing the standard output from bsub
    :param errDir: the directory containing the standard error from bsub
    :param runs: the number of runs to execute
    """
    jobs = ""
    echo_sleep = ["echo", "sleep 1"]
    for i in xrange(1, runs + 1):
        jobs = "done(j" + str(i) + ")&&" + jobs
        echo_cmd = ["echo", command.replace(command_iter_substr, str(i))]
        bsub_cmd = ["bsub", "-cwd", "-J", "j" + str(i), "-o", os.path.join(outDir, "j" + str(i)), "-e",
                   os.path.join(errDir, "j" + str(i))]
        echo_proc = subprocess.Popen(echo_cmd, stdout=subprocess.PIPE)
        bsub_proc = subprocess.Popen(bsub_cmd, stdin=echo_proc.stdout, stdout=subprocess.PIPE)
    # Check here when these jobs are finished before proceeding
    import random
    import string
    job_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))
    bsub_cmd = ["bsub", "-J", job_name, "-w",
               jobs[:-2]]  # , "-o", os.path.join(outDir, "wait"), "-e", os.path.join(errDir, "wait")]
    echo_proc = subprocess.Popen(echo_sleep, stdout=subprocess.PIPE)
    bsub_proc = subprocess.Popen(bsub_cmd, stdin=echo_proc.stdout, stdout=subprocess.PIPE)
    bsub_proc.communicate()[0]
    # Something better than the following would be highly desirable
    import time
    found = True
    while found:
        time.sleep(2)
        my_poll = subprocess.Popen(["bjobs", "-psr"], stdout=subprocess.PIPE)
        output = my_poll.communicate()[0]
        if not job_name in output:
            found = False
