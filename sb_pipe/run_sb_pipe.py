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
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "create_project"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "simulate"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "param_estim"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "single_param_scan"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "double_param_scan"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "sensitivity"))

# pipelines
import create_project
import simulate
import param_estim
import single_param_scan
#import double_param_scan
import sensitivity


import logging
from logging.config import fileConfig


def logo():
  """
  Return sb_pipe logo.
  """
  logo = ("\n"
          "                            _             \n"
	  "          /\               (_)            \n"
	  "    ___  / /_        ____    ____  ___    \n"              
	  "   / __\/ __ \      / __ \/\/ __ \/ _ \   \n"      
	  "  _\ \_/ /_/ /     / /_/ / / /_/ /  __/   \n"
	  " \____/\____/     / ____/_/ ____/\____/   \n"
	  "            =====/ /     / /              \n"
	  "                /_/     /_/               \n"
  )
  return logo  


def help():
  """
  Return help message.
  """
  message = (
    "Usage: run_sb_pipe.py [OPTION] [FILE]\n"
    "Pipelines for systems modelling of biological networks.\n\n"
    "List of mandatory options:\n"
    "\t-h, --help\n\t\tShows this help.\n"
    "\t-c, --create-project\n\t\tCreate a project structure using the argument as name.\n"
    "\t-s, --simulate\n\t\tSimulate a model.\n"
    "\t-p, --single-param-scan\n\t\tSimulate a single parameter scan.\n"
    "\t-d, --double-param-scan\n\t\tSimulate a double parameter scan.\n"
    "\t-e, --param-estim\n\t\tGenerate a parameter fit sequence.\n"
    "\t-n, --sensitivity\n\t\tRun a sensitivity analysis.\n\n"
    "Exit status:\n"
    " 0  if OK,\n"
    " 1  if minor problems (e.g., a pipeline did not execute correctly.\n"
    "Please check the configuration file and Copasi file before reporting),\n"
    " 2  if serious trouble (e.g., cannot access command-line argument).\n\n"
    "Report sb_pipe bugs to sb_pipe@googlegroups.com\n"
    "sb_pipe home page: <https://pdp10.github.io/sb_pipe>\n"
    "For complete documentation, see README.md .\n"
  )
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



def main(argv=None):
  """
  The main launcher for sb_pipe.
  """   
  if argv is None:
      argv = sys.argv
      
  # logging settings
  if not os.path.exists(os.path.join(SB_PIPE, 'logs')):
      os.makedirs(os.path.join(SB_PIPE, 'logs'))
  # disable_existing_loggers=False to enable logging for Python third-party packages
  fileConfig(os.path.join(SB_PIPE, 'logging_config.ini'), 
	     defaults={'logfilename': os.path.join(SB_PIPE, 'logs', 'sb_pipe.log')},
	     disable_existing_loggers=False)   
  logger = logging.getLogger('sbpipe')
  
  try:
      try:
	  opts, args = getopt.getopt(argv[1:], 
				      "hcspenlv", 
				    ["help", 
				      "create-project", 
				      "simulate", 
				      "single-param-scan", 
				      "double-param-scan", 
				      "param-estim", 
				      "sensitivity", 
				      "license", 
				      "version"
				    ])
  
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
		return create_project.main(args[0])
		
	      elif opt in ("-s", "--simulate"):
	        print(logo())
		return simulate.main(args[0])

	      elif opt in ("-p", "--single-param-scan"):
	        print(logo())
		return single_param_scan.main(args[0])

	      elif opt in ("-d", "--double-param-scan"):
	        print(logo())
		#return double_param_scan.main(args[0])
		logger.error("Double parameter scan is not yet available! Apologise!")
		return False
	    
	      elif opt in ("-e", "--param-estim"): 
	        print(logo())
		return param_estim.main(args[0])
	    
	      elif opt in ("-n", "--sensitivity"):
	        print(logo())
		return sensitivity.main(args[0])
	    
	
	  print(help())
	  
      except getopt.error, msg:
	    raise Usage(msg)

  except Usage, err:
      print >>sys.stderr, err.msg
      print >>sys.stderr, "for help use -h, --help"
      return 2



if __name__ == "__main__":
    sys.exit(main())    
    
    
    