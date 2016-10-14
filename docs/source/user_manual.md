# User manual

Copyright © 2015-2018, Piero Dalle Pezze and Nicolas Le Novère.

SB pipe and its documentation are released under the GNU Lesser General Public License v3 (LGPLv3). 
A copy of this license is provided with the package and can also be found here:
[https://www.gnu.org/licenses/lgpl-3.0.txt](https://www.gnu.org/licenses/lgpl-3.0.txt).

Contacts: Dr Piero Dalle Pezze (piero.dallepezze AT babraham.ac.uk) and Dr Nicolas Le Novère (nicolas.lenovere AT babraham.ac.uk)

Affiliation: The Babraham Institute, Cambridge, CB22 3AT, UK

Mailing list: sb_pipe AT googlegroups.com

Forum: [https://groups.google.com/forum/#!forum/sb_pipe](https://groups.google.com/forum/#!forum/sb_pipe)


## Introduction
This package contains a collection of pipelines for dynamic modelling of biological systems. 
It aims to automate common processes and speed up productivity for tasks such as model simulation, 
single and double parameter scan, and parameter estimation. 


### Requirements
In order to use SB pipe, the following software must be installed:

- Copasi 4.16 - [http://copasi.org/](http://copasi.org/)
- Python 2.7+ - [https://www.python.org/](https://www.python.org/)
- R 3.3.0+ - [https://cran.r-project.org/](https://cran.r-project.org/)
- LaTeX 2013 (optional) [https://latex-project.org/ftp.html](https://latex-project.org/ftp.html)

You should also make sure that the following packages are installed in 
your machine: `python-pip`, and (optionally) `texlive-latex-base`.

Before installing SB pipe Python and R dependencies the following 
environment variables must be added to your GNU/Linux $HOME/.bashrc file:

```
# SB_PIPE
export SB_PIPE=/path/to/sb_pipe
export PATH=$PATH:${SB_PIPE}/sb_pipe

# Path to CopasiSE
export PATH=$PATH:/path/to/CopasiSE
```

The .bashrc file can then be reloaded from your shell using the command: 
```
$ source $HOME/.bashrc
```

On Windows platforms, these environment variables are configured as any other 
Windows environment variable.

Now it is the time to install Python and R packages used by SB pipe. Two scripts 
are provided to perform these tasks automatically. 

To install SB pipe Python dependencies, run:
```
cd ${SB_PIPE}/
./install_pydeps.py
```

To install SB pipe R dependencies, run:
```
cd ${SB_PIPE}/
$ R
# Inside R environment, answer 'y' to install packages locally
> source('install_rdeps.r')
```

If R package dependencies must be compiled, it is worth checking that the following additional packages are installed in your machine: `build-essential`, `liblapack-dev`, `libblas-dev`, `libcairo-dev`, `libssl-dev`, `libcurl4-openssl-dev`. After installing these packages, `install_rdeps.r` must be executed again.


### Installation
Run the command inside the sb_pipe folder: 
```
python setup.py install
```
The correct installation of SB pipe and its dependencies can be checked by 
running the following commands inside the SB pipe folder: 
```
cd tests
./test_suite.py
```

## How to use SB pipe

### Preliminary configuration steps

#### Pipelines using Copasi
Before using these pipelines, a Copasi model must be configured as follow using CopasiUI:

**pipeline: simulate**

- Tick the flag _executable_ in the Time Course Task.
- Select a report template for the Time Course Task.
- Save the report in the same folder with the same name as the model but replacing the extension .cps with .csv.

**pipeline: single or double parameter scan**

- Tick the flag _executable_ in the Parameter Scan Task.
- Select a report template for the Parameter Scan Task.
- Save the report in the same folder with the same name as the model but replacing the extension .cps with .csv.

**pipeline: param-estim**

- Tick the flag _executable_ in the Parameter Estimation Task.
- Select the report template for the Parameter Estimation Task.
- Save the report in the same folder with the same name as the model but replacing the extension .cps with .csv.


### Running SB pipe
SB pipe is executed via the command *run_sb_pipe.py*. The syntax for this command and its complete list 
of options can be retrieved by running *run_sb_pipe.py -h*. 

As of Sep 2016 the output is as follows:
```
pdp@ariel:~/sb_pipe$ run_sb_pipe.py -h
Usage: run_sb_pipe.py [OPTION] [FILE]
Pipelines for systems modelling of biological networks.

List of mandatory options:
        -h, --help
                Shows this help.
        -c, --create-project
                Create a project structure using the argument as name.
        -s, --simulate
                Simulate a model.
        -p, --single-param-scan
                Simulate a single parameter scan.
        -d, --double-param-scan
                Simulate a double parameter scan.
        -e, --param-estim
                Generate a parameter fit sequence.
Exit status:
 0  if OK,
 1  if minor problems (e.g., a pipeline did not execute correctly),
 2  if serious trouble (e.g., cannot access command-line argument).

Report bugs to sb_pipe@googlegroups.com
SB pipe home page: <https://pdp10.github.io/sb_pipe>
For complete documentation, see README.md .

```

The first step is to create a new project. This can be done with the command:
```
run_sb_pipe.py --create-project project_name
```

This generates the following structure:
```
project_name/
    | - Data/
    | - Models/
    | - Working_Folder/
```
Models must be stored in the Models/ folder. The folder Data/ is meant for collecting experimental data files and analyses in one place. Once the data files for Copasi (e.g. for parameter estimation) are generated, **it is advised** to move them into the Models/ folder so that the Copasi (.cps) file and its associated experimental data files are stored in the same folder. To run SB pipe, users need to create a configuration file 
for each pipeline they intend to run (see next section). These configuration files should be placed in the Working_Folder/. This folder will eventually contain all the results generated by SB pipe. 


For instance, the pipeline for parameter estimation configured with a certain configuration file can be executed by typing:
```
run_sb_pipe.py -e my_config_file.conf
```


### Pipeline configuration files
Pipelines are configured using files (here called configuration files). These files are INI files and are therefore structured as follows: 
```
[pipeline_name]
option1=value1
option2=value2
...
```

In SB pipe each pipeline executes three tasks: data generation, data analysis, and report generation. Each task depends on the previous one. This choice allows user to analyse the same data without having to generate it every time, or to skip the report generation if not wanted. 
Assuming that the configuration files are placed in the Working_Folder of a certain project, examples are given as follow: 

**Example 1:** configuration file for the pipeline *simulate*
```
[simulate]
# True if data must be generated, False otherwise
generate_data=True
# True if data must be analysed, False otherwise
analyse_data=True
# True if a report must be generated, False otherwise
generate_report=True
# The relative path to the project directory (from Working_Folder)
project_dir=..
# The Copasi model name
model=insulin_receptor_stoch.cps
# The cluster type. pp if the model is run locally, sge/lsf if run on cluster.
cluster=pp
# The number of CPU if pp is used, ignored otherwise
pp_cpus=7
# The number of simulations to perform. n>=1 for stochastic simulations.
runs=40
# The label for the x axis.
xaxis_label=Time [min]
# The label for the y axis.
yaxis_label=Level [a.u.]
```

**Example 2:** configuration file for the pipeline *single_param_scan*
```
[single_param_scan]
generate_data=True
analyse_data=True
generate_report=True
project_dir=..
model=insulin_receptor_inhib_scan_IR_beta.cps
# The variable to scan (as set in Copasi Parameter Scan Task)
scanned_par=IR_beta
# The number of intervals in the simulation
simulate__intervals=100
# The number of simulations to perform for each scan
single_param_scan_simulations_number=1
# True if the variable is only reduced (knock down), False otherwise.
single_param_scan_knock_down_only=True
# True if the scanning represents percent levels.
single_param_scan_percent_levels=True
# The minimum level (as set in Copasi Parameter Scan Task)
min_level=0
# The maximum level (as set in Copasi Parameter Scan Task)
max_level=100
# The number of scans (as set in Copasi Parameter Scan Task)
levels_number=10
# True if plot lines are the same between scans (e.g. full lines, same colour)
homogeneous_lines=False
# The label for the x axis.
xaxis_label=Time [min]
# The label for the y axis.
yaxis_label=Level [a.u.]
```

**Example 3:** configuration file for the pipeline *double_param_scan*
```
[double_param_scan]
generate_data=True
analyse_data=True
generate_report=True
project_dir=..
model=insulin_receptor_inhib_dbl_scan_InsulinPercent__IRbetaPercent.cps
# The 1st variable to scan (as set in Copasi Parameter Scan Task)
scanned_par1=InsulinPercent
# The 2nd variable to scan (as set in Copasi Parameter Scan Task)
scanned_par2=IRbetaPercent
# The length of the simulation (as set in Copasi Time Course Task)
sim_length=10
```

**Example 4:** configuration file for the pipeline *param_estim*
```
[param_estim]
generate_data=True
analyse_data=True
generate_report=True
generate_tarball=True
project_dir=..
model=insulin_receptor_param_estim.cps
cluster=pp
pp_cpus=7
# The parameter estimation round which is used to distinguish 
# phases of parameter estimations when parameters cannot be 
# estimated at the same time
round=1
# The number of parameter estimations 
# (the length of the fit sequence)
runs=250
# The threshold percentage of the best fits to consider
best_fits_percent=75
# The number of available data points
data_point_num=33
# True if 2D all fits plots for 66% confidence levels 
# should be plotted. This can be computationally expensive.
plot_2d_66cl_corr=True
# True if 2D all fits plots for 95% confidence levels 
# should be plotted. This can be computationally expensive.
plot_2d_95cl_corr=True
# True if 2D all fits plots for 99% confidence levels 
# should be plotted. This can be computationally expensive.
plot_2d_99cl_corr=True
# True if parameter values should be plotted in log space.
logspace=True
# True if plot axis labels should be plotted in scientific notation.
scientific_notation=True
```

Additional examples of configuration files can be found in:
```
${SB_PIPE}/tests/insulin_receptor/Working_Folder/ 
```


## Reporting bugs or requesting new features
SB pipe is a relatively young project and there is a chance that some error occurs. 
The following mailing list should be used for general questions: 
```
sb_pipe AT googlegroups.com
```

All the topics discussed in this mailing list are also available at 
the website: 

[https://groups.google.com/forum/#!forum/sb_pipe](https://groups.google.com/forum/#!forum/sb_pipe)


To help us better identify and reproduce your problem, some technical information 
is needed. This detail data can be found in SB pipe log files which are stored in ${HOME}/.sb_pipe/logs/. When using the mailing list above, it would be worth providing 
this extra information.

Issues and feature requests can also be notified using the github issue tracking system 
for SB pipe at the web page: 

[https://github.com/pdp10/sb_pipe/issues](https://github.com/pdp10/sb_pipe/issues).

