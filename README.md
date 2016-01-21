
# SB_pipe


### Authors
Piero Dalle Pezze (The Babraham Institute, Cambridge, UK)


### Introduction
This package contains a collection of pipelines for model simulation, single parameter perturbation, double parameter perturbation, and sensitivity analysis, and parameter estimation. The aims are to automate common processes and speed up productivity.


### Environment Variables
- export SB_PIPE=/path/to/SB_pipe
- export SB_PIPE_LIB=${SB_PIPE}/lib
- export PATH=$PATH:${SB_PIPE}/bin


### Requirements
- Bash (script management)
- R (plot generation), gplots, abind, colorspace
- Python (report generation)
- LaTeX (for report generation) (On GNU/Linux Kubuntu 14.04, install package texlive)
- Matlab with Potterswheel (for parameter estimation)
- Copasi (model simulation) - remember to tick the execution check box on the task to run


### Package Structure (in progress)

##### bin
The *bin* folder contains the following pipelines: 
- *sb_simulate* simulates a model deterministically or stochastically using Copasi (this must be configured first), generate plots and report;
- *sb_param_scan__single_perturb* runs Copasi (this must be configured first), generate plots and report;
- *sb_param_scan__double_perturb* runs Copasi (this must be configured first), generate plots;
- *sb_param_estim__pw* performs parameter estimation and MOTA identifiability analysis using the Matlab toolbox Potterswheel;
Other scripts are also included although not formalised as a pipeline. These need some work.

##### cluster
The *cluster* folder contains Bash scripts for copying data within a cluster of computers. It was written for the pipeline *sb_param_estim__pw* and uses OpenLava as cluster manager. Inside there are Bash scripts and configuration files for minimally managing this cluster.

##### lib
The *lib* folder contains the routines in Bash, Matlab, Python, and R for running SB_pipe. Currently, Bash is used for linking each pipeline part; Matlab for Potterswheel and model double perturbation; Python for report generation; and R for statistics / plot generation. 
In the future, it would be nice that the current Bash and Matlab code is written in Python, so that SB_pipe only depends on Python/R. ABC-sysbio could replace Potterswheel for parameter estimation.

##### tests
The *tests* folder contains the script *run_tests.py* to run tests on a mini-project called *ins_rec_model*. This script is invoked using the following command: 
```
python run_tests.py
```
This mini-project has the SB_pipe project structure: 
- *Data* (e.g. training / testing data sets for the model);
- *Model* (e.g. Copasi or Potterswheel models);
- *Working_Folder* (e.g. pipelines configurations and parameter estimation results).
SB_pipe automatically generates other two folders: 
- *simulation* (e.g. time course, parameter scan, sensitivity analysis etc);
- *tmp* (e.g. a temporary folder used for pre-processing by SB_pipe).


### Examples of Configuration file
You can find examples of configuration files (*.conf) in the folder ${SB_PIPE}/tests/ins_rec_model/Working_Folder.
