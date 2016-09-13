# sb_pipe package

Mailing list: sb_pipe AT googlegroups.com

Forum: [https://groups.google.com/forum/#!forum/sb_pipe](https://groups.google.com/forum/#!forum/sb_pipe)

[![Build Status](https://travis-ci.org/pdp10/sb_pipe.svg?branch=master)](https://travis-ci.org/pdp10/sb_pipe)

[![LGPLv3 License](http://img.shields.io/badge/license-LGPLv3-blue.svg)](https://www.gnu.org/licenses/lgpl.html)


## Introduction
This package contains a collection of pipelines for dynamic modelling of biological systems. 
It aims to automate common processes and speed up productivity for tasks such as model simulation, 
model single and double parameter scan, and parameter estimation. 


### Environment variables for sb_pipe
The following environmental variables need to be set up:
- export SB_PIPE=/path/to/sb_pipe
- export PATH=$PATH:${SB_PIPE}/sb_pipe

The path to CopasiSE must be added to the PATH environmental variable
- export PATH=$PATH:/path/to/CopasiSE


### Requirements
Before proceeding, you should make sure that the following packages 
are installed in your machine: `build-essential`, `python-pip`, and 
(optionally) `texlive-latex-base`.

In order to use sb_pipe, the following software must be installed:
- Copasi 4.16 - [http://copasi.org/](http://copasi.org/)
- Python 2.7+ - [https://www.python.org/](https://www.python.org/)
- R 3.3.0+ - [https://cran.r-project.org/](https://cran.r-project.org/)
- LaTeX 2013 (optional) [https://latex-project.org/ftp.html](https://latex-project.org/ftp.html)

Before installing sb_pipe Python and R dependencies, the environment 
variables for sb_pipe need to be configured. 

To install sb_pipe Python dependencies, run:
```
cd ${SB_PIPE}/
./install_pydeps.py
```

To install sb_pipe R dependencies, run:
```
cd ${SB_PIPE}/
$ R
# Inside R environment, answer 'y' to install packages locally
> source('install_rdeps.r')
```
If R package dependencies are to be compiled, it would be worth checking that these additional packages are installed in your machine: `liblapack-dev`, `libblas-dev`, `libcairo-dev`, `libssl-dev`, `libcurl4-openssl-dev`. After installing these packages, `install_rdeps.r` must be executed again.


### Installation
Run the command inside the sb_pipe folder: 
```
python setup.py install
```
The correct installation of sb_pipe and its dependencies can be checked by 
running the following commands inside the sb_pipe folder: 
```
cd tests
./test_suite.py
```

## How to use sb_pipe

### Preliminary configuration steps

#### Pipelines using Copasi
Before using these pipelines, a Copasi model must be configured as follows. Reports must be created in the same folder of the model (Models/). 

##### simulate 
Using CopasiUI:
- Tick the flag _executable_ in the Time Course Task.
- Select a report template for the Time Course Task.
- Save the report with the model name replacing the extension .cps with .csv.

##### single or double parameter scan
Using CopasiUI:
- Tick the flag _executable_ in the Parameter Scan Task.
- Select a report template for the Paramete Scan Task.
- Save the report with the model name replacing the extension .cps with .csv.

##### param-estim
Using CopasiUI:
- Tick the flag _executable_ in the Parameter Estimation Task.
- Select the report template for the Parameter Estimation Task.
- Save the report with the model name replacing the extension .cps with .csv.


### Running sb_pipe
The first step is to create a new project. This can be done with 
the command:
```
run_sb_pipe.py --create-project projectname
```
After creating a project, users need to create a configuration file 
for each task they intend to run. Examples of configuration files can be found in:
```
${SB_PIPE}/tests/insulin_receptor/Working_Folder/ 
```
Users should place their configuration files in the Working_Folder/ of their project. Models must be stored in the Models/ folder. The folder Data/ is meant for collecting experimental data files and analyses in one place. 
Once the data files for Copasi (e.g. for parameter estimation) are generated, **it is advised** to move them into the Models/ folder so that the Copasi (.cps) file and its associated experimental data files are stored in the same folder. 
Finally, a pipeline for a certain configuration file can be executed as follows:
```
cd Working_Folder
run_sb_pipe.py pipeline configuration_file
```
where *pipeline* can be one of the following option: 
- --simulate (-s)
- --single-param-scan (-p) 
- --double-param-scan (-d)
- --param-estim (-e)

For additional options, run
```
run_sb_pipe.py --help
```


### Issue reporting & request for new features
sb_pipe is a relatively young project and there is a chance that some error occurs. If this is the case, 
users should report problems using the following mailing list: 
```
sb_pipe AT googlegroups.com
```
To help us better identify and reproduce your problem, some technical information is needed. This 
detail data can be found in sb_pipe log files which are stored in ${HOME}/.sb_pipe/logs/. When using 
the mailing list above, it would be worth this extra information is also included.

Issues and feature requrests can also be notified using the github issue tracking system for sb_pipe 
at the web page: [https://github.com/pdp10/sb_pipe/issues](https://github.com/pdp10/sb_pipe/issues).
