Installation
------------

Requirements
~~~~~~~~~~~~

In order to use SBpipe, the following packages must be installed:

-  Python 2.7+ or 3.4+ - https://www.python.org/
-  R 3.3.0+ - https://cran.r-project.org/

Please, make sure that `Python pip` and `Rscript` work fine.
SBpipe can work with the simulators:

-  COPASI 4.19+ - http://copasi.org/ (for model simulation, parameter
   scan, and parameter estimation)
-  Python (directly or as a wrapper to call models coded in any
   programming language)

If LaTeX/PDF reports are also desired, the following package must also
be installed:

-  LaTeX 2013+

Installation on GNU/Linux
~~~~~~~~~~~~~~~~~~~~~~~~~

Installation of COPASI
^^^^^^^^^^^^^^^^^^^^^^

As of 2016, COPASI is not available as a package in GNU/Linux
distributions. Users must add the path to COPASI binary files manually
editing the GNU/Linux ``$HOME/.bashrc`` file as follows:

::

    # Path to CopasiSE (update this accordingly)
    export PATH=$PATH:/path/to/CopasiSE/

The correct installation of CopasiSE can be tested with:

::

    # Reload the .bashrc file
    source $HOME/.bashrc

    CopasiSE -h
    > COPASI 4.19 (Build 140)

Installation of LaTeX
^^^^^^^^^^^^^^^^^^^^^

Users are recommended to install LaTeX/texlive using the package manager
of their GNU/Linux distribution. On GNU/Linux Ubuntu machines the
following package is required:

::

    texlive-latex-base

The correct installation of LaTeX can be tested with:

::

    pdflatex -v
    > pdfTeX 3.14159265-2.6-1.40.16 (TeX Live 2015/Debian)
    > kpathsea version 6.2.1
    > Copyright 2015 Peter Breitenlohner (eTeX)/Han The Thanh (pdfTeX).

Installation of SBpipe via Python pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SBpipe and its Python dependencies can simply be installed via
Python pip using the command:

::

    # install sbpipe from pypi.org via pip
    pip install sbpipe

In order to analyse the data, SBpipe requires the R package ``sbpiper``, which
can be installed as follows:

::

    # install sbpiper from r-cran
    Rscript -e "install.packages('sbpiper', dep=TRUE, repos='http://cran.r-project.org')"

Installation of SBpipe via Conda
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users need to download and install Miniconda3 (https://conda.io/miniconda.html).
SBpipe will be installed in a dedicated conda environment:

::

    # create a new environment `sbpipe`
    conda create -n sbpipe

    # activate the environment.
    # For old versions of conda, replace `conda` with `source`.
    conda activate sbpipe

    # install sbpipe and its dependencies (including sbpiper)
    conda install sbpipe -c pdp10 -c conda-forge -c fbergmann -c defaults


Installation of SBpipe from source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users need to install ``git``.

::

    # clone SBpipe from GitHub
    git clone https://github.com/pdp10/sbpipe.git
    # move to sbpipe folder
    cd sbpipe
    # install SBpipe dependencies on GNU/Linux, run:
    make

Finally, to run sbpipe from any shell, users need to add
‘sbpipe/scripts’ to the ``PATH`` environment variable by adding the
following lines to the ``$HOME``/.bashrc file:

::

    # SBPIPE (update this accordingly)
    export PATH=$PATH:/path/to/sbpipe/scripts

The .bashrc file should be reloaded to apply the previous edits:

::

    # Reload the .bashrc file
    source $HOME/.bashrc


Installation on Windows
~~~~~~~~~~~~~~~~~~~~~~~

See installation on GNU/Linux and install SBpipe via PIP or Conda. Windows
users need to install LaTeX MikTeX https://miktex.org/.

Testing SBpipe
~~~~~~~~~~~~~~

The correct installation of SBpipe and its dependencies can be verified
by running the following commands. For the correct execution of all
tests, LaTeX must be installed.

::

    # SBpipe version:
    sbpipe -V
    > sbpipe 4.13.0

Unless SBpipe was installed from source, users need to download the source code
at the page https://github.com/pdp10/sbpipe/releases to run the test suites.

::
    # unzip and change path
    unzip sbpipe-X.Y.Z.zip
    cd sbpipe-X.Y.Z/tests

::

    # run model simulation using COPASI (see results in tests/copasi_models):
    nosetests test_copasi_sim.py --nocapture

::

    # run all tests:
    nosetests test_suite.py --nocapture

::

    # generate the manuscript figures (see results in tests/insulin_receptor):
    nosetests test_suite_manuscript.py --nocapture
