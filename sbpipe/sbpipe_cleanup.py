#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import argparse

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)
from sbpipe.utils.io import remove_file_silently


def cleanup():
    """
    Clean-up the package including the tests.
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
    parser = argparse.ArgumentParser(prog='sbpipe_cleanup',
                                     description='SBpipe script to clean-up the package and tests',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''
Report bugs to sbpipe@googlegroups.com
SBpipe home page: <https://github.com/pdp10/sbpipe>
For complete documentation, see http://sbpipe.readthedocs.io .
    ''')

    args = parser.parse_args()
    cleanup()


if __name__ == "__main__":
    main()
