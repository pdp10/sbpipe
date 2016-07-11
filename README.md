# sb_pipe

Mailing list: sb_pipe AT googlegroups.com

[![Build Status](https://travis-ci.org/pdp10/sb_pipe.svg?branch=master)](https://travis-ci.org/pdp10/sb_pipe)


### Introduction
This package contains a collection of pipelines for dynamic modelling 
of biological systems. It aims to automate common processes and speed up
productivity for tasks such as model simulation, model single and double
perturbation, sensitivity analysis and parameter estimation. 


### Environment Variables
- export SB_PIPE=/path/to/sb_pipe
- export PATH=$PATH:${SB_PIPE}/sb_pipe


### Requirements
- Python (+dependencies: scipy, numpy, pp)
- R (plots + statistics) (+dependencies: ggplot2, gplot, abind, colorspace, 
stringr)
- LaTeX (for report generation) (+dependencies: texlive and recommended 
fonts)
- Copasi (model simulation) - remember to tick the execution check box 
on the task to run
- **[obsolete]** Matlab-toolbox Potterswheel (for parameter estimation 
using Potterswheel). This pipeline also requires bash, sed, Matlab.


### Installation
Run the command: 
```
python setup.py install
```

### Use case
The general structure of a command is: 
```
python run_sb_pipe.py [OPTION] [FILE]
```

In more detail, to create a new project: 
```
python run_sb_pipe.py --create-project projectname
```
After creating a project, the Copasi files should be placed inside 
Models/, whereas the configuration files in Working_Folder/. Examples of
project structures can be found in sb_pipe/tests/. 
A Copasi file must be configured appropriately before starting a 
pipeline. For instance, for simulating a model time course, the Copasi 
Time Course task must be checked as executable (via CopasiUI) and an 
output report must be specified inside the project folder tmp/. The name
of the report must be the name of the Copasi model and this name must
also be included in the configuration file. (See examples in tests/). 

After this preliminary configuration step, the user should move to the 
folder containing the configuration file and start one of the pipelines 
with the command: 
```
python run_sb_pipe.py pipeline configuration_file
```
where *pipeline* can be one of the following option: 
- --simulate
- --single-perturb 
- --double-perturb 
- --sensitivity
- --param-estim 

For additional options, run
```
python run_sb_pipe.py --help
```


### Instructions before running sb_pipe

#### Pipelines using Copasi

##### simulate 
Using CopasiUI:
- Tick the flag _executable_ in the Time Course Task.
- Select a report template for the Time Course Task.
- Save the report with the model name replacing the extension .cps with .csv.

##### single-perturb
Using CopasiUI:
- Tick the flag _executable_ in the Parameter Scan Task.
- Select a report template for the Paramete Scan Task.
- Save the report with the model name replacing the extension .cps with .csv.

##### param-estim
Using CopasiUI:
- Tick the flag _executable_ in the Parameter Estimation Task.
- Select the report template for the Parameter Estimation Task.
- Save the report with the model name replacing the extension .cps with .csv.

##### sensitivity
Using CopasiUI:
- Tick the flag _executable_ in the Sensitivities Task.
- Select the report template for the Sensitivities Task.
- Save the report with the model name replacing the extension .cps with .csv.

Copasi has changed a few times the format for this report. As Sensitivity analysis is not a repetitive task, right now:
- Generate a report for sensitivity analysis. Save this report in PROJECT_FOLDER/simulations/MODEL_NAME/sensitivities/MODEL_NAME_sensitivities.csv
- After running the task, edit the file so that it contains exactly one table.
- Create a configuration file including: 
sensitivities_dir=sensitivities
- The script will generate a plot for each csv file found in the folder `sensitivity`.



### Package Structure


##### sb_pipe
The *sb_pipe/* folder contains the following pipelines:

- *sb_create_project.py* creates a new project
- *sb_simulate.py* simulates a model deterministically or stochastically
using Copasi (this must be configured first), generate plots and report;
- *sb_param_scan__single_perturb.py* runs Copasi (this must be 
configured first), generate plots and report;
- *sb_param_scan__double_perturb.py* runs Copasi (this must be 
configured first), generate plots;
- *sb_param_estim__copasi.py* generate a fits sequence using Copasi 
(this must be configured first), generate tables for statistics;
- *sb_sensitivity.py* runs Copasi (this must be 
configured first), generate plots;
- **[obsolete]** *sb_param_estim__pw.sh* performs parameter estimation 
and MOTA identifiability analysis using the Matlab toolbox Potterswheel.

These pipelines are available as Python functions and are invoked 
directly via *run_sb_pipe.py*.


##### tests
The *tests/* folder contains the script *run_tests.py* to run a test 
suite. It should be used for testing the correct installation of sb_pipe
dependencies as well as reference for configuring a project before 
running any pipeline. The above script is invoked using the 
following commands: 
```
cd tests
python test_suite.py
```
Projects inside the folder tests/ have the sb_pipe project structure: 
- *Data* (e.g. training / testing data sets for the model);
- *Model* (e.g. Copasi or Potterswheel models);
- *Working_Folder* (e.g. pipelines configurations and parameter 
estimation results, time course, parameter scan, sensitivity analysis 
etc).
- *tmp* (e.g. a temporary folder used for pre-processing by sb_pipe).

Examples of configuration files (*.conf) can be found in 
${SB_PIPE}/tests/insulin_receptor/Working_Folder/.

