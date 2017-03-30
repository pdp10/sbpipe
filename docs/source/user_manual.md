# User manual

## Metadata

Copyright © 2015-2018, Piero Dalle Pezze and Nicolas Le Novère.

SBpipe and its documentation are released under the GNU Lesser General Public License v3 (LGPLv3).
A copy of this license is provided with the package and can also be found here:
[https://www.gnu.org/licenses/lgpl-3.0.txt](https://www.gnu.org/licenses/lgpl-3.0.txt).

Contacts: Dr Piero Dalle Pezze (piero.dallepezze AT babraham.ac.uk) and 
Dr Nicolas Le Novère (lenov AT babraham.ac.uk)

Affiliation: The Babraham Institute, Cambridge, CB22 3AT, UK

Mailing list: sbpipe AT googlegroups.com

Forum: [https://groups.google.com/forum/#!forum/sbpipe](https://groups.google.com/forum/#!forum/sbpipe)

Citation:

Dalle Pezze, P and Le Novère, N. (2017) SBpipe: a collection of pipelines for automating repetitive simulation and analysis tasks. BioRxiv, February 9, 2017.
doi: https://doi.org/10.1101/107250


## Introduction
This package contains a collection of pipelines for dynamic modelling of 
biological systems. It aims to automate common processes and speed up 
productivity for tasks such as model simulation, single/double parameter 
scan, and parameter estimation. 


### Requirements
In order to use SBpipe, the following software must be installed:

- Python 2.7+ or 3.4+ - [https://www.python.org/](https://www.python.org/)
- R 3.3.0+ - [https://cran.r-project.org/](https://cran.r-project.org/)

SBpipe can work with the following simulators:

- Copasi 4.19+ - [http://copasi.org/](http://copasi.org/) (for model
simulation, parameter scan, and parameter estimation)
- Python (directly or as a wrapper to call models coded in any programming language)


If LaTeX/PDF reports are also desired, the following software must also 
be installed:

- LaTeX 2013



### Installing SBpipe on GNU/Linux

#### Installation of Copasi
As of 2016, Copasi is not available as a package in GNU/Linux distributions. Users must add the path to Copasi
binary files manually editing the GNU/Linux `$HOME/.bashrc` file as follows:

```
# Path to CopasiSE (update this accordingly)
export PATH=$PATH:/path/to/CopasiSE/
```

The correct installation of CopasiSE can be tested with:
```
# Reload the .bashrc file
$ source $HOME/.bashrc

$ CopasiSE -h
COPASI 4.19 (Build 140)
```


#### Installation of LaTeX
If you decide to install SBpipe dependencies using Miniconda or Anaconda 64bit, you can skip this section.
Users are recommended to install LaTeX/texlive using the package manager of their GNU/Linux distribution.
On GNU/Linux Ubuntu machines the following package is required:

```
texlive-latex-base
```

The correct installation of LaTeX can be tested with:
```
$ pdflatex -v
pdfTeX 3.14159265-2.6-1.40.16 (TeX Live 2015/Debian)
kpathsea version 6.2.1
Copyright 2015 Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
```


#### Preparation of SBpipe
SBpipe can be downloaded from the website or cloned using `git`. To run sbpipe from any shell, users
should add 'sbpipe/scripts' to their `PATH` environment variable by adding the following lines
to their `$HOME`/.bashrc file:

```
# SBPIPE (update this accordingly)
export PATH=$PATH:/path/to/sbpipe/scripts
```

Now you should reload the .bashrc file to apply the previous edits:
```
# Reload the .bashrc file
$ source $HOME/.bashrc
```


#### Installation of Python and R packages
Python and R packages required by SBpipe can be installed via Anaconda/Miniconda (recommended) or using the
GNU/Linux distribution package manager. This will be explained in the following two sections.

##### Installation of Python and R dependencies via Anaconda/Miniconda
Users need to download and install Anaconda ([https://www.continuum.io/downloads](https://www.continuum.io/downloads)) or
Miniconda ([https://conda.io/miniconda.html](https://conda.io/miniconda.html)).

From a GNU/Linux shell:
```
cd path/to/sbpipe

# install dependencies into isolated environment using Anaconda/Miniconda
conda env create --name sbpipe --file environment.yaml

# activate environment. The following line can be
# added to the .bashrc file to skip the activation
# of this environment every time SBpipe is used.
source activate sbpipe
```

##### Installation of Python and R dependencies via the distribution package manager
Users can install Python and R using the package manager of their GNU/Linux distribution. Users need to
make sure that the package `python-pip` is installed. In most cases, the installation via the package manager
will automatically configure the correct environment variables.

The correct installation of Python and R can be tested by running the commands:
```
$ python -V
Python 2.7.12
$ pip -V
pip 8.1.2 from /home/ariel/.local/lib/python2.7/site-packages (python 2.7)

$ R --version
R version 3.2.3 (2015-12-10) -- "Wooden Christmas-Tree"
Copyright (C) 2015 The R Foundation for Statistical Computing
Platform: x86_64-pc-linux-gnu (64-bit)
```

Users need to install Python and R dependency packages used by SBpipe. Two scripts are provided to perform
these tasks automatically.

To install SBpipe Python dependencies on GNU/Linux, run:
```
$ cd path/to/sbpipe
$ ./install_pydeps.py
```

To install SBpipe R dependencies on GNU/Linux, run:
```
$ cd path/to/sbpipe
$ R
# Inside R environment, answer 'y' to install packages locally
> source('install_rdeps.r')
```

**NOTE:**
If R package dependencies must be compiled, it is worth checking that the following
additional packages are installed in your machine: `build-essential`,
`liblapack-dev`, `libblas-dev`, `libcairo-dev`, `libssl-dev`,
`libcurl4-openssl-dev`, and `gfortran`.
Other packages might be needed, depending on R dependencies.
After installing these packages, `install_rdeps.r` must be executed again.



### Installing SBpipe on Windows

#### Installation of Copasi and LaTeX
Windows users need to install the Windows versions of Copasi and LaTeX MikTeX [https://miktex.org/](https://miktex.org/).


#### Installation of MINGW
We advise users to install `Git for Windows` [https://git-for-windows.github.io/](https://git-for-windows.github.io/) as
a simple Shell (MINGW) running on Windows. Leave the default setting during installation.


#### Preparation of SBpipe and Copasi with MINGW
Once `Git for Windows` is started, a Shell-like window appears and enables users to run commands.
The first step is to clone SBpipe from GitHub using the command:

```
$ git clone https://github.com/pdp10/sbpipe.git
```

We now need to set up the SBpipe environment variable:
```
$ touch .bashrc
$ wordpad .bashrc
```
A Wordpad window should be visible, loading the file `.bashrc` . The following lines must be copied into this file:

```
#!/bin/bash/

# SBPIPE
export PATH=$PATH:~/sbpipe/scripts

# COPASI (update this accordingly. Use \ to escape spaces)
export PATH=/path/to/copasi/bin/:$PATH

# Optional: activate Anaconda environment for SBpipe automatically
source activate sbpipe
```

Save the file and close wordpad. Now you should reload the .bashrc file to apply the previous changes:
```
# Reload the .bashrc file
$ source $HOME/.bashrc
```


#### Installation of Python and R dependencies via Anaconda/Miniconda
Users need to download and install Anaconda ([https://www.continuum.io/downloads](https://www.continuum.io/downloads)) or
Miniconda ([https://conda.io/miniconda.html](https://conda.io/miniconda.html)).

From a MINGW shell (`Git for Windows`) type:
```
cd path/to/sbpipe

# install dependencies into isolated environment using Anaconda/Miniconda
conda env create --name sbpipe --file environment.yaml

# activate environment. The following line can be added to the .bashrc file to skip the activation
# of this environment every time SBpipe is used.
source activate sbpipe
```


### Complete installation via Anaconda/miniconda
SBpipe can also be installed via Anaconda/miniconda using the command:
```
$ conda install -c pdp10 sbpipe
```
This command will install sbpipe and all its dependencies automatically.


### Check installation of SBpipe
The correct installation of SBpipe and its dependencies can be checked by running the following commands
inside the SBpipe folder:

```
$ sbpipe -V
sbpipe 3.12.0
```

```
$ cd path/to/sbpipe/tests
$ nosetests test_ok_sim.py
```

To run all tests, run the following instead:
```
$ nosetests test_suite.py
```



## How to use SBpipe

### Preliminary configuration steps

#### Pipelines using Copasi
Before using these pipelines, a Copasi model must be configured as follow 
using CopasiUI:

**pipeline: simulation**

- Tick the flag _executable_ in the Time Course Task.
- Select a report template for the Time Course Task.
- Save the report in the same folder with the same name as the model but 
replacing the extension .cps with .csv (extensions .txt, .tsv, or .dat are also accepted by SBpipe).

**pipelines: single or double parameter scan**

- Tick the flag _executable_ in the Parameter Scan Task.
- Select a report template for the Parameter Scan Task.
- Save the report in the same folder with the same name as the model but 
replacing the extension .cps with .csv (extensions .txt, .tsv, or .dat are also accepted by SBpipe)

**pipeline: parameter estimation**

- Tick the flag _executable_ in the Parameter Estimation Task.
- Select the report template for the Parameter Estimation Task.
- Save the report in the same folder with the same name as the model but 
replacing the extension .cps with .csv (extensions .txt, .tsv, or .dat are also accepted by SBpipe)

For tasks such as parameter estimation using Copasi, it is
recommended to move the data set into the folder `Models/` so
that the Copasi model file and its associated experimental data
files are stored in the same folder.


#### Pipelines running Python models

**pipelines: model simulation**

- The model coded in Python must be functional and invokable via _python_ command.
- The program must receive the report file name as input argument (see examples in sbpipe/tests/).
- The program must save the report to file including the _Time_ column. Report fields must be separated by TAB, and row names must be discarded.

**pipeline: parameter estimation**

- The model coded in Python must be functional and invokable via _python_ command.
- The program must receive the report file name as input argument (see examples in sbpipe/tests/).
- The program must save the report to file. This includes the objective value as first column column, and the estimated
 parameters as following columns. Rows are the evaluated functions. Report fields must be separated by TAB, and row
 names must be discarded.

**Python as a wrapper**
Users can use Python as a wrapper to execute models coded in ANY programming language. The following Python model is
essentially a wrapper invoking an R model called `sde_periodic_drift.r`. This Python wrapper and `sde_periodic_drift.r`
are stored in the `Models/` folder. The configuration file calls the Python wrapper. This wrapper code must receive the report
file name as input argument and forward it to the R script. This R script will run a model and store the results in
the received report file name. These data must be stored as described above.

Python wrapper `sde_periodic_drift.py`. This runs `sde_periodic_drift.r`
```
import os
import sys
import subprocess
import shlex

# This is a Python wrapper used to run an R model.
# The R model receives the report_filename as input
# and must add the results to it.

# Retrieve the report file name
report_filename = "sde_periodic_drift.csv"
if len(sys.argv) > 1:
    report_filename = sys.argv[1]

command = 'Rscript --vanilla ' + os.path.join(os.path.dirname(__file__), 'sde_periodic_drift.r') + \
          ' ' + report_filename

# Block until command is finished
subprocess.call(shlex.split(command))
```

Configuration file invoking the Python wrapper `sde_periodic_drift.py`
```
generate_data: True
analyse_data: True
generate_report: True
project_dir: "."
simulator: "Python"
model: "sde_periodic_drift.py"
cluster: "local"
local_cpus: 7
runs: 14
exp_dataset: ""
plot_exp_dataset: False
xaxis_label: "Time"
yaxis_label: "#"
```


### Running SBpipe
SBpipe is executed via the command *sbpipe*. The syntax for this
command and its complete list of options can be retrieved by running *sbpipe -h*.
The first step is to create a new project. This can be done with the
command:
```
$ sbpipe --create-project project_name
```

This generates the following structure:
```
project_name/
    | - Models/
    | - Results/
```
Models must be stored in the Models/ folder. Copasi data sets used by a model
should also be stored in Models. To run SBpipe, users need to create a configuration file
for each pipeline they intend to run (see next section). These configuration 
files should be placed in the root project folder. In Results/ users
will eventually find all the results generated by SBpipe.

For instance, the pipeline for parameter estimation configured with a 
certain configuration file can be executed by typing:
```
$ cd project_name/
$ sbpipe -e my_config_file.yaml
```


### Pipeline configuration files
Pipelines are configured using files (here called configuration files). 
These files are YAML files.
In SBpipe each pipeline executes three tasks: data generation, data
analysis, and report generation. These tasks can be activated in each
configuration files using the options:

- generate_data: True
- analyse_data: True
- generate_report: True

The `generate_data` task runs a simulator accordingly to the options in
the configuration file. Hence, this task collects and organises the reports
generated from the simulator. The `analyse_data` task processes the reports
to generate plots and compute statistics. Finally, the `generate_report`
task generates a LaTeX report containing the computed plots and invokes the
utility `pdflatex` to produce a PDF file. This modularisation allows users
to analyse the same data without having to re-generate it, or to skip the
report generation if not wanted.

Pipelines for parameter estimation or stochastic model simulation can be
computationally intensive. SBpipe allows users to generate simulated data
in parallel using the following options in the pipeline configuration file:

- cluster: "local"
- local_cpus: 7
- runs: 250

The `cluster` option defines whether the simulator should be executed
locally (`local`: Python multiprocessing), or in a computer cluster (`sge`: Sun Grid
Engine (SGE), `lsf`: Load Sharing Facility (LSF)). If `local` is selected, the
`local_cpus` option determines the maximum number of CPUs to be allocated for
local simulations. The `runs` option specifies the number of simulations
(or parameter estimations for the pipeline `param_estim`) to be run.

Assuming that the configuration files are placed in the root directory
of a certain project (e.g. project_name/), examples are given as follow:

**Example 1:** configuration file for the pipeline *simulation*
```
# True if data should be generated, False otherwise
generate_data: True
# True if data should be analysed, False otherwise
analyse_data: True
# True if a report should be generated, False otherwise
generate_report: True
# The relative path to the project directory
project_dir: "."
# The name of the configurator (e.g. Copasi, Rscript, Python, Java)
simulator: "Copasi"
# The model name
model: "insulin_receptor_stoch.cps"
# The cluster type. local if the model is run locally,
# sge/lsf if run on cluster.
cluster: "local"
# The number of CPU if local is used, ignored otherwise
local_cpus: 7
# The number of simulations to perform.
# n>: 1 for stochastic simulations.
runs: 40
# An experimental data set (or blank) to add to the
# simulated plots as additional layer
exp_dataset: "insulin_receptor_dataset.csv"
# True if the experimental data set should be plotted.
plot_exp_dataset: True
# The label for the x axis.
xaxis_label: "Time [min]"
# The label for the y axis.
yaxis_label: "Level [a.u.]"
```

**Example 2:** configuration file for the pipeline *single parameter scan*
```
# True if data should be generated, False otherwise
generate_data: True
# True if data should be analysed, False otherwise
analyse_data: True
# True if a report should be generated, False otherwise
generate_report: True
# The relative path to the project directory
project_dir: "."
# The name of the configurator (e.g. Copasi)
simulator: "Copasi"
# The model name
model: "insulin_receptor_inhib_scan_IR_beta.cps"
# The variable to scan (as set in Copasi Parameter Scan Task)
scanned_par: "IR_beta"
# The cluster type. local if the model is run locally,
# sge/lsf if run on cluster.
cluster: "local"
# The number of CPU if local is used, ignored otherwise
local_cpus: 7
# The number of simulations to perform per run.
# n>: 1 for stochastic simulations.
runs: 1
# The number of intervals in the simulation
simulate__intervals: 100
# True if the variable is only reduced (knock down), False otherwise.
ps1_knock_down_only: True
# True if the scanning represents percent levels.
ps1_percent_levels: True
# The minimum level (as set in Copasi Parameter Scan Task)
min_level: 0
# The maximum level (as set in Copasi Parameter Scan Task)
max_level: 100
# The number of scans (as set in Copasi Parameter Scan Task)
levels_number: 10
# True if plot lines are the same between scans
# (e.g. full lines, same colour)
homogeneous_lines: False
# The label for the x axis.
xaxis_label: "Time [min]"
# The label for the y axis.
yaxis_label: "Level [a.u.]"
```

**Example 3:** configuration file for the pipeline *double parameter scan*
```
# True if data should be generated, False otherwise
generate_data: True
# True if data should be analysed, False otherwise
analyse_data: True
# True if a report should be generated, False otherwise
generate_report: True
# The relative path to the project directory
project_dir: "."
# The name of the configurator (e.g. Copasi)
simulator: "Copasi"
# The model name
model: "insulin_receptor_inhib_dbl_scan_InsulinPercent__IRbetaPercent.cps"
# The 1st variable to scan (as set in Copasi Parameter Scan Task)
scanned_par1: "InsulinPercent"
# The 2nd variable to scan (as set in Copasi Parameter Scan Task)
scanned_par2: "IRbetaPercent"
# The cluster type. local if the model is run locally,
# sge/lsf if run on cluster.
cluster: "local"
# The number of CPU if local is used, ignored otherwise
local_cpus: 7
# The number of simulations to perform.
# n>: 1 for stochastic simulations.
runs: 1
# The simulation length (as set in Copasi Time Course Task)
sim_length: 10
```

**Example 4:** configuration file for the pipeline *parameter estimation*
```
# True if data should be generated, False otherwise
generate_data: True
# True if data should be analysed, False otherwise
analyse_data: True
# True if a report should be generated, False otherwise
generate_report: True
# True if a zipped tarball should be generated, False otherwise
generate_tarball: True
# The relative path to the project directory
project_dir: "."
# The name of the configurator (e.g. Copasi)
simulator: "Copasi"
# The model name
model: "insulin_receptor_param_estim.cps"
# The cluster type. local if the model is run locally,
# sge/lsf if run on cluster.
cluster: "local"
# The number of CPU if local is used, ignored otherwise
local_cpus: 7
# The parameter estimation round which is used to distinguish
# phases of parameter estimations when parameters cannot be
# estimated at the same time
round: 1
# The number of parameter estimations
# (the length of the fit sequence)
runs: 250
# The threshold percentage of the best fits to consider
best_fits_percent: 75
# The number of available data points
data_point_num: 33
# True if 2D all fits plots for 66% confidence levels
# should be plotted. This can be computationally expensive.
plot_2d_66cl_corr: True
# True if 2D all fits plots for 95% confidence levels
# should be plotted. This can be computationally expensive.
plot_2d_95cl_corr: True
# True if 2D all fits plots for 99% confidence levels
# should be plotted. This can be computationally expensive.
plot_2d_99cl_corr: True
# True if parameter values should be plotted in log space.
logspace: True
# True if plot axis labels should be plotted in scientific notation.
scientific_notation: True
```

Additional examples of configuration files can be found in:
```
sbpipe/tests/insulin_receptor/
```


### Running SBpipe using Snakemake (in progress, so expect some changes)
SBpipe can also be executed using [Snakemake](https://snakemake.readthedocs.io). Snakemake offers an infrastructure
for running software pipelines using declarative rules.
The SBpipe pipelines for parameter estimation, single/double parameter scan, and model simulation are also implemented
as snakemake files (which contain the set of rules for each pipeline). These are:

- sbpipe_pe.snake
- sbpipe_ps1.snake
- sbpipe_ps2.snake
- sbpipe_sim.snake

and are stored on the root folder of SBpipe. The advantage of using snakemake as pipeline infrastructure is that it offers
an extended command sets compared to the one provided with the standard sbpipe. For details, run
```
snakemake -h
```
Snakemake also offers a strong support for dependency management at coding level and reentrancy at execution level.
The former is defined as a way to precisely define the dependency order of functions. The latter is the
capacity of a program to continue from the last interrupted task. Benefitting of dependency declaration and
execution reentrancy can be beneficial for running SBpipe on clusters or on the cloud.

Under the current implementation of SBpipe snakefile, the configuration files described above require the additional
field:
```
# The name of the report variables
report_variables: ['IR_beta_pY1146']
```
which contain the names of the variables exported by the simulator. For the parameter estimation pipeline,
`report_variables` will contain the names of the estimated parameters.

For the parameter estimation pipeline, the following option must also be added:
```
# An experimental data set (or blank) to add to the
# simulated plots as additional layer
exp_dataset: "insulin_receptor_dataset.csv"
```

A complete example of configuration file for the parameter estimation pipeline is the following:
```
simulator: "Copasi"
model: "insulin_receptor_param_estim.cps"
round: 1
runs: 4
best_fits_percent: 75
data_point_num: 33
plot_2d_66cl_corr: True
plot_2d_95cl_corr: True
plot_2d_99cl_corr: True
logspace: True
scientific_notation: True
report_variables: ['k1','k2','k3']
exp_dataset: "insulin_receptor_dataset.csv"
```
**NOTE:**
As it can be noticed, a configuration files for SBpipe using snakemake requires less options than the
corresponding configuration file using SBpipe directly. This because Snakemake files is more automated than SBpipe.
Nevertheless, the removal of those additional options is not necessary for running the configuration file using Snakemake.

Examples of configuration files for running SBpipe using Snakemake are in `tests/snakemake`.

Examples of commands running SBpipe pipelines using Snakemake are:

```
# run model simulation
$ snakemake -s path/to/sbpipe/sbpipe_sim.snake --configfile SBPIPE_CONFIG_FILE.yaml --cores 7

# run model parameter estimation using 40 jobs
$ snakemake -s path/to/sbpipe/sbpipe_pe.snake --configfile SBPIPE_CONFIG_FILE.yaml -p -j 40 --verbose --cluster "qsub"

# run model parameter parameter scan using 5 jobs
$ snakemake -s path/to/sbpipe/sbpipe_ps1.snake --configfile SBPIPE_CONFIG_FILE.yaml -p -j 5 --verbose --cluster "bsub"

# run model parameter parameter scan using 5 jobs
$ snakemake -s path/to/sbpipe/sbpipe_ps2.snake --configfile SBPIPE_CONFIG_FILE.yaml -p -j 1 --verbose --cluster "qsub"
```

See `snakemake -h` for a complete list of commands.


## Reporting bugs or requesting new features
SBpipe is a relatively young project and there is a chance that some 
error occurs. The following mailing list should be used for general 
questions: 
```
sbpipe AT googlegroups.com
```

All the topics discussed in this mailing list are also available at 
the website: 

[https://groups.google.com/forum/#!forum/sbpipe](https://groups.google.com/forum/#!forum/sbpipe)


To help us better identify and reproduce your problem, some technical 
information is needed. This detail data can be found in SBpipe log files 
which are stored in ${HOME}/.sbpipe/logs/. When using the mailing list 
above, it would be worth providing this extra information.

Issues and feature requests can also be notified using the github issue 
tracking system for SBpipe at the web page: 

[https://github.com/pdp10/sbpipe/issues](https://github.com/pdp10/sbpipe/issues).

