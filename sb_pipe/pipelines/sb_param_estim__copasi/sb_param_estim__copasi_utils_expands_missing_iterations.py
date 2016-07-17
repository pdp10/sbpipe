#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $



# The parameter estimation task in Copasi only reports the function number by which
# the Squared Mean Error is decreased. This script add also the other values so it 
# is possible to compare more parameter estimation tasks under the same conditions and 
# test whether or not the model reach a good optima statistically.

# This script only extends the result of the Copasi parameter estimation task. 
# Use the R script to perform statistics and compute plots. (~/phd/project/scripts)

# command:
# ./expands_missing_iterations_par_est.py --with-header Calibration1 calibration/dataset_short/dataset1.csv calibration/dataset/dataset1-extended.csv 


import sys


# INITIALISATION
# hearder: the header 
# error : ?
# filenamein : the input file
# filenameout : the output file
def main(hearder, error, filenamein, filenameout):
  
  fileIN = open(filenamein, "r")
  fileOUT = open(filenameout, "w")

  if header == "--with-header":
    fileOUT.write("Iterations\t" + error + "\n")
  else:
    fileOUT.write("Iterations\tSquared_Mean_Error\n")

  # It assumes the table contain a header line. It skips it.
  line = fileIN.readline()

  line = fileIN.readline()
  content = line.split()
  line_next = line
  content_next = content
  iteration = 0
  lastone = False

  while len(content) > 0 and not lastone: 
    if len(content_next) > 0:
      if int(content_next[0]) <= iteration:
	line = line_next
	content = content_next
	line_next = fileIN.readline()
	content_next = line_next.split()
	print(content)
    elif int(content[0]) <= iteration:
      lastone = True
    fileOUT.write(str(iteration) + "\t" + content[1] + "\n")
    iteration = iteration + 1

  fileIN.close()
  fileOUT.close()
