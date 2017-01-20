#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-11-01 22:14:32 $

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
path, foldername = os.path.split(dir_path)

# dynamically load the module with the same name of this package
for module in os.listdir(os.path.dirname(__file__)):
    if module[:-3] == foldername:
        # print(module[:-3])
        __import__('sbpipe.simul.'+module[:-3], locals(), globals())
    del module
