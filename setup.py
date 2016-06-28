#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
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



# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = 'sb_pipe',
  packages = ['sb_pipe'],
  version = '0.0.7',
  description = 'Pipelines for systems modelling of biological networks',
  author = 'Dr Piero Dalle Pezze',
  requires=['pp','numpy','scipy'],
  package_data={'sb_pipe': ['doc/*.pdf','doc/*.html','*.tgz']},
  author_email = 'piero.dallepezze@babraham.ac.uk',
  url = 'https://github.com/pdp10/sb_pipe',
  download_url = 'http://pdp10.github.io/sb_pipe/',
  keywords = ['systems biology','mathematical modelling','copasi','pipeline'],
  include_package_data=False,
  license='GNU GPL v3',
  long_description=read('README.md')
)

