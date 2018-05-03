.. sbpipe documentation master file, created by
   sphinx-quickstart on Tue Aug 12 15:55:32 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   Copyright (c) 2018 Piero Dalle Pezze
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:
   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.


SBpipe
======

SBpipe allows mathematical modellers to automatically repeat the tasks of model simulation
and parameter estimation, and extract robustness information from these repeat sequences
in a solid and consistent manner, facilitating model development and analysis.
SBpipe can run models implemented in COPASI, Python or coded in any other programming
language using Python as a wrapper module.
Pipelines can run on multicore computers, Sun Grid Engine (SGE), Load Sharing Facility
(LSF) clusters, or via Snakemake.


**Project info**

Copyright © 2015-2018, Piero Dalle Pezze

Affiliation: The Babraham Institute, Cambridge, CB22 3AT, UK

License: MIT License (https://opensource.org/licenses/MIT)

Home Page: http://sbpipe.readthedocs.io

Anaconda Cloud: https://anaconda.org/pdp10/sbpipe

PyPI: https://pypi.org/project/sbpipe

sbpiper (R dependency for data analysis): https://cran.r-project.org/package=sbpiper

sbpipe_snake (Snakemake workflows for SBpipe): https://github.com/pdp10/sbpipe_snake

Mailing list: sbpipe@googlegroups.com

Forum: https://groups.google.com/forum/#!forum/sbpipe

GitHub (dev): https://github.com/pdp10/sbpipe

Travis-CI (dev): https://travis-ci.org/pdp10/sbpipe

Issues / Feature requests (dev): https://github.com/pdp10/sbpipe/issues

Citation: Dalle Pezze P, Le Novère N. SBpipe: a collection of pipelines for automating repetitive
simulation and analysis tasks. *BMC Systems Biology*. 2017 Apr;11:46. https://doi.org/10.1186/s12918-017-0423-3


.. toctree::
   :caption: Contents
   :name: contents
   :maxdepth: 3


.. toctree::
   :caption: Introduction
   :name: introduction
   :hidden:
   :maxdepth: 3

   project_info/introduction


.. toctree::
   :caption: Getting started
   :name: getting_started
   :hidden:
   :maxdepth: 3

   getting_started/quick_examples
   getting_started/installation
   getting_started/using_sbpipe


.. toctree::
   :caption: Contributing
   :name: contributing
   :hidden:
   :maxdepth: 3

   contributing/reporting_issues
   contributing/package_structure
   contributing/development_model
   contributing/useful_commands


.. toctree::
   :caption: Other info
   :name: other_info
   :hidden:
   :maxdepth: 3

   project_info/license
   project_info/history