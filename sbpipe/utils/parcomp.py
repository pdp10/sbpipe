#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Object: Execute the model several times for deterministic or stochastic analysis


from __future__ import print_function
import logging
import sys
import os
import multiprocessing
import subprocess
import shlex
from time import sleep
logger = logging.getLogger('sbpipe')


def run_cmd(cmd):
    """
    Run a command using Python subprocess.

    :param cmd: The string of the command to run
    """
    if sys.version_info > (3,):
        with subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            out, err = p.communicate()
    else:
        p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    return out, err


def run_cmd_block(cmd):
    """
    Run a command using Python subprocess. Block the call until the command has finished.

    :param cmd: A tuple containing the string of the command to run
    """
    p = subprocess.call(shlex.split(cmd))


def parcomp(cmd, cmd_iter_substr, output_dir, cluster='local', runs=1, local_cpus=1, output_msg=False,
            colnames=[]):
    """
    Generic function to run a command in parallel

    :param cmd: the command string to run in parallel
    :param cmd_iter_substr: the substring of the iteration number. This will be replaced in a number automatically
    :param output_dir: the output directory
    :param cluster: the cluster type among local (Python multiprocessing), sge, or lsf
    :param runs: the number of runs. Ignored if colnames is not empty
    :param local_cpus: the number of cpus to use at most
    :param output_msg: print the output messages on screen (available for cluster='local' only)
    :param colnames: the name of the columns to process
    :return: True if the computation succeeded.
    """
    logger.debug("Parallel computation using " + cluster)
    logger.debug("Command: " + cmd)
    logger.debug("Iter ID string: " + cmd_iter_substr)
    logger.debug("# runs: " + str(runs))
    if cluster == "sge" or cluster == "lsf":
        out_dir = os.path.join(output_dir, 'out')
        err_dir = os.path.join(output_dir, 'err')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if not os.path.exists(err_dir):
            os.makedirs(err_dir)

        if cluster == "sge":  # use SGE (Sun Grid Engine)
            return run_jobs_sge(cmd, cmd_iter_substr, out_dir, err_dir, runs, colnames)

        elif cluster == "lsf":  # use LSF (Platform Load Sharing Facility)
            return run_jobs_lsf(cmd, cmd_iter_substr, out_dir, err_dir, runs, colnames)

    else:  # use local by default (python multiprocessing). This is configured to work locally using multi-core.
        if cluster != "local":
            logger.warning(
                "Variable cluster is not set correctly in the configuration file. "
                "Values are: `local`, `lsf`, `sge`. Running `local` by default")
        return run_jobs_local(cmd, cmd_iter_substr, runs, local_cpus, output_msg, colnames)


def progress_bar(it, total):
    """
    A minimal CLI progress bar.

    :param it: current iteration starting from 1
    :param total: total iterations
    """
    percent = '(' + ("{0:.1f}").format(100 * (it / float(total))) + '%)'
    progress = str(it) + ' of ' + str(total)
    print('\r%s %s %s' % ('Initialised:', progress, percent), end='\r')
    if it == total:
        print()


