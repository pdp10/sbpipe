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


import sys
import os
from os.path import isdir, join
import shutil
import glob

SBPIPE = os.environ["SBPIPE"]
sys.path.insert(0, SBPIPE)


def cleanup_tests():
    """
    Clean up the test results.
    """
    testpath = os.path.join(SBPIPE, 'tests')
    projects = [f for f in os.listdir(testpath) if isdir(join(testpath, f))]

    for file in projects:
        modelspath = join(testpath, file, 'Models')
        print("cleaning replicated copasi files...")
        replicated_copasi_files = glob.glob(os.path.join(modelspath, "*[0-9].cps"))
        for f in replicated_copasi_files:
            os.remove(f)

        print("cleaning tmp folder...")
        # print tmppath
        tmppath = join(testpath, file, 'tmp')
        shutil.rmtree(tmppath, ignore_errors=True)

        print("cleaning output files...")
        wfpath = join(testpath, file, 'Working_Folder')

        # Delete tgz files
        wflist = [f for f in os.listdir(wfpath) if f.endswith(".tgz")]
        for f in wflist:
            os.remove(os.path.join(wfpath, f))
        # delete sub-directories
        wflist = [d for d in os.listdir(wfpath) if os.path.isdir(os.path.join(wfpath, d))]
        for d in wflist:
            shutil.rmtree(os.path.join(wfpath, d), ignore_errors=True)


def main(args=None):
    cleanup_tests()


main(sys.argv)
