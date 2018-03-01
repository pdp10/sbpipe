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

from setuptools import setup, find_packages
import os


def read(filename):
    """
    Utility function to read a file.

    :param filename: the name of the file to read
    :return: the text contained in filename
    """
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sbpipe',
    packages=find_packages(exclude=['docs', 'tests', 'tests.*']),
    version=read('VERSION'),
    description='Pipelines for systems modelling of biological networks',
    author='Dr Piero Dalle Pezze',
    author_email='piero.dallepezze@gmail.com',
    requires=required,
    # These files are searched in any SBpipe python package
    include_package_data=True,
    package_data={'': ['*.r', '*.R']},
    # These files are outside my packages. They also need to be included in MANIFEST.in
    data_files=[('.',['VERSION', 'LICENSE', 'logging_config.ini'])],
    entry_points = {
                   'console_scripts': [
                       'sbpipe = sbpipe.__main__:main'
                   ]
    },
    url='https://github.com/pdp10/sbpipe',
    download_url='https://pdp10.github.io/sbpipe',
    keywords=['systems biology', 'mathematical modelling', 'pipeline'],
    license='LGPL-3.0',
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'],
    test_suite='tests.test_suite',
    zip_safe=False
)