def progress_bar2(it, total):
    """
    A CLI progress bar.

    :param it: current iteration starting from 1
    :param total: total iterations
    """
    percent = ("{0:.1f}").format(100 * (it / float(total)))
    length = 50
    filled = int(length * it // total)
    bar = '#' * filled + '-' * (length - filled)
    progress = '(' + str(it) + ' of ' + str(total) + ')'
    print('\r%s |%s| %s%% %s' % ('Progress:', bar, percent, progress), end='\r')
    if it == total:
        print()

def call_proc(params):
    """
    Run a command using Python subprocess.

    :param params: A tuple containing (the string of the command to run, the command id)
    """
    cmd, id, runs, handler_level = params
    if handler_level <= logging.INFO:
        progress_bar(id, runs)
    if sys.version_info > (3,):
        with subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            out, err = p.communicate()
    else:
        p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    return out, err


def run_jobs_local(cmd, cmd_iter_substr, runs=1, local_cpus=1, output_msg=False, colnames=[]):
    """
    Run jobs using python multiprocessing locally.

    :param cmd: the full command to run as a job
    :param cmd_iter_substr: the substring in command to be replaced with a number
    :param runs: the number of runs. Ignored if colnames is not empty
    :param local_cpus: The number of available cpus. If local_cpus <=0, only one core will be used.
    :param output_msg: print the output messages on screen (available for cluster_type='local' only)
    :param colnames: the name of the columns to process
    :return: True
    """

    # Create a Pool.
    pool = multiprocessing.Pool(1)
    if local_cpus > 0:
        if local_cpus <= multiprocessing.cpu_count():
            # Create a pool with local_cpus
            pool = multiprocessing.Pool(local_cpus)
            logger.debug('Initialised multiprocessing.Pool with ' + str(local_cpus))
        else:
            logger.warning('`local_cpus` is higher than the physical number of CPUs (' +
                           str(multiprocessing.cpu_count()) + '). Setting `local_cpus` to ' +
                           str(multiprocessing.cpu_count()))
            pool = multiprocessing.Pool(multiprocessing.cpu_count())

    logger.info("Starting computation...")

    results = []

    # get the current level for the StreamHandler
    # this must be executed at run-time
    if len(logger.handlers) > 1:
        handler_level = logger.handlers[1].level
    else:
        handler_level = logging.INFO

    if len(colnames) > 0:
        runs = len(colnames)
        for i, column in enumerate(colnames):
            command = cmd.replace(cmd_iter_substr, column)
            logger.debug(command)
            params = (command, i+1, runs, handler_level)
            results.append(pool.apply_async(call_proc, (params,)))
    else:
        for i in range(0, runs):
            command = cmd.replace(cmd_iter_substr, str(i+1))
            logger.debug(command)
            params = (command, i+1, runs, handler_level)
            results.append(pool.apply_async(call_proc, (params,)))

    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()

    failed = 0
    for result in results:

        out, err = result.get()
        # convert byte to str. Necessary for Python 3+.
        # this is also compatible with Python 2.7
        out = out.decode('utf-8')
        err = err.decode('utf-8')

        if 'error' in err.lower():
            logger.error('\n' + err)
            failed += 1
        elif 'warning' in err.lower():
            logger.warning('\n' + err)
        else:
            logger.debug('\n' + err)

        if 'error' in out.lower():
            logger.error('\n' + out)
        elif 'warning' in out.lower():
            logger.warning('\n' + out)
        else:
            if output_msg:
                logger.info('\n' + out)
            else:
                logger.debug('\n' + out)

    # Print the status of the parallel computation.
    logger.info("Computation terminated.")
    if failed == runs:
        logger.warning('All computations seem to have errors in the standard error.')
        logger.warning("For additional information, run SBpipe using the `--verbose` option.")
        # return False
    elif failed > 0:
        logger.warning("Some computation might have failed. Do all output files exist?")
        logger.warning("For additional information, run SBpipe using the `--verbose` option.")
    else:
        logger.info("If errors occur, check that " + cmd.split(" ")[0] + " runs correctly.")
        logger.info("For additional information, run SBpipe using the `--verbose` option.")
    return True


def run_jobs_sge(cmd, cmd_iter_substr, out_dir, err_dir, runs=1, colnames=[]):
    """
    Run jobs using a Sun Grid Engine (SGE) cluster.

    :param cmd: the full command to run as a job
    :param cmd_iter_substr: the substring in command to be replaced with a number
    :param out_dir: the directory containing the standard output from qsub
    :param err_dir: the directory containing the standard error from qsub
    :param runs: the number of runs. Ignored if colnames is not empty
    :param colnames: the name of the columns to process
    :return: True if the computation succeeded.
    """
    # Test this with echo "ls -la" | xargs xargs using Python environment.
    # The following works:
    # lsCMD = "ls -la"
    # echo_cmd=["echo", lsCMD]
    # xargsCMD=["xargs", "xargs"]
    # echo_proc = subprocess.Popen(echo_cmd, stdout=subprocess.PIPE)
    # xargsProc = subprocess.Popen(xargsCMD, stdin=echo_proc.stdout)

    logger.info("Starting computation...")
    jobs = ""
    cmd_iter_substr = cmd_iter_substr.strip('/')

    # get the current level for the StreamHandler
    # this must be executed at run-time
    if len(logger.handlers) > 1:
        handler_level = logger.handlers[1].level
    else:
        handler_level = logging.INFO

    if len(colnames) > 0:
        runs = len(colnames)
        for i, column in enumerate(colnames):
            # Now the same with qsub
            jobs = "j" + column + "_" + cmd_iter_substr + "," + jobs
            qsub_cmd = ["qsub", "-cwd", "-V", "-N", "j" + column + "_" + cmd_iter_substr, "-o", os.path.join(out_dir, "j" + column), "-e", os.path.join(err_dir, "j" + column), "-b", "y", cmd.replace(cmd_iter_substr, column)]
            logger.debug(qsub_cmd)
            #logger.info('Starting Task ' + column)
            if sys.version_info > (3,):
                with subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE) as p:
                    p.communicate()[0]
            else:
                qsub_proc = subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE)
                qsub_proc.communicate()[0]
            if handler_level <= logging.INFO:
                sleep(0.01)
                progress_bar(i+1, runs)
    else:
        for i in range(0, runs):
            # Now the same with qsub
            jobs = "j" + str(i+1) + "_" + cmd_iter_substr + "," + jobs
            qsub_cmd = ["qsub", "-cwd", "-V", "-N", "j" + str(i+1) + "_" + cmd_iter_substr, "-o", os.path.join(out_dir, "j" + str(i+1)), "-e", os.path.join(err_dir, "j" + str(i+1)), "-b", "y", cmd.replace(cmd_iter_substr, str(i+1))]
            logger.debug(qsub_cmd)
            #logger.info('Starting Task ' + str(i+1))
            if sys.version_info > (3,):
                with subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE) as p:
                    p.communicate()[0]
            else:
                qsub_proc = subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE)
                qsub_proc.communicate()[0]
            if handler_level <= logging.INFO:
                sleep(0.01)
                progress_bar(i+1, runs)
    # Check here when these jobs are finished before proceeding
    # don't add names for output and error files as they can generate errors..
    qsub_cmd = ["qsub", "-sync", "y", "-b", "y", "-o", "/dev/null", "-e", "/dev/null", "-hold_jid", jobs[:-1], "sbpipe_" + cmd_iter_substr, "1"]
    if sys.version_info > (3,):
        with subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE) as p:
            p.communicate()[0]
    else:
        qsub_proc = subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE)
        qsub_proc.communicate()[0]
    logger.debug(qsub_cmd)
    logger.info("Computation terminated.")
    return quick_debug(cmd, out_dir, err_dir)


