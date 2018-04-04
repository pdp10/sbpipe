## Installation

### Requirements
In order to use SBpipe, the following packages must be installed:

- Python 2.7+ or 3.4+ - [https://www.python.org/](https://www.python.org/)
- R 3.3.0+ - [https://cran.r-project.org/](https://cran.r-project.org/)

SBpipe can work with the simulators:

- COPASI 4.19+ - [http://copasi.org/](http://copasi.org/) (for model
simulation, parameter scan, and parameter estimation)
- Python (directly or as a wrapper to call models coded in any programming language)

If LaTeX/PDF reports are also desired, the following package must also
be installed:

- LaTeX 2013+



### Installation on GNU/Linux

#### Install COPASI
As of 2016, COPASI is not available as a package in GNU/Linux distributions. Users must add the path to COPASI
binary files manually editing the GNU/Linux `$HOME/.bashrc` file as follows:

```
# Path to CopasiSE (update this accordingly)
export PATH=$PATH:/path/to/CopasiSE/
```

The correct installation of CopasiSE can be tested with:
```
# Reload the .bashrc file
source $HOME/.bashrc

CopasiSE -h
> COPASI 4.19 (Build 140)
```


#### Install LaTeX
Users are recommended to install LaTeX/texlive using the package manager of their GNU/Linux distribution.
On GNU/Linux Ubuntu machines the following package is required:

```
texlive-latex-base
```

The correct installation of LaTeX can be tested with:
```
pdflatex -v
> pdfTeX 3.14159265-2.6-1.40.16 (TeX Live 2015/Debian)
> kpathsea version 6.2.1
> Copyright 2015 Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).
```

#### Install SBpipe via Miniconda3
Users need to download and install Miniconda3 ([https://conda.io/miniconda.html](https://conda.io/miniconda.html)).

###### **1st Method**
This method creates a new environment and installs SBpipe dependencies in this environment.
SBpipe is installed locally, enabling an easy access to the package documentation and test suite.
```
# download SBpipe
wget https://github.com/pdp10/sbpipe/tarball/master
# or clone it from GitHub
git clone https://github.com/pdp10/sbpipe.git

# move to sbpipe folder
cd path/to/sbpipe

# install the dependencies within an isolated Miniconda3 environment
conda env create --name sbpipe --file environment.yaml

# activate the environment.
# For recent versions of conda, replace `source` with `conda`.
source activate sbpipe
```

To run sbpipe from any shell, users need to add 'sbpipe/scripts' to their `PATH` environment variable by
adding the following lines to their `$HOME`/.bashrc file:
```
# SBPIPE (update accordingly)
export PATH=$PATH:/path/to/sbpipe/scripts
```

The .bashrc file should be reloaded to apply the previous edits:
```
# Reload the .bashrc file
source $HOME/.bashrc
```

###### **2nd Method**
This method installs SBpipe as a conda package in a dedicated conda environment:
```
# create a new environment `sbpipe`
conda create -n sbpipe

# activate the environment.
# For recent versions of conda, replace `source` with `conda`.
source activate sbpipe

# install sbpipe and its dependencies (including sbpiper)
conda install sbpipe -c pdp10 -c conda-forge -c fbergmann -c defaults
```


#### Install SBpipe manually
For this type of installation, SBpipe must be downloaded from the website or cloned using `git`.
```
# download SBpipe
wget https://github.com/pdp10/sbpipe/tarball/master
# or clone it from GitHub
git clone https://github.com/pdp10/sbpipe.git
```
Users need to make sure that the package `python-pip` and `r-base` are installed.
The correct installation of Python and R can be tested by running the commands:
```
python -V
> Python 3.6.4
pip -V
> pip 9.0.1 from /home/ariel/.local/lib/python3.6/site-packages (python 3.6)

R --version
> R version 3.4.1 (2017-06-30) -- "Single Candle"
> Copyright (C) 2017 The R Foundation for Statistical Computing
> Platform: x86_64-pc-linux-gnu (64-bit)
```

The next step is the installation of SBpipe dependencies.
To install Python dependencies on GNU/Linux, run:
```
cd path/to/sbpipe
./install_pydeps.py
```

To install SBpipe R dependencies on GNU/Linux, run:
```
cd path/to/sbpipe
R
>>> # Inside R environment, answer 'y' to install packages locally
>>> source('install_rdeps.r')
```

Finally, to run sbpipe from any shell, users need to add 'sbpipe/scripts' to their `PATH` environment variable by
adding the following lines to their `$HOME`/.bashrc file:
```
# SBPIPE (update this accordingly)
export PATH=$PATH:/path/to/sbpipe/scripts
```

The .bashrc file should be reloaded to apply the previous edits:
```
# Reload the .bashrc file
source $HOME/.bashrc
```


**NOTES:**

1. If R package dependencies must be compiled, it is worth checking that the following
additional packages are installed in your machine: `build-essential`, `liblapack-dev`,
`libblas-dev`, `libcairo-dev`, `libssl-dev`, `libcurl4-openssl-dev`, and `gfortran`.
These can be installed using the package manager coming with your distribution. Other
packages might be needed, depending on R dependencies. After installing these packages,
`install_rdeps.r` must be executed again.
2. If Python bindings for COPASI are installed, SBpipe automatically checks whether the
COPASI model can be loaded and executed, before generating the data. As of January 2018,
this code is released for Python 2.7 and Python 3.6 on the COPASI website and Anaconda Cloud.
The installation of SBpipe via Miniconda3 automatically installs this dependency.


### Installation on Windows

#### Install MINGW
We advise users to install `Git for Windows` [https://git-for-windows.github.io/](https://git-for-windows.github.io/) as
a simple Shell (MINGW) running on Windows. Leave the default setting during installation.

#### Installation of COPASI
Windows users need to install the Windows versions of COPASI from the COPASI website.
Once `Git for Windows` is started, a Shell-like window appears and enables users to run commands.
A .bashrc file must be created and configured:
```
touch .bashrc
wordpad .bashrc
```
A Wordpad window should be visible, loading the file `.bashrc` . The following lines must be
copied into this file:

```
#!/bin/bash/

# COPASI (update this accordingly. Use \ to escape spaces)
export PATH=/path/to/copasi/bin/:$PATH

```

#### Installation of LaTeX
Windows users need to install LaTeX MikTeX [https://miktex.org/](https://miktex.org/).


#### Install SBpipe via Miniconda3
See GNU/Linux.


#### Install SBpipe manually
Start `Git for Windows` and clone SBpipe from GitHub using the command:

```
git clone https://github.com/pdp10/sbpipe.git
```

We now need to set up the path to SBpipe:
```
wordpad .bashrc
```
The following lines must be appended to this file:

```
# SBPIPE
export PATH=$PATH:~/sbpipe/scripts
```

Save the file and close wordpad. Now you should reload the .bashrc file to apply the previous changes:
```
# Reload the .bashrc file
source $HOME/.bashrc
```
Python and R dependencies should be installed as explained in the corresponding section 
for GNU/Linux section.


### Test SBpipe
The correct installation of SBpipe and its dependencies can be verified by running the following commands.
For the correct execution of all tests, LaTeX must be installed.

```
# SBpipe version:
sbpipe -V
> sbpipe 4.6.0
```

```
# run model simulation using COPASI (see results in tests/copasi_models):
cd path/to/sbpipe/tests
nosetests test_copasi_sim.py --nocapture --verbose
```

```
# run all tests:
nosetests test_suite.py --nocapture --verbose
```

```
# generate the manuscript figures (see results in tests/insulin_receptor):
nosetests test_suite_manuscript.py --nocapture --verbose
```
