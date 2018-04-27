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
# To install: 
# $ python setup.py install
#
# To clean:
# $ sudo python setup.py clean --all

import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools before installing sbpipe.",
          file=sys.stderr)
    exit(1)


_this_dir = os.path.dirname(__file__)
version = "unknown"
with open(os.path.join(_this_dir, 'sbpipe', 'VERSION')) as in_file:
    version = in_file.read().splitlines()[0]


setup(
    name='sbpipe',
    packages=find_packages(exclude=['docs', 'tests']),
    version=version,
    description='Pipelines for systems modelling of biological networks.',
    long_description=('SBpipe allows mathematical modellers to automatically repeat '
                      'the tasks of model simulation and parameter estimation, and '
                      'extract robustness information from these repeat sequences in '
                      'a solid and consistent manner, facilitating model development '
                      'and analysis. SBpipe can run models implemented in COPASI, Python '
                      'or coded in any other programming language using Python as a '
                      'wrapper module. Pipelines can run on multicore computers, '
                      'Sun Grid Engine (SGE), Load Sharing Facility (LSF) clusters, '
                      'or via Snakemake.'),
    author='Piero Dalle Pezze',
    author_email='piero.dallepezze@gmail.com',
    install_requires=[
        'pyyaml',
        'colorlog',
    ],
    # These files are searched in any SBpipe python package
    include_package_data=True,
    package_data={'': ['*.md', '*.rst', '*.txt', '*.snake',
                       'Makefile', 'LICENSE'],
                  'sbpipe': ['logging_config.ini', 'VERSION']},
    entry_points={
                  'console_scripts': [
                      'sbpipe = sbpipe.__main__:main'
                  ]
    },
    url='http://sbpipe.readthedocs.io',
    download_url='https://github.com/pdp10/sbpipe',
    keywords=['systems biology', 'mathematical modelling', 'pipeline'],
    license='LGPL-3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
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
