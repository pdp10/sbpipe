import os
import sys
import subprocess
import shlex

# This is a Python wrapper used to run an R model.
# The R model receives the report_filename as input
# and must add the results to it.

# Retrieve the report file name
report_filename = "sde_cox_ingersoll_ross_process.csv"
if len(sys.argv) > 1:
    report_filename = sys.argv[1]

command = 'Rscript --vanilla ' + os.path.join(os.path.dirname(__file__), 'sde_cox_ingersoll_ross_process.r') + \
          ' ' + report_filename

# we replace \\ with / otherwise subprocess complains on windows systems.
command = command.replace('\\', '\\\\')

# Block until command is finished
subprocess.call(shlex.split(command))
