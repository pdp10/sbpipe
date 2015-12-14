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

import subprocess
import os, sys
from os import listdir, chdir
from os.path import isdir, isfile, join, abspath
from sys import path


mypath = './'
modelProjects = [f for f in listdir(mypath) if isdir(join(mypath, f))]


origWD = os.getcwd() # remember our original working directory

for file in modelProjects:
  localpath = join(file, 'Working_Folder')
  if isdir(localpath):
    print file
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), localpath))
    process = subprocess.Popen(['python', 'run_test.py'])
    process.wait() 
    os.chdir(origWD) # get back to our original working directory
