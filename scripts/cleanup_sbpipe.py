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

import os
import sys

SBPIPE = os.environ["SBPIPE"]
sys.path.insert(0, SBPIPE)

from sbpipe.utils.io import remove_file_silently

def cleanup():
    """
    Clean up the package including the tests.
    """
    # Clean the tests (note cleanup_tests has a main() so it runs when imported.
    import tests.cleanup_tests as cleanup_tests
    cleanup_tests.cleanup_tests()
    from sbpipe.utils.io import files_with_pattern_recur
    # Remove all files with suffix .pyc recursively
    for f in files_with_pattern_recur(SBPIPE, '.pyc'):
        remove_file_silently(f)
    # Remove all temporary files (*~) recursively
    for f in files_with_pattern_recur(SBPIPE, '~'):
        remove_file_silently(f)


def main(argv=None):
    cleanup()


if __name__ == "__main__":
    main()
