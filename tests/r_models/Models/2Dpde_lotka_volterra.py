import os
import sys
import subprocess
import shlex

# This is a Python wrapper used to run an R model.
# The R model receives the report_filename as input
# and must add the results to it.

# Retrieve the report file name
report_filename = "2Dpde_lotka_volterra.csv"
if len(sys.argv) > 1:
    report_filename = sys.argv[1]

command = 'Rscript --vanilla ' + os.path.join(os.path.dirname(__file__), '2Dpde_lotka_volterra.r') + \
          ' ' + report_filename

# Block until command is finished
subprocess.call(shlex.split(command))