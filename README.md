# sb_pipe package

Mailing list: sb_pipe AT googlegroups.com

[![Build Status](https://travis-ci.org/pdp10/sb_pipe.svg?branch=master)](https://travis-ci.org/pdp10/sb_pipe)

[![LGPLv3 License](http://img.shields.io/badge/license-LGPLv3-blue.svg)](https://www.gnu.org/licenses/lgpl.html)


## Introduction
This package contains a collection of pipelines for dynamic modelling of biological systems. It aims to automate common processes and speed up productivity for tasks such as model simulation, model single and double perturbation, sensitivity analysis and parameter estimation. 


### Requirements
In order to use sb_pipe, the following software must be installed:
- Copasi 4.16 (model parameter estimation, simulation, analyses)
- Python 2.7.3+ (+dependencies: scipy 0.13.3, numpy 1.8.2, pp 1.6.4)
- R 3.3.1+ (plots + statistics) (+dependencies: ggplot2 2.1.0, gplots 2.11.3, abind 1.4)
- LaTeX 2013 (optional for report generation) (texlive-latex-base)
- **[obsolete]** Matlab-toolbox Potterswheel (for parameter estimation 
using Potterswheel). This pipeline also requires bash, sed, Matlab.


### Environment variables for sb_pipe
The following environmental variables need to be set up:
- export SB_PIPE=/path/to/sb_pipe
- export PATH=$PATH:${SB_PIPE}/sb_pipe


### Installation
Run the command inside the sb_pipe folder: 
```
python setup.py install
```
The correct installation of sb_pipe and its dependencies can be checked by 
running the following commands inside the sb_pipe folder: 
```
cd tests
python test_suite.py
```

## How to use sb_pipe

### Preliminary configuration steps

#### Pipelines using Copasi
Before using these pipelines, a Copasi model must be configured as follows:

##### simulate 
Using CopasiUI:
- Tick the flag _executable_ in the Time Course Task.
- Select a report template for the Time Course Task.
- Save the report with the model name replacing the extension .cps with .csv.

##### single-perturb or double-perturb
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


### Running sb_pipe
The first step is to create a new project. This can be done with 
the command:
```
python run_sb_pipe.py --create-project projectname
```
After creating a project, users need to create a configuration file 
for each task they intend to run. Examples of configuration files can be found in:
```
${SB_PIPE}/tests/insulin_receptor/Working_Folder/ 
```
Users should place their configuration files in the Working_Folder/ of their project. Models must be stored in the Models/ folder, while the any data used by the model must be placed in Data/ folder.
Finally, a pipeline for a certain configuration file can be executed as follows:
```
cd Working_Folder
python run_sb_pipe.py pipeline configuration_file
```
where *pipeline* can be one of the following option: 
- --simulate (-s)
- --single-perturb (-p) 
- --double-perturb (-d)
- --sensitivity (-n)
- --param-estim (-e)

For additional options, run
```
python run_sb_pipe.py --help
```
