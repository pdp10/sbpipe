#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-27 10:18:32 $


import os, sys
from os import listdir, chdir
from os.path import isdir, isfile, join, abspath
import unittest


SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(SB_PIPE + '/tests/ins_rec_model/Working_Folder/')
from test_insulin_receptor import TestInsulinReceptor

"""
Test runner
"""

def main(args):
  """
  Run a suite of tests
  """
    
  mypath = './'
  modelProjects = [f for f in listdir(mypath) if isdir(join(mypath, f))]


  origWD = os.getcwd() # remember our original working directory

  os.chdir(os.path.join(os.path.abspath(sys.path[0]), './ins_rec_model/Working_Folder'))    
  suite = unittest.TestLoader().loadTestsFromTestCase(TestInsulinReceptor)


  unittest.TextTestRunner(verbosity=2).run(suite)

  os.chdir(origWD) # get back to our original working directory


main(sys.argv)