def run_jobs_lsf(cmd, cmd_iter_substr, out_dir, err_dir, runs=1, colnames=[]):
    """
    Run jobs using a Load Sharing Facility (LSF) cluster.

    :param cmd: the full command to run as a job
    :param cmd_iter_substr: the substring in command to be replaced with a number
    :param out_dir: the directory containing the standard output from bsub
    :param err_dir: the directory containing the standard error from bsub
    :param runs: the number of runs. Ignored if colnames is not empty
    :param colnames: the name of the columns to process
    :return: True if the computation succeeded.
    """
    logger.info("Starting computation...")
    jobs = ""
    cmd_iter_substr = cmd_iter_substr.strip('/')

    # get the current level for the StreamHandler
    # this must be executed at run-time
    if len(logger.handlers) > 1:
        handler_level = logger.handlers[1].level
    else:
        handler_level = logging.INFO

    if len(colnames) > 0:
        runs = len(colnames)
        for i, column in enumerate(colnames):
            jobs = "done(j" + column + "_" + cmd_iter_substr + ")&&" + jobs
            bsub_cmd = ["bsub", "-cwd", "-J", "j" + column + "_" + cmd_iter_substr, "-o", os.path.join(out_dir, "j" + column), "-e",
                        os.path.join(err_dir, "j" + column), cmd.replace(cmd_iter_substr, column)]
            logger.debug(bsub_cmd)
            #logger.info('Starting Task ' + column)
            if sys.version_info > (3,):
                with subprocess.Popen(bsub_cmd, stdout=subprocess.PIPE) as p:
                    p.communicate()[0]
            else:
                bsub_proc = subprocess.Popen(bsub_cmd, stdout=subprocess.PIPE)
                bsub_proc.communicate()[0]
            if handler_level <= logging.INFO:
                sleep(0.01)
                progress_bar(i+1, runs)
    else:
        for i in range(0, runs):
            jobs = "done(j" + str(i+1) + "_" + cmd_iter_substr + ")&&" + jobs
            bsub_cmd = ["bsub", "-cwd", "-J", "j" + str(i+1) + "_" + cmd_iter_substr, "-o", os.path.join(out_dir, "j" + str(i+1)), "-e", os.path.join(err_dir, "j" + str(i+1)), cmd.replace(cmd_iter_substr, str(i+1))]
            logger.debug(bsub_cmd)
            #logger.info('Starting Task ' + str(i+1))
            if sys.version_info > (3,):
                with subprocess.Popen(bsub_cmd, stdout=subprocess.PIPE) as p:
                    p.communicate()[0]
            else:
                bsub_proc = subprocess.Popen(bsub_cmd, stdout=subprocess.PIPE)
                bsub_proc.communicate()[0]
            if handler_level <= logging.INFO:
                sleep(0.01)
                progress_bar(i + 1, runs)
    # Check here when these jobs are finished before proceeding
    import random
    import string
    job_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))
    bsub_cmd = ["bsub", "-J", job_name, "-o", "/dev/null", "-e", "/dev/null", "-w", jobs[:-2], "sbpipe_" + cmd_iter_substr, "1"]
    logger.debug(bsub_cmd)
    if sys.version_info > (3,):
        with subprocess.Popen(bsub_cmd, stdout=subprocess.PIPE) as p:
            p.communicate()[0]
    else:
        bsub_proc = subprocess.Popen(bsub_cmd, stdout=subprocess.PIPE)
        bsub_proc.communicate()[0]
    # Something better than the following would be highly desirable
    import time
    found = True
    while found:
        time.sleep(2)
        if sys.version_info > (3,):
            with subprocess.Popen(["bjobs", "-psr"], stdout=subprocess.PIPE) as p:
                output = p.communicate()[0]
        else:
            my_poll = subprocess.Popen(["bjobs", "-psr"], stdout=subprocess.PIPE)
            output = my_poll.communicate()[0]
        if job_name not in output:
            found = False
    logger.info("Computation terminated.")
    return quick_debug(cmd, out_dir, err_dir)


