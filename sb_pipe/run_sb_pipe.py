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
# Object: sb_pipe main 
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-27 10:18:32 $


import os
import sys
import getopt

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE)

# pipelines
import sb_create_project
import sb_simulate
import sb_param_estim__copasi
import sb_param_scan__single_perturb
import sb_sensitivity




def help():
  message = "Usage: python run_sb_pipe.py [OPTION] [FILE]\n"\
	    "Pipelines for systems modelling of biological networks.\n\n"\
	    "List of mandatory options:\n"\
	    "\t-h, --help\n\t\tShows this help.\n"\
	    "\t-c, --create-project\n\t\tCreate a project structure using the argument as name.\n"\
	    "\t-s, --simulate\n\t\tSimulate a model.\n"\
	    "\t-p, --single-perturb\n\t\tSimulate a single parameter perturbation.\n"\
	    "\t-e, --param-estim\n\t\tGenerate a parameter fit sequence.\n"\
	    "\t-n, --sensitivity\n\t\tRun a sensitivity analysis.\n\n"\
	    "Exit status:\n"\
	    " 0  if OK,\n"\
	    " 1  if minor problems (e.g., a pipeline did not execute correctly.\n"\
	    "Please check the configuration file and Copasi file before reporting),\n"\
	    " 2  if serious trouble (e.g., cannot access command-line argument).\n\n"\
	    "Report sb_pipe bugs to sb_pipe@googlegroups.com\n"\
	    "sb_pipe home page: <https://pdp10.github.io/sb_pipe>\n"\
	    "For complete documentation, see README.md .\n"
  return message


def readFileHeader(fname):
  line = ""
  with open(os.path.join(SB_PIPE, fname)) as file:
    line = file.readline().strip() + " "+ file.readline().strip()
  return line
  

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


# NOTE: 
# don't name this file: __init__.py or sb_pipe.py . 
# They both cause a conflict when these are invoked from the tests



"""
The main launcher for sb_pipe.
Usage: python sb_pipe.py sb_simulate model_ins_rec_v1_det_simul.conf 
"""   

def main(argv=None):
  """Main function for sb_pipe."""   
  if argv is None:
      argv = sys.argv
  try:
      try:
	  opts, args = getopt.getopt(argv[1:], "hcspenlv", 
			      ["help", "create-project", "simulate", "single-perturb", "param-estim", "sensitivity", "license", "version"])

	  for opt, arg in opts:
	    
	    if opt in ("-h", "--help"):
	      print(help())
	      return 0
	    
	    if opt in ("-l", "--license"):
	      print(readFileHeader("LICENSE"))
	      return 0
	    
	    if opt in ("-v", "--version"):
	      print(readFileHeader("VERSION"))
	      return 0
	      
	    elif opt in ("-c", "--create-project"):
	      return sb_create_project.main(args[0])
	      
	    elif opt in ("-s", "--simulate"):
	      return sb_simulate.main(args[0])

	    elif opt in ("-p", "--single-perturb"):
	      return sb_param_scan__single_perturb.main(args[0])
	  
	    elif opt in ("-e", "--param-estim"):	  
	      return sb_param_estim__copasi.main(args[0])
	  
	    elif opt in ("-n", "--sensitivity"):	  
	      return sb_sensitivity.main(args[0])
	  
      except getopt.error, msg:
	    raise Usage(msg)

  except Usage, err:
      print >>sys.stderr, err.msg
      print >>sys.stderr, "for help use --help"
      return 2



if __name__ == "__main__":
    sys.exit(main())    
    
    
    