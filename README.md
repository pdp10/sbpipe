
# sb_pipe

Mailing list: sb_pipe AT googlegroups.com

[![Build Status](https://travis-ci.org/pdp10/SB_pipe.svg?branch=master)](https://travis-ci.org/pdp10/SB_pipe)

[![Code Climate](https://codeclimate.com/github/pdp10/SB_pipe/badges/gpa.svg)](https://codeclimate.com/github/pdp10/SB_pipe)

[![Test Coverage](https://codeclimate.com/github/pdp10/SB_pipe/badges/coverage.svg)](https://codeclimate.com/github/pdp10/SB_pipe/coverage)

[![Issue Count](https://codeclimate.com/github/pdp10/SB_pipe/badges/issue_count.svg)](https://codeclimate.com/github/pdp10/SB_pipe)


### Introduction
This package contains a collection of pipelines for model simulation, 
single parameter perturbation, double parameter perturbation, sensitivity analysis, 
and parameter estimation. It aims to automate common processes and speed up productivity.


### Environment Variables
- export SB_PIPE=/path/to/sb_pipe
- export PATH=$PATH:${SB_PIPE}/sb_pipe


### Requirements
- Python (+dependencies: scipy, numpy, pp)
- R (plots + stats) (+dependencies: gplots, abind, colorspace, stringr)
- LaTeX (for reports) (+dependencies: texlive and recommended fonts)
- Copasi (model simulation) - remember to tick the execution check box on the task to run
- Matlab with Potterswheel (for parameter estimation using Potterswheel), bash, sed, matlab


### Installation
Run the command: 
```
python setup.py install
```

### Use case
Run:
```
python sb_pipe task configuration_file
```
where *task* can be one of the following: 
- create_project
- simulate
- single_perturb 
- double_perturb 
- param_estim 



### Package Structure (in progress)

##### sb_pipe
The *sb_pipe* folder contains the following pipelines:

- *sb_create_project.py* creates a new project
- *sb_simulate.py* simulates a model deterministically or stochastically using Copasi (this must be configured first), generate plots and report;
- *sb_param_scan__single_perturb.py* runs Copasi (this must be configured first), generate plots and report;
- *sb_param_scan__double_perturb.py* runs Copasi (this must be configured first), generate plots;
- *sb_param_estim__copasi.py* generate a fits sequence using Copasi (this must be configured first), generate tables for statistics;
- *sb_param_estim__pw.sh* performs parameter estimation and MOTA identifiability analysis using the Matlab toolbox Potterswheel;

These pipelines are available as python functions and can be invoked directly via *sb_pipe.py*.
Other scripts are also included although not formalised as a pipeline. In the future, it would be nice if the current Matlab code were written in Python, so that sb_pipe only depends on Python/R.

##### cluster
The *cluster* folder contains Bash scripts for copying data within a cluster of computers. It was written for the pipeline *sb_param_estim__pw* and uses OpenLava as cluster manager. Inside there are Bash scripts and configuration files for minimally managing this cluster.

##### tests
The *tests* folder contains the script *run_tests.py* to run tests on a mini-project called *ins_rec_model*. This script is invoked using the following command: 
```
cd tests
python test_suite.py
```
This mini-project has the sb_pipe project structure: 
- *Data* (e.g. training / testing data sets for the model);
- *Model* (e.g. Copasi or Potterswheel models);
- *Working_Folder* (e.g. pipelines configurations and parameter estimation results).
sb_pipe automatically generates other two folders: 
- *simulation* (e.g. time course, parameter scan, sensitivity analysis etc);
- *tmp* (e.g. a temporary folder used for pre-processing by sb_pipe).


### Examples of Configuration file
You can find examples of configuration files (*.conf) in the folder ${SB_PIPE}/tests/ins_rec_model/Working_Folder.
