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

try:
    subprocess.Popen(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

    # The Jar file for Java models includes a manifest.mf specifying the main class.
    command = 'java -jar ' + os.path.join(os.path.dirname(__file__), 'simqueue-devel-jar-with-dependencies.jar') + \
              ' ' + report_filename

    # we replace \\ with / otherwise subprocess complains on windows systems.
    command = command.replace('\\', '\\\\')

    # Block until command is finished
    subprocess.call(shlex.split(command))


except OSError as e:
    print("Warning: skipping test as no Java Virtual Machine was found.")