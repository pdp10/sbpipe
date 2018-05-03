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
#
#
#
# # To install/clean:
# $ python setup.py install --user
# $ sudo python setup.py clean --all
#
# # or using Python pip:
# $ pip install . --user
# $ pip uninstall sbpipe

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools before installing sbpipe.")
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
                       'Makefile', 'LICENSE', 'CHANGELOG'],
                  'sbpipe': ['logging_config.ini', 'VERSION', 'is_package_installed.r']},
    entry_points={
                  'console_scripts': [
                      'sbpipe = sbpipe:main',
                      'sbpipe_move_datasets = sbpipe.sbpipe_move_datasets:main'
                  ]
    },
    url='http://sbpipe.readthedocs.io',
    download_url='https://github.com/pdp10/sbpipe',
    keywords=['simulation', 'parameter-estimation', 'modelling', 'pipeline'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'],
    zip_safe=False
)
