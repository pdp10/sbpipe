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


import sys
import os
from os.path import isdir, join
import shutil
import glob

testpath = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(testpath, os.pardir))
from sbpipe.utils.io import remove_file_silently


def cleanup_tests():
    """
    Clean up the test results.
    """
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
            snake_files = glob.glob(os.path.join(testpath, file, "*.snake"))
            for f in snake_files:
                remove_file_silently(f)
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
