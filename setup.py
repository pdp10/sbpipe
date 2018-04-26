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

_this_dir = os.path.dirname(__file__)
version = open(os.path.join(_this_dir, 'sbpipe', 'VERSION')).read()


setup(
    name='sbpipe',
    packages=find_packages(exclude=['docs']),
    version=version,
    description='Pipelines for systems modelling of biological networks',
    author='Piero Dalle Pezze',
    author_email='piero.dallepezze@gmail.com',
    install_requires=[
        "pyyaml",
        "colorlog",
    ],
    tests_require=['nose'],
    test_suite='tests.test_suite',
    # These files are searched in any SBpipe python package
    include_package_data=True,
    package_data={'': ['*.md', '*.rst', '*.txt', '*.snake',
                       'VERSION', 'LICENSE'],
                  'sbpipe': ['logging_config.ini', 'VERSION']},
    entry_points = {
                   'console_scripts': [
                       'sbpipe = sbpipe.__main__:main'
                   ]
    },
    url='http://sbpipe.readthedocs.io',
    download_url='https://github.com/pdp10/sbpipep',
    keywords=['systems biology', 'mathematical modelling', 'pipeline'],
    license='LGPL-3.0',
    long_description=open(os.path.join(_this_dir, 'README.md')).read(),
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
    zip_safe=False
)
