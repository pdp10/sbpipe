# SBpipe package

[![Anaconda Cloud](https://anaconda.org/pdp10/sbpipe/badges/version.svg)](https://anaconda.org/pdp10/sbpipe) [![LGPLv3 License](http://img.shields.io/badge/license-LGPLv3-blue.svg)](https://www.gnu.org/licenses/lgpl.html) [![Build Status](https://travis-ci.org/pdp10/sbpipe.svg?branch=master)](https://travis-ci.org/pdp10/sbpipe) [![Docs Status](https://readthedocs.org/projects/sbpipe/badge/)](http://sbpipe.readthedocs.io/en/latest/) [![Anaconda-Server Badge](https://anaconda.org/pdp10/sbpipe/badges/platforms.svg)](https://anaconda.org/pdp10/sbpipe) [![Anaconda-Server Badge](https://anaconda.org/pdp10/sbpipe/badges/downloads.svg)](https://anaconda.org/pdp10/sbpipe)
## Introduction
SBpipe is an open source software tool for automating repetitive tasks in model building and simulation. Using basic YAML configuration files, SBpipe builds a sequence of repeated model simulations or parameter estimations, performs analyses from this generated sequence, and finally generates a LaTeX/PDF report. The parameter estimation pipeline offers analyses of parameter profile likelihood and parameter correlation using samples from the computed estimates. Specific pipelines for scanning of one or two model parameters at the same time are also provided. Pipelines can run on multicore computers, Sun Grid Engine (SGE), or Load Sharing Facility (LSF) clusters, speeding up the processes of model building and simulation. If desired, pipelines can also be executed via [Snakemake](https://snakemake.readthedocs.io), a powerful workflow management system. SBpipe can run models implemented in COPASI, Python or coded in any other programming language using Python as a wrapper module. Future support for other software simulators can be dynamically added without affecting the current implementation. 

To install SBpipe, see the documentation: [HTML](http://sbpipe.readthedocs.io/en/latest/) or [PDF](https://media.readthedocs.org/pdf/sbpipe/latest/sbpipe.pdf).

If you only need the R functions used by SBpipe for data analysis, visit the project `SBpiper` on [CRAN](https://cran.r-project.org/package=sbpiper) or [GitHub](https://github.com/pdp10/sbpiper).

**Citation:** Dalle Pezze, P and Le Novère, N. (2017) *BMC Systems Biology* **11**:46. SBpipe: a collection of pipelines for automating repetitive simulation and analysis tasks.
[DOI:10.1186/s12918-017-0423-3](https://doi.org/10.1186/s12918-017-0423-3)


![alt text](https://github.com/pdp10/sbpipe/blob/master/docs/images/sbpipe_workflow.png "SBpipe workflow")


## Issues / Feature requests

SBpipe is a relatively young project and there is a chance that some error occurs. Issues with this package can be
reported using the [mailing list](mailto:sbpipe@googlegroups.com) or the [SBpipe forum](https://groups.google.com/forum/#!forum/sbpipe).

To help us better identify and reproduce your problem, some technical information is needed. These details can be retrieved by
executing the SBpipe command using the `--verbose` option or directly from the SBpipe log files which are stored in `~/.sbpipe/logs/`. Please, provide this information when reporting a bug.

Issues and feature requests can also be notified using the [github issue tracking system](https://github.com/pdp10/sbpipe/issues).

