# SBpipe package

[![Build Status](https://travis-ci.org/pdp10/sbpipe.svg?branch=master)](https://travis-ci.org/pdp10/sbpipe) [![Docs Status](https://readthedocs.org/projects/sbpipe/badge/)](http://sbpipe.readthedocs.io/en/latest/) [![LGPLv3 License](http://img.shields.io/badge/license-LGPLv3-blue.svg)](https://www.gnu.org/licenses/lgpl.html) [![PyPI version](https://badge.fury.io/py/sbpipe.svg)](https://badge.fury.io/py/sbpipe) [![Anaconda Cloud](https://anaconda.org/pdp10/sbpipe/badges/version.svg)](https://anaconda.org/pdp10/sbpipe) [![Anaconda-Server Badge](https://anaconda.org/pdp10/sbpipe/badges/platforms.svg)](https://anaconda.org/pdp10/sbpipe) [![Anaconda-Server Badge](https://anaconda.org/pdp10/sbpipe/badges/downloads.svg)](https://anaconda.org/pdp10/sbpipe)
## Introduction
SBpipe is an open source software tool for automating repetitive tasks in model building and simulation. Using basic YAML configuration files, SBpipe builds a sequence of repeated model simulations or parameter estimations, performs analyses from this generated sequence, and finally generates a LaTeX/PDF report. The parameter estimation pipeline offers analyses of parameter profile likelihood and parameter correlation using samples from the computed estimates. Specific pipelines for scanning of one or two model parameters at the same time are also provided. Pipelines can run on multicore computers, Sun Grid Engine (SGE), or Load Sharing Facility (LSF) clusters, speeding up the processes of model building and simulation. If desired, pipelines can also be executed via [Snakemake](https://snakemake.readthedocs.io), a powerful workflow management system. SBpipe can run models implemented in COPASI, Python or coded in any other programming language using Python as a wrapper module. Future support for other software simulators can be dynamically added without affecting the current implementation. 

To install SBpipe, see the documentation: [HTML](http://sbpipe.readthedocs.io/en/latest/) or [PDF](https://media.readthedocs.org/pdf/sbpipe/latest/sbpipe.pdf).

If you only need the R functions used by SBpipe for data analysis, visit the project `SBpiper` on [CRAN](https://cran.r-project.org/package=sbpiper) or [GitHub](https://github.com/pdp10/sbpiper).

**Citation:** Dalle Pezze P, Le Novère N. SBpipe: a collection of pipelines for automating repetitive
simulation and analysis tasks. *BMC Systems Biology*. 2017 Apr;11:46. [DOI:10.1186/s12918-017-0423-3](https://doi.org/10.1186/s12918-017-0423-3)


![alt text](https://github.com/pdp10/sbpipe/blob/master/docs/images/sbpipe_workflow.png "SBpipe workflow")


## Issues / Feature requests

SBpipe is a relatively young project and there is a chance that some
error occurs. Issues and feature requests can be notified using the github issue
tracking system for SBpipe at the web page: [https://github.com/pdp10/sbpipe/issues](https://github.com/pdp10/sbpipe/issues).
To help us better identify and reproduce your problem, some technical
information is needed. This detail data can be found in SBpipe log files
which are stored in ${HOME}/.sbpipe/logs/. When using the mailing list
above, it would be worth providing this extra information.

Please, use the following mailing list for generic questions: [sbpipe@googlegroups.com](mailto:sbpipe@googlegroups.com).
The topics discussed in this mailing list are also available at
the website: [https://groups.google.com/forum/#!forum/sbpipe](https://groups.google.com/forum/#!forum/sbpipe).

