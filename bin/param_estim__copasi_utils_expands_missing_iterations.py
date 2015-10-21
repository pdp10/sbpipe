#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#    
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
#
# Institute for Ageing and Health
# Newcastle University
# Newcastle upon Tyne
# NE4 5PL
# UK
# Tel: +44 (0)191 248 1106
# Fax: +44 (0)191 248 1101
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $



# The parameter estimation task in Copasi only reports the function number by which
# the Squared Mean Error is decreased. This script add also the other values so it 
# is possible to compare more parameter estimation tasks under the same conditions and 
# test whether or not the model reach a good optima statistically.

# This script only extends the result of the Copasi parameter estimation task. 
# Use the R script to perform statistics and compute plots. (~/phd/project/scripts)

# command:
# ./expands_missing_iterations_par_est.py --with-header Calibration1 calibration/dataset_short/dataset1.csv calibration/dataset/dataset1-extended.csv 


import sys




def main(args):
  
  hearder = args[1]
  error = args[2]
  filenamein = args[3]
  filenameout = args[4]
  
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

  

main(sys.argv[1:])