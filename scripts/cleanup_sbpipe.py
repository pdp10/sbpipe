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
# Object: clean the package
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-24 13:02:32 $


import sys
import os
import subprocess

SBPIPE = os.environ["SBPIPE"]
sys.path.insert(0, SBPIPE)

from sbpipe.utils.io_util_functions import files_with_pattern_recur


def cleanup_sbpipe():
    """
    Clean up the package including the tests.
    """
    # Remove all files with suffix .pyc recursively
    for f in files_with_pattern_recur('.', '.pyc'):
        os.remove(f)
    # Remove all temporary files (*~) recursively
    for f in files_with_pattern_recur('.', '~'):
        os.remove(f)
          
    ### delete this silly file
    if os.path.isfile(os.path.join(SBPIPE,'tests','insulin_receptor','Working_Folder','Rplots.pdf')):
        os.remove(os.path.join(SBPIPE,'tests','insulin_receptor','Working_Folder','Rplots.pdf'))


def main(args):
    # Clean the tests (note cleanup_tests has a main() so it runs when imported.
    from tests.cleanup_tests import cleanup_tests
    # Clean sbpipe
    cleanup_sbpipe()


main(sys.argv)
