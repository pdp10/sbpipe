import os
import sys
import subprocess
import shlex

# This is a Python wrapper used to run an octave model.
# The octave model receives the report_filename as input
# and must add the results to it.

# Retrieve the report file name
report_filename = "sim_simple_reacts.csv"
if len(sys.argv) > 1:
    report_filename = sys.argv[1]

# Create a command running 'sim_simple_reacts.m' using Octave.
# the report filename is passed as input argument
command = 'octave ' + os.path.join(os.path.dirname(__file__), 'sim_simple_reacts.m') + ' ' + report_filename

# Block until command is finished
subprocess.call(shlex.split(command))
