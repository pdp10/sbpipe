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
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-11 11:14:32 $

import os


def which(cmd_name):
    """
    Utility equivalent to `which` in GNU/Linux OS.
    :param cmd_name: a command name
    :return: return the command name with absolute path if this exists, or None
    """
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, cmd_name)):
                return os.path.join(path, cmd_name)
    return None


def get_copasi():
    """
    Return CopasiSE with its absolute path if the command exists, or None.
    :return: CopasiSE with absolute path or None.
    """
    return which("CopasiSE")
