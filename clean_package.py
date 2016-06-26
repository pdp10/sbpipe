#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: clean the package
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-24 13:02:32 $


import sys
import os
import subprocess
SB_PIPE = os.environ["SB_PIPE"]
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + '/utils/python/')
import io_util_functions

def main(args):
   
  # Some cleaning
  # Remove all files with suffix .pyc recursively
  for f in io_util_functions.files_with_pattern_recur('.', '.pyc'):
    os.remove(f)
  # Remove all temporary files (*~) recursively
  for f in io_util_functions.files_with_pattern_recur('.', '~'):
    os.remove(f)
    
   
  # clean the test results
  origWD = os.getcwd() # remember our original working directory

  os.chdir("tests")    # change folder
  process = subprocess.Popen(['python', SB_PIPE+'/tests/clean_tests.py'])
  process.wait() 
  
  process = subprocess.Popen(['pyclean', '.'])
  process.wait()
  
  ### delete this silly file
  if os.path.isfile("ins_rec_model/Working_Folder/Rplots.pdf"):
    os.remove("ins_rec_model/Working_Folder/Rplots.pdf")

  os.chdir(origWD) # get back to our original working directory  


main(sys.argv)
