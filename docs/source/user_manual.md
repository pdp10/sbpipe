# User manual

Copyright © 2015-2018, Piero Dalle Pezze and Nicolas Le Novère.

SBpipe and its documentation are released under the GNU Lesser General 
Public License v3 (LGPLv3). A copy of this license is provided with the 
package and can also be found here:
[https://www.gnu.org/licenses/lgpl-3.0.txt](https://www.gnu.org/licenses/lgpl-3.0.txt).

Contacts: Dr Piero Dalle Pezze (piero.dallepezze AT babraham.ac.uk) and 
Dr Nicolas Le Novère (lenov AT babraham.ac.uk)

Affiliation: The Babraham Institute, Cambridge, CB22 3AT, UK

Mailing list: sbpipe AT googlegroups.com

Forum: [https://groups.google.com/forum/#!forum/sbpipe](https://groups.google.com/forum/#!forum/sbpipe)


## Introduction
This package contains a collection of pipelines for dynamic modelling of 
biological systems. It aims to automate common processes and speed up 
productivity for tasks such as model simulation, single/double parameter 
scan, and parameter estimation. 


### Requirements
In order to use SBpipe, the following software must be installed:

- Python 2.7+ or 3.2+ - [https://www.python.org/](https://www.python.org/)
- R 3.3.0+ - [https://cran.r-project.org/](https://cran.r-project.org/)

SBpipe can work with the following simulators (at least one must be installed):

- Copasi 4.19+ - [http://copasi.org/](http://copasi.org/) (for model
simulation, parameter scan, and parameter estimation)
- Any R / Python / Octave / Java simulator (for model simulation. Users must install the dependencies)


If LaTeX/PDF reports are also desired, the following software must also 
be installed:

- LaTeX 2013

Depending on your operating system, LaTeX can be downloaded at these 
websites: 

- GNU/Linux: [https://latex-project.org/ftp.html](https://latex-project.org/ftp.html)
- Windows: [https://miktex.org/](https://miktex.org/)


#### GNU/Linux
It is advised that users install Python, R and (optionally) LaTeX packages 
using the package manager of their GNU/Linux distribution. Users need to 
make sure that the packages `python-pip` and `texlive-latex-base` (only 
for reports). In most cases, the installation via the package manager 
will automatically configure the correct environment variables. 

If a local installation of Python, R, or LaTeX is needed, users need to 
add the following environment variables to `$PATH` in their `$HOME`/.bashrc 
file as follows:

```
# Path to R
export PATH=$PATH:/path/to/R/binaries/

# Path to Python. Scripts is the folder (if any) containing the Python 
# script `pip`. pip must be available via command line.
export PATH=$PATH:/path/to/Python/:/path/to/Python/Scripts/

# Path to LaTeX
export PATH=$PATH:/path/to/LaTeX/binaries/

```

The correct installation of Python, R, and LaTeX can be tested by running 
the commands: 
```
# If variables were manually exported, reload the .bashrc file
$ source $HOME/.bashrc

$ python -V
Python 2.7.12
$ pip -V
pip 8.1.2 from /home/ariel/.local/lib/python2.7/site-packages (python 2.7)

$ R --version
R version 3.2.3 (2015-12-10) -- "Wooden Christmas-Tree"
Copyright (C) 2015 The R Foundation for Statistical Computing
Platform: x86_64-pc-linux-gnu (64-bit)

$ pdflatex -v
pdfTeX 3.14159265-2.6-1.40.16 (TeX Live 2015/Debian)
kpathsea version 6.2.1
Copyright 2015 Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
```

As of 2016, Copasi is not available as a package in GNU/Linux distributions. 
Users must add the path to Copasi binary files manually editing their 
GNU/Linux `$HOME`/.bashrc file as follows:

```
# Path to CopasiSE
export PATH=$PATH:/path/to/CopasiSE/
```
The correct installation of CopasiSE can be tested by running the command: 
```
# Reload the .bashrc file
$ source $HOME/.bashrc

$ CopasiSE -h
COPASI 4.16 (Build 104)
```

At this stage, Python, R, Copasi, and (optionally) LaTeX should be installed 
correctly. SBpipe requires the configuration of the environment variable 
`$SBPIPE` which must also be added in the `$HOME`/.bashrc file. The 
package also needs to be added to `$PATH`. To do so, users need to add 
the following lines to their `$HOME`/.bashrc file:

```
# SBPIPE
export SBPIPE=/path/to/sbpipe
export PATH=$PATH:$SBPIPE/scripts

```

Now you should reload the .bashrc file to make the previous change effective: 
```
# Reload the .bashrc file
$ source $HOME/.bashrc
```


Before testing the correct installation of SBpipe, users need to install 
Python and R dependency packages used by SBpipe. Two scripts are provided 
to perform these tasks automatically. 

To install SBpipe Python dependencies on GNU/Linux, run:
```
$ cd $SBPIPE/
$ ./install_pydeps.py
```

To install SBpipe R dependencies on GNU/Linux, run:
```
$ cd $SBPIPE/
$ R
# Inside R environment, answer 'y' to install packages locally
> source('install_rdeps.r')
```

If R package dependencies must be compiled, it is worth checking that 
the following additional packages are installed in your machine: 
`build-essential`, `liblapack-dev`, `libblas-dev`, `libcairo-dev`, 
`libssl-dev`, `libcurl4-openssl-dev`, and `gfortran`. After installing 
these packages, `install_rdeps.r` must be executed again.

The correct installation of SBpipe can be tested by running the command: 
```
$ sbpipe.py -v
2.1.0
```


#### Windows
Windows users are also strongly advised to install the package: 

- Cygwin 2.6.0 [https://www.cygwin.com/](https://www.cygwin.com/)

Cygwin offers a GNU/Linux-like shell. This makes the installation of 
dependencies easier as this follows the configuration for GNU/Linux users.

Windows users may need to edit the `PATH` environment variable so that 
the binary files for the previous packages (Copasi, Python, R, and 
(optionally) LaTeX) are correctly found. Specifically for Python, the 
python scripts `pip.py` and `easy_install.py` are located inside the 
folder `Scripts` within the Python root directory. The path to this folder 
must also be added to `PATH`.

Therefore, the following environment variables must also be added:

```
SBPIPE=\path\to\sbpipe
PATH=[previous paths];%SBPIPE%\scripts
```


**NOTE for Cygwin:**
Environment variables can also be configured directly within the .bashrc 
file in cygwin/home/USERNAME/. 
In the beginning of this file, users should place: 

```
# Path to R
export PATH=$PATH:/path/to/R/binaries/

# Path to Python
export PATH=$PATH:/path/to/Python/:/path/to/Python/Scripts/

# Path to LaTeX
export PATH=$PATH:/path/to/LaTeX/binaries/

# Path to CopasiSE
export PATH=$PATH:/path/to/CopasiSE/binaries/

# SBPIPE
export SBPIPE=/path/to/sbpipe
export PATH=$PATH:$SBPIPE/scripts

```

After configuring the environment variables directly or internally in 
Cygwin, the next step is to install Python and R packages used by SBpipe. 
Two scripts are provided to perform these tasks automatically. 

To install SBpipe Python dependencies using Cygwin on Windows, run:
```
$ cd /cygdrive/PATH/TO/SBPIPE/
$ python.exe install_pydeps.py
```

To install SBpipe R dependencies using Cygwin on Windows, run:
```
$ cd /cygdrive/PATH/TO/SBPIPE/
$ R.exe
# Inside R environment, answer 'y' to install packages locally
> source('install_rdeps.r')
```


### Installation
If desired, SBpipe can be installed in your system. To do so, run the 
command inside the sbpipe folder: 
```
$ cd $SBPIPE
$ python setup.py install
```
The correct installation of SBpipe and its dependencies can be checked 
by running the following commands inside the SBpipe folder: 
```
$ cd $SBPIPE/tests
$ ./test_suite.py
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
replacing the extension .cps with .csv.

**pipelines: single or double parameter scan**

- Tick the flag _executable_ in the Parameter Scan Task.
- Select a report template for the Parameter Scan Task.
- Save the report in the same folder with the same name as the model but 
replacing the extension .cps with .csv.

**pipeline: parameter estimation**

- Tick the flag _executable_ in the Parameter Estimation Task.
- Select the report template for the Parameter Estimation Task.
- Save the report in the same folder with the same name as the model but 
replacing the extension .cps with .csv.

For tasks such as parameter estimation using Copasi, it is
recommended to move the data set into the folder `Models/` so
that the Copasi model file and its associated experimental data
files are stored in the same folder.


#### Pipelines using R, Python, Octave, or Java

**pipeline: simulation**

- The program must be a functional and invokable via _Rscript_, _python_, _octave_, or _java -jar_, respectively.
- The Jar file for Java models must include a manifest.mf specifying the main class.
- The program must receive the report file name as input argument (see examples in $SBPIPE/tests/).
- The program must save the report to file including the _Time_ column. Report fields must be separated by TAB, and row names must be discarded.

**pipeline: parameter estimation**

- The program must be a functional and invokable via _Rscript_, _python_, _octave_, or _java -jar_, respectively.
- The Jar file for Java models must include a manifest.mf specifying the main class.
- The program must receive the report file name as input argument (see examples in $SBPIPE/tests/).
- The program must save the report to file. This includes the objective value as first column column, and the estimated
 parameters as following columns. Rows are the evaluated functions. Report fields must be separated by TAB, and row
 names must be discarded.

### Running SBpipe
SBpipe is executed via the command *sbpipe.py*. The syntax for this
command and its complete list 
of options can be retrieved by running *sbpipe.py -h*.

As of Sep 2016 the output is as follows:
```
$ sbpipe.py -h
Usage: sbpipe.py [OPTION] [FILE]
Pipelines for systems modelling of biological networks.

List of mandatory options:
        -h, --help
                Show this help.
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
        -l, --license
                Show the license.
        -v, --version
                Show the version.
Exit status:
 0  if OK,
 1  if minor problems (e.g., a pipeline did not execute correctly),
 2  if serious trouble (e.g., cannot access command-line argument).

Report bugs to sbpipe@googlegroups.com
SBpipe home page: <https://pdp10.github.io/sbpipe>
For complete documentation, see README.md .

```

The first step is to create a new project. This can be done with the 
command:
```
$ sbpipe.py --create-project project_name
```

This generates the following structure:
```
project_name/
    | - Data/
    | - Models/
    | - Working_Folder/
```
Models must be stored in the Models/ folder. The folder Data/ is meant 
for collecting experimental data files and analyses in one place. Regarding 
Copasi, once the data files (e.g. for parameter estimation) are generated, 
**it is advised** to move them into the Models/ folder so that the Copasi 
(.cps) file and its associated experimental data files are stored in the 
same folder. To run SBpipe, users need to create a configuration file 
for each pipeline they intend to run (see next section). These configuration 
files should be placed in the Working_Folder/. This folder will eventually 
contain all the results generated by SBpipe. 

For instance, the pipeline for parameter estimation configured with a 
certain configuration file can be executed by typing:
```
$ cd project_name/Working_Folder/
$ sbpipe.py -e my_config_file.conf
```


### Pipeline configuration files
Pipelines are configured using files (here called configuration files). 
These files are INI files and are therefore structured as follows: 
```
[pipeline_name]
option1=value1
option2=value2
...
```
where `pipeline_name` can be:
- `simulate`, for deterministic or stochastic model simulation;
- `single_param_scan`, for scanning one model parameter;
- `double_param_scan`, for scanning two model parameters;
- `param_estim`, for parameter estimation.

In SBpipe each pipeline executes three tasks: data generation, data 
analysis, and report generation. These tasks can be activated in each
configuration files using the options:

- generate_data=True
- analyse_data=True
- generate_report=True

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

- cluster=pp
- pp_cpus=7
- runs=250

The `cluster` option defines whether the simulator should be executed
locally (`pp`: Python multiprocessing), or in a computer cluster (`sge`: Sun Grid
Engine (SGE), `lsf`: Load Sharing Facility (LSF)). If `pp` is selected, the
`pp_cpus` option determines the maximum number of CPUs to be allocated for
local simulations. The `runs` option specifies the number of simulations
(or parameter estimations for the pipeline `param_estim`) to be run.

Assuming that the configuration files are placed in the Working_Folder 
of a certain project, examples are given as follow: 

**Example 1:** configuration file for the pipeline *simulation*
```
[simulate]
# True if data should be generated, False otherwise
generate_data=True
# True if data should be analysed, False otherwise
analyse_data=True
# True if a report should be generated, False otherwise
generate_report=True
# The relative path to the project directory (from Working_Folder)
project_dir=..
# The name of the configurator (e.g. Copasi, Rscript, Python, Octave, Java)
simulator=Copasi
# The model name
model=insulin_receptor_stoch.cps
# The cluster type. pp if the model is run locally, 
# sge/lsf if run on cluster.
cluster=pp
# The number of CPU if pp is used, ignored otherwise
pp_cpus=7
# The number of simulations to perform. 
# n>=1 for stochastic simulations.
runs=40
# An experimental data set (or blank) to add to the 
# simulated plots as additional layer
exp_dataset=insulin_receptor_dataset.csv
# True if the experimental data set should be plotted.
plot_exp_dataset=True
# The label for the x axis.
xaxis_label=Time [min]
# The label for the y axis.
yaxis_label=Level [a.u.]
```

**Example 2:** configuration file for the pipeline *single parameter scan*
```
[single_param_scan]
# True if data should be generated, False otherwise
generate_data=True
# True if data should be analysed, False otherwise
analyse_data=True
# True if a report should be generated, False otherwise
generate_report=True
# The relative path to the project directory (from Working_Folder)
project_dir=..
# The name of the configurator (e.g. Copasi)
simulator=Copasi
# The model name
model=insulin_receptor_inhib_scan_IR_beta.cps
# The variable to scan (as set in Copasi Parameter Scan Task)
scanned_par=IR_beta
# The cluster type. pp if the model is run locally,
# sge/lsf if run on cluster.
cluster=pp
# The number of CPU if pp is used, ignored otherwise
pp_cpus=7
# The number of simulations to perform per run.
# n>=1 for stochastic simulations.
runs=1
# The number of intervals in the simulation
simulate__intervals=100
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
# True if plot lines are the same between scans
# (e.g. full lines, same colour)
homogeneous_lines=False
# The label for the x axis.
xaxis_label=Time [min]
# The label for the y axis.
yaxis_label=Level [a.u.]
```

**Example 3:** configuration file for the pipeline *double parameter scan*
```
[double_param_scan]
# True if data should be generated, False otherwise
generate_data=True
# True if data should be analysed, False otherwise
analyse_data=True
# True if a report should be generated, False otherwise
generate_report=True
# The relative path to the project directory (from Working_Folder)
project_dir=..
# The name of the configurator (e.g. Copasi)
simulator=Copasi
# The model name
model=insulin_receptor_inhib_dbl_scan_InsulinPercent__IRbetaPercent.cps
# The 1st variable to scan (as set in Copasi Parameter Scan Task)
scanned_par1=InsulinPercent
# The 2nd variable to scan (as set in Copasi Parameter Scan Task)
scanned_par2=IRbetaPercent
# The cluster type. pp if the model is run locally,
# sge/lsf if run on cluster.
cluster=pp
# The number of CPU if pp is used, ignored otherwise
pp_cpus=7
# The number of simulations to perform.
# n>=1 for stochastic simulations.
runs=1
# The simulation length (as set in Copasi Time Course Task)
sim_length=10
```

**Example 4:** configuration file for the pipeline *parameter estimation*
```
[param_estim]
# True if data should be generated, False otherwise
generate_data=True
# True if data should be analysed, False otherwise
analyse_data=True
# True if a report should be generated, False otherwise
generate_report=True
# True if a zipped tarball should be generated, False otherwise
generate_tarball=True
# The relative path to the project directory (from Working_Folder)
project_dir=..
# The name of the configurator (e.g. Copasi, Rscript, Python, Octave, Java)
simulator=Copasi
# The model name
model=insulin_receptor_param_estim.cps
# The cluster type. pp if the model is run locally, 
# sge/lsf if run on cluster.
cluster=pp
# The number of CPU if pp is used, ignored otherwise
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
$SBPIPE/tests/insulin_receptor/Working_Folder/ 
```


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

