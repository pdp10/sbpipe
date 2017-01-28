import os
import sys
import subprocess
import shlex

# This is a Python wrapper used to run an octave model.
# The octave model receives the report_filename as input
# and must add the results to it.

# Retrieve the report file name
report_filename = "simqueue-devel-jar-with-dependencies.csv"
if len(sys.argv) > 1:
    report_filename = sys.argv[1]

# The Jar file for Java models includes a manifest.mf specifying the main class.
command = 'java -jar ' + os.path.join(os.path.dirname(__file__), 'simqueue-devel-jar-with-dependencies.jar') + \
          ' ' + report_filename

# Block until command is finished
subprocess.call(shlex.split(command))
