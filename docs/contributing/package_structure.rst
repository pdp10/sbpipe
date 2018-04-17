Package structure
-----------------

This section presents the structure of the SBpipe package. The root of
the project contains general management scripts for installing Python
and R dependencies (install_pydeps.py and install_rdeps.r), and
installing SBpipe (setup.py). Additionally, the logging configuration
file (logging_config.ini) is also at this level.

In order to automatically compile and run the test suite, Travis-CI is
used and configured accordingly (.travis.yml).

The project is structured as follows:

::

    sbpipe:
      | - docs/
      | - sbpipe/
            | - pl
            | - report
            | - simul
            | - tasks
            | - utils
      | - scripts/
      | - tests/

These folders will be discussed in the next sections. In SBpipe, Python
is the project main language, whereas R is used for computing statistics
and for generating plots. This choice allows users to run these scripts
independently of SBpipe if needed using an R environment like Rstudio.
This can be convenient if further data analysis are needed or plots need
to be annotated or edited. The R code for SBpipe is distributed as a
separate R package and installed as a dependency using the provided
script (install_rdeps.r) or conda. The source code for this package can
be found here: https://github.com/pdp10/sbpiper and on CRAN
https://cran.r-project.org/package=sbpiper.

docs
~~~~

The folder ``docs/`` contains the documentation for this project. The
user and developer manuals in markdown format are contained in
``docs/source``. In order to generate the complete documentation for
SBpipe, the following packages must be installed:

-  python-sphinx
-  texlive-fonts-recommended
-  texlive-latex-extra

By default the documentation is generated in LaTeX/PDF. Instruction for
generating or cleaning SBpipe documentation are provided below.

To generate the source code documentation:

::

    cd path/to/sbpipe/docs
    ./create_doc.sh

GitHub and ReadTheDocs.io are automatically configured to build the
documentation in HTML and PDF format at every commit. These are
available at: http://sbpipe.readthedocs.io.

sbpipe
~~~~~~

This folder contains the source code of the project SBpipe. At this
level a file called ``__main__.py`` enables users to run SBpipe
programmatically as a Python module via the command:

::

    python sbpipe

Alternatively ``sbpipe`` can programmatically be imported within a
Python environment as shown below:

::

    cd path/to/sbpipe
    python
    >>> # Python environment
    >>> from sbpipe.main import sbpipe
    >>> sbpipe(simulate="my_model.yaml")

The following subsections describe sbpipe subpackages.

pl
^^

The subpackage ``sbpipe.pl`` contains the class ``Pipeline`` in the file
``pipeline.py``. This class represents a generic pipeline which is
extended by SBpipe pipelines. These are organised in the following
subpackages:

-  ``create``: creates a new project
-  ``ps1``: scan a model parameter, generate plots and report;
-  ``ps2``: scan two model parameters, generate plots and report;
-  ``pe``: generate a parameter fit sequence, tables of statistics,
   plots and report;
-  ``sim``: generate deterministic or stochastic model simulations,
   plots and report.

All these pipelines can be invoked directly via the script
``sbpipe/scripts/sbpipe``. Each SBpipe pipeline extends the class
``Pipeline`` and therefore must implement the following methods:

::

    # executes a pipeline
    def run(self, config_file)

    # process the dictionary of the configuration file loaded by Pipeline.load()
    def parse(self, config_dict)

-  The method run() can invoke Pipeline.load() to load the YAML
   config_file as a dictionary. Once the configuration is loaded and the
   parameters are imported, run() executes the pipeline.
-  The method parse() parses the dictionary and collects the values.

report
^^^^^^

The subpackage ``sbpipe.report`` contains Python modules for generating
LaTeX/PDF reports.

simul
^^^^^

The subpackage ``sbpipe.simul`` contains the class ``Simul`` in the file
``simul.py``. This is a generic simulator interface used by the
pipelines in SBpipe. This mechanism uncouples pipelines from specific
simulators which can therefore be configured in each pipeline
configuration file. As of 2016, the following simulators are available
in SBpipe:

-  ``Copasi``, package ``sbpipe.simul.copasi``, which implements all the
   methods of the class ``Simul``;
-  ``Python``, package ``sbpipe.simul.python``.

Pipelines can dynamically load a simulator via the class method
``Pipeline.get_simul_obj(simulator)``. This method instantiates an
object of subtype ``Simul`` by refractoring the simulator name as
parameter. A simulator class (e.g. ``Copasi``) must have the same name
of their package (e.g. ``copasi``) but start with an upper case letter.
A simulator class must be contained in a file with the same name of
their package (e.g. ``copasi``). Therefore, for each simulator package,
exactly one simulator class can be instantiated. Simulators can be
configured in the configuration file using the field ``simulator``.

tasks
^^^^^

The subpackage ``sbpipe.tasks`` contains the Python scripts to invoke
the single SBpipe tasks. These are invoked by the rules in the SBpipe
snakemake files. These snakemake files are:

-  sbpipe_pe.snake
-  sbpipe_ps1.snake
-  sbpipe_ps2.snake
-  sbpipe_sim.snake

and are stored on the root folder of SBpipe.

utils
^^^^^

The subpackage ``sbpipe.utils`` contains a collection of Python utility
modules which are used by sbpipe. Here are also contained the functions
for running commands in parallel.

scripts
~~~~~~~

The folder ``scripts`` contains the scripts: ``cleanup_sbpipe`` and
``sbpipe``. ``sbpipe`` is the main script and is used to run the
pipelines. ``cleanup_sbpipe.py`` is used for cleaning the package
including the test results.

tests
~~~~~

The package ``tests`` contains the script ``test_suite.py`` which
executes all sbpipe tests. It should be used for testing the correct
installation of SBpipe dependencies as well as reference for configuring
a project before running any pipeline. Projects inside the folder
``sbpipe/tests/`` have the SBpipe project structure:

-  ``Models``: (e.g. models, COPASI models, Python models, data sets
   directly used by Copasi models);
-  ``Results``: (e.g. pipelines results, etc).

Examples of configuration files (``*.yaml``) using COPASI can be found
in ``sbpipe/tests/insulin_receptor/``.

To run tests for Python models, the Python packages ``numpy``,
``scipy``, and ``pandas`` must be installed. In principle, users may
define their Python models using arbitrary packages.

As of 2016, the repository for SBpipe source code is ``github.com``.
This is configured to run Travis-CI every time a ``git push`` into the
repository is performed. The exact details of execution of Travis-CI can
be found in Travis-CI configuration file ``sbpipe/.travis.yml``.
Importantly, Travis-CI runs all SBpipe tests using ``nosetests``.
