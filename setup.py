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
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-26 22:00:32 $
#
#
# To install: 
# $ python setup.py install
#
# To clean:
# $ sudo python setup.py clean --all

from setuptools import setup
import os


def read(filename):
    """
    Utility function to read a file.

    :param filename: the name of the file to read
    :return: the text contained in filename
    """
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='sbpipe',
    packages=['sbpipe'],
    version=read('VERSION'),
    description='Pipelines for systems modelling of biological networks',
    author='Dr Piero Dalle Pezze',
    author_email='piero.dallepezze@babraham.ac.uk',
    requires=['pp'],
    package_data={'sbpipe': ['src/*']},
    scripts=['scripts/sbpipe.py', 'scripts/cleanup_sbpipe.py'],
    url='https://github.com/pdp10/sbpipe',
    download_url='https://pdp10.github.io/sbpipe',
    keywords=['systems biology', 'mathematical modelling', 'copasi', 'pipeline'],
    include_package_data=False,
    license='GNU GPL v3',
    long_description=read('README.md')
)
