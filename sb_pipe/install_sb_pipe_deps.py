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
# Object: install sb_pipe requirements
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-26 22:18:32 $

import os
import sys

import logging
from logging.config import fileConfig

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))

from install_python_deps import install_python_deps
from install_r_deps import install_r_deps
from sb_config import which




def python_deps(logger):
  logger.debug("Installing Python dependencies...")    
  if which("pip") == None: 
      logger.warn("pip not found. Skipping installation of Python dependencies.")
  else:
      out = install_python_deps(os.path.join(SB_PIPE, 'requirements.txt'))
      logger.debug(out)
      if ' ERROR' in out:
	  logger.error("Some error occurred when installing Python dependencies. "
		       "Please check log files in logs/")  
      else:
	  logger.debug("Python dependencies installed correctly.")  



def r_deps(logger):
  logger.debug("Installing R dependencies...")  
  if which("R") == None: 
      logger.error("R not found. Skipping installation of R dependencies."
	           "sb_pipe will be severely affected due to this.")
  else:
      # TODO these should be placed accessible easily from another file (e.g. dependencies.r)
      rpkgs = ("gplots", "ggplot2")
      if not install_r_deps(rpkgs):
	  logger.error("Some error occurred when installing R dependencies.")  
      else:
	  logger.debug("R dependencies installed correctly.") 
      



def main(argv=None):
  
  # logging settings
  home = os.path.expanduser("~")
  if not os.path.exists(os.path.join(home, '.sb_pipe', 'logs')):
      os.makedirs(os.path.join(home, '.sb_pipe', 'logs'))
  # disable_existing_loggers=False to enable logging for Python third-party packages
  fileConfig(os.path.join(SB_PIPE, 'logging_config.ini'), 
	     defaults={'logfilename': os.path.join(home, '.sb_pipe', 'logs', 'sb_pipe.log')},
	     disable_existing_loggers=False)   
  logger = logging.getLogger('sbpipe')  
  
  
  python_deps(logger)
  r_deps(logger)
  
  
  
if __name__ == "__main__":
    sys.exit(main())    