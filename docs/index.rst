.. sbpipe documentation master file, created by
   sphinx-quickstart on Tue Aug 12 15:55:32 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   This file is part of sbpipe.
   sbpipe is free software: you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   sbpipe is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.
   You should have received a copy of the GNU Lesser General Public License
   along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.


SBpipe
======

SBpipe allows mathematical modellers to automatically repeat the tasks of model simulation
and parameter estimation, and extract robustness information from these repeat sequences
in a solid and consistent manner, facilitating model development and analysis.
SBpipe can run models implemented in COPASI, Python or coded in any other programming
language using Python as a wrapper module.
Pipelines can run on multicore computers, Sun Grid Engine (SGE), Load Sharing Facility
(LSF) clusters, or via Snakemake (https://snakemake.readthedocs.io).


**Project info**

Copyright © 2015-2018, Piero Dalle Pezze (piero.dallepezze AT
gmail.com).

License: GNU Lesser General Public License v3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)

Affiliation: The Babraham Institute, Cambridge, CB22 3AT, UK

Mailing list: sbpipe@googlegroups.com

Forum: https://groups.google.com/forum/#!forum/sbpipe

GitHub: https://github.com/pdp10/sbpipe

Citation: Dalle Pezze, P and Le Novère, N. (2017) *BMC Systems Biology*
**11**:46. SBpipe: a collection of pipelines for automating repetitive
simulation and analysis tasks. https://doi.org/10.1186/s12918-017-0423-3


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