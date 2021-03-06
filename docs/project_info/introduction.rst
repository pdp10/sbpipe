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
`Snakemake <https://snakemake.readthedocs.io>`__, a powerful workflow
management system. SBpipe can run models implemented in COPASI, Python
or coded in any other programming language using Python as a wrapper
module. Future support for other software simulators can be dynamically
added without affecting the current implementation.
