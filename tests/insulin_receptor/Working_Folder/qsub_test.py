#!/usr/bin/env python
import sys
import subprocess

case = int(sys.argv[1])

queue = "all.q"
jobName = "test%i" % case
cmd = "echo %i; date; sleep 2; date" % case
echoArgs = ["echo", "-e", "'%s'" % cmd]
print(" ".join(echoArgs))
qsubArgs = ["qsub", "-cwd", "-j", "y", "-V", "-q", queue, "-N", jobName]
print(" ".join(qsubArgs))

if case == 1:
    wholeCmd = " ".join(echoArgs) + " | " + " ".join(qsubArgs)
    out = subprocess.Popen(wholeCmd, shell=True, stdout=subprocess.PIPE)
    out = out.communicate()[0]

if case == 2:
    wholeCmd = " ".join(echoArgs) + " | " + " ".join(qsubArgs)
    out = subprocess.Popen(wholeCmd, shell=False, stdout=subprocess.PIPE)
    out = out.communicate()[0]

if case == 3:
    # http://stackoverflow.com/a/13332300/597069
    echoProc = subprocess.Popen(echoArgs, stdout=subprocess.PIPE)
    out = subprocess.check_output(qsubArgs, stdin=echoProc.stdout)
    echoProc.wait()

if case == 4:
    # http://stackoverflow.com/a/17129244/597069
    echoProc = subprocess.Popen(echoArgs, stdout=subprocess.PIPE)
    qsubProc = subprocess.Popen(qsubArgs, stdin=echoProc.stdout, stdout=subprocess.PIPE)
    echoProc.stdout.close()
    out = qsubProc.communicate()[0]
    echoProc.wait()

jobId = out.split()[2]
print jobId

