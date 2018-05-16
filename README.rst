SBpipe package
==============

|Build Status| |Docs Status| |MIT License| |Anaconda Cloud Version| |PyPI version| |CRAN version|

Introduction
------------

SBpipe is an open source software tool for automating repetitive tasks
in model building and simulation. Using basic YAML configuration files,
SBpipe builds a sequence of repeated model simulations or parameter
estimations, performs analyses from this generated sequence, and finally
generates a LaTeX/PDF report. The parameter estimation pipeline offers
analyses of parameter profile likelihood and parameter correlation using
samples from the computed estimates. Specific pipelines for scanning of
one or two model parameters at the same time are also provided.
Pipelines can run on multicore computers, Sun Grid Engine (SGE), or Load
Sharing Facility (LSF) clusters, speeding up the processes of model
building and simulation. If desired, pipelines can also be executed via
`Snakemake`_, a powerful workflow management system. SBpipe can run
models implemented in COPASI, Python or coded in any other programming
language using Python as a wrapper module. Future support for other
software simulators can be dynamically added without affecting the
current implementation.

To install SBpipe, see the documentation: `HTML`_ or `PDF`_.

The R functions used by SBpipe for data analysis can also be retrieved separately
from `CRAN (sbpiper)`_, `bioconda (r-sbpiper)`_, or from `GitHub (sbpiper)`_.

To download the Snakemake workflows for SBpipe, visit the GitHub repository `sbpipe_snake`_.

**Citation:** Dalle Pezze P, Le Novère N. SBpipe: a collection of
pipelines for automating repetitive simulation and analysis tasks. *BMC
Systems Biology*. 2017 Apr;11:46. `DOI:10.1186/s12918-017-0423-3`_

.. figure:: https://github.com/pdp10/sbpipe/blob/master/docs/images/sbpipe_workflow.png
   :alt: SBpipe workflow


Issues / Feature requests
-------------------------

SBpipe is a relatively young project and there is a chance that some
error occurs. Issues and feature requests can be notified using the
github issue tracking system for SBpipe at the web page:
https://github.com/pdp10/sbpipe/issues. To help us better identify and
reproduce your problem, some technical info.

.. _Snakemake: https://snakemake.readthedocs.io
.. _HTML: http://sbpipe.readthedocs.io
.. _PDF: https://media.readthedocs.org/pdf/sbpipe/latest/sbpipe.pdf
.. _`CRAN (sbpiper)`: https://cran.r-project.org/package=sbpiper
.. _`bioconda (r-sbpiper)`: https://anaconda.org/bioconda/r-sbpiper
.. _`GitHub (sbpiper)`: https://github.com/pdp10/sbpiper
.. _sbpipe_snake: https://github.com/pdp10/sbpipe_snake
.. _`DOI:10.1186/s12918-017-0423-3`: https://doi.org/10.1186/s12918-017-0423-3

.. |Build Status| image:: https://travis-ci.org/pdp10/sbpipe.svg?branch=master
   :target: https://travis-ci.org/pdp10/sbpipe
.. |Docs Status| image:: https://readthedocs.org/projects/sbpipe/badge/
   :target: http://sbpipe.readthedocs.io
.. |MIT License| image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |Anaconda Cloud Version| image:: https://anaconda.org/bioconda/sbpipe/badges/version.svg
   :target: https://anaconda.org/bioconda/sbpipe
.. |PyPI version| image:: https://badge.fury.io/py/sbpipe.svg
   :target: https://badge.fury.io/py/sbpipe
.. |CRAN version| image:: https://www.r-pkg.org/badges/version/sbpiper
   :target: https://cran.r-project.org/package=sbpiper
