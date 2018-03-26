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

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(SBPIPE)

from sbpipe.utils.io import remove_file_silently


def cleanup_tests():
    """
    Clean up the test results.
    """
    testpath = os.path.join(SBPIPE, 'tests')
    projects = [f for f in os.listdir(testpath) if isdir(join(testpath, f))]

    print('Cleaning tests:')
    for file in projects:
        if file == '__pycache__':
            shutil.rmtree(os.path.join(testpath, file), ignore_errors=True)
            continue

        print('- ' + file)

        if file == 'snakemake':
            print("cleaning output files...")
            shutil.rmtree(os.path.join(testpath, file, 'Results'), ignore_errors=True)
            shutil.rmtree(os.path.join(testpath, file, 'log'), ignore_errors=True)
            shutil.rmtree(os.path.join(testpath, file, '.snakemake'), ignore_errors=True)
            continue

        modelspath = join(testpath, file, 'Models')
        replicated_files = glob.glob(os.path.join(modelspath, "*[0-9].cps"))
        for f in replicated_files:
            remove_file_silently(f)

        check_files = glob.glob(os.path.join(modelspath, "*_check.txt"))
        for f in check_files:
            remove_file_silently(f)

        wfpath = join(testpath, file, 'Results')
        if file == 'interrupted':
            # We keep the generated data sets for these tests
            results = [os.path.join(dp, f) for dp, dn, filenames in os.walk(wfpath)
                       for f in filenames]
            for f in results:
                if f.find('param_estim_data') == -1:
                    remove_file_silently(f)
            continue
        shutil.rmtree(wfpath, ignore_errors=True)


def main(args=None):
    cleanup_tests()


if __name__ == "__main__":
    main(sys.argv)
