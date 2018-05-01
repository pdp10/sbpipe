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
import subprocess
from shutil import copy2, rmtree

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir, os.pardir))
sys.path.append(SBPIPE)
from sbpipe.sbpipe_config import which
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
    git_retrieve('http://github.com/pdp10/simqueue.git')
    compile_simqueue()
    print('cleanup!')
    rmtree(os.path.join('.', 'simqueue'), ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv)
