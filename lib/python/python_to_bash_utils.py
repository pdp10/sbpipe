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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $


# Python to Bash functions

import sys, os, os.path
import shutil
import shlex
from subprocess import * 



# Return the line number (as string) of the first occurrence of pattern in filename
def get_pattern_position(pattern, filename):
  # Older function for this was: output=`grep -n ctrl_str file_in | cut -f 1 -d ":"`
  p1 = Popen(["grep", "-n", pattern, filename], stdout=PIPE) 
  p2 = Popen(["cut", "-f", "1", "-d", ":"], stdin=p1.stdout, stdout=PIPE)
  p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
  return p2.communicate()[0]

