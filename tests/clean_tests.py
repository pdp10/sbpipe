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

from os import listdir
from os.path import isdir, join
import shutil

mypath = './'
modelProjects = [f for f in listdir(mypath) if isdir(join(mypath, f))]

for file in modelProjects:
  simpath = join(file, 'simulations')
  tmppath = join(file, 'tmp')
#  print simpath
#  print tmppath
  shutil.rmtree(simpath)
  shutil.rmtree(tmppath)  