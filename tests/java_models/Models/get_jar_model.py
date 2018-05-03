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
import subprocess
import sys
from shutil import copy2, rmtree

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, os.pardir))
sys.path.append(SBPIPE)
from sbpipe.utils.dependencies import which
from sbpipe.utils.io import git_retrieve


def compile_simqueue():
    """
    Compile simqueue
    """
    # let's change directory
    # remember our original working directory
    orig_wd = os.getcwd()
    os.chdir(os.path.join('.', 'simqueue'))
    subprocess.Popen(['mvn', 'package']).communicate()[0]
    print("\n")
    os.chdir(orig_wd)
    copy2(os.path.join('.', 'simqueue', 'target', 'simqueue-devel-jar-with-dependencies.jar'), orig_wd)


def main(args=None):
    if which('git') is None:
        print('Error: git was not found. Quit')
        return
    if which('mvn') is None:
        print('Error: mvn was not found. Quit')
        return
    git_retrieve('https://github.com/pdp10/simqueue.git')
    compile_simqueue()
    print('cleanup!')
    rmtree(os.path.join('.', 'simqueue'), ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv)