def quick_debug(cmd, out_dir, err_dir):
    """
    Look up for `error` and `warning` in the standard output and error files.
    A simple debugging function checking the generated log files. We don't stop the computation because it happens
    that these messages are more `warnings` than real errors.

    :param cmd: the executed command
    :param out_dir: the directory containing the standard output files
    :param err_dir: the directory contining the standard error files
    :return: True
    """
    outcome = True

    logger.debug("Running parcomp.quick_debug()")

    filename = os.path.join(err_dir, "j1")
    if os.path.isfile(filename):
        if not is_output_file_clean(filename, 'standard error'):
            outcome = False
    filename = os.path.join(out_dir, "j1")
    if os.path.isfile(filename):
        if not is_output_file_clean(filename, 'standard output'):
            outcome = False
    if not outcome:
        logger.warning("\nSome computation might have failed. Please check the output in the folders:")
        logger.warning("\t" + out_dir + ' (standard output)')
        logger.warning("\t" + err_dir + ' (standard error)')
        logger.warning("For additional information, run SBpipe using the `--verbose` option.")
        logger.warning("(ignore previous warnings if results are generated as expected)")
    else:
        logger.info("If errors occur, please check the output in the folders: ")
        logger.info("\t" + out_dir + ' (standard output)')
        logger.info("\t" + err_dir + ' (standard error)')
        logger.info("For additional information, run SBpipe using the `--verbose` option.")
    # return outcome
    return True


def is_output_file_clean(filename, stream_type='standard output'):
    """
    Check whether a file contains the string 'error' or 'warning'. If so a message is printed.

    :param filename: a file
    :param stream_type: 'stderr' for standard error, 'stdout' for standard output.
    :return: True
    """
    with open(filename) as my_file:
        content = my_file.read().replace('\n', ' ').lower()
        if 'error' in content:
            logger.warning('Found word `error` in ' + stream_type)
            logger.warning('\n' + content)
            return False
        elif 'warning' in content:
            logger.warning('Found word `warning` in ' + stream_type)
            logger.warning('\n' + content)
        else:
            logger.debug('\n' + content)
    return True
