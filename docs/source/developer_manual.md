# Developer manual

Mailing list: sbpipe AT googlegroups.com

Forum: [https://groups.google.com/forum/#!forum/sbpipe](https://groups.google.com/forum/#!forum/sbpipe)


## Introduction
This guide is meant for developers and contains guidelines for developing 
this project. 


## Development model
This project follows the Feature-Branching model. Briefly, there are two
main branches: `master` and `develop`. The former contains the history 
of stable releases, the latter contains the history of development. The 
`master` branch contains checkout points for production hotfixes 
or merge points for release-x.x.x branches. The `develop` branch is used 
for feature-bugfix integration and checkout point in development. Nobody 
should directly develop in here.


### Conventions
To manage the project in a more consistent way, here is a list of conventions 
to follow:

- Each new feature is developed in a separate branch forked from *develop*. 
This new branch is called *featureNUMBER*, where *NUMBER* is the number 
of the GitHub Issue discussing that feature. The first line of each 
commit message for this branch should contain the string *Issue #NUMBER* 
at the beginning. Doing so, the commit is automatically recorded by the 
Issue Tracking System for that specific Issue. Note that the sharp (#) 
symbol is required.
- The same for each new bugfix, but in this case the branch name is called 
bugfixNUMBER.
- The same for each new hotfix, but in this case the branch name is called 
hotfixNUMBER and is forked from *master*.


### Work flow
The procedure for checking out a new feature from the `develop` branch 
is: 
```
$ git checkout -b feature10 develop
```
This creates the `feature10` branch off `develop`. This feature10 is 
discussed in *Issue #10* in GitHub.
When you are ready to commit your work, run:
```
$ git commit -am "Issue #10, summary of the changes. Detailed 
description of the changes, if any."
$ git push origin feature10       # sometimes and at the end.
```

As of June 2016, the branches `master` and `develop` are protected and a
status check using Travis-CI must be performed before merging or pushing
into these branches. This automatically forces a merge without 
fast-forward. 
In order to merge **any** new feature, bugfix or simple edits into 
`master` or `develop`, a developer **must** checkout a new branch and, 
once committed and pushed, **merge** it to `master` or `develop` using a
`pull request`. To merge `feature10` to `develop`, the pull request output 
will look like this in GitHub Pull Requests:
```
base:develop  compare:feature10   Able to merge. These branches can be 
automatically merged.

```
A small discussion about feature10 should also be included to allow 
other users to understand the feature.

Finally delete the branch: 
```
$ git branch -d feature10      # delete the branch feature10 (locally)
```


### New releases
When the `develop` branch includes all the desired feature for a 
release, it is time to checkout this 
branch in a new one called `release-x.x.x`. It is at this stage that a 
version is established. Only bugfixes or hotfixes are applied to this 
branch. When this testing/correction phase is completed, the `master` 
branch will merge with the `release-x.x.x` branch, using the commands 
above.
To record the release add a tag:
```
git tag -a v1.3 -m "PROGRAM_NAME v1.3"
```
To transfer the tag to the remote server:
```
git push origin v1.3   # Note: it goes in a separate 'branch'
```
To see all the releases:
```
git show
```


## Package structure
This section presents the structure of the SBpipe package. The root of 
the project contains general management scripts for installing Python 
and R dependencies (install_pydeps.py and install_rdeps.r), and installing 
SBpipe (setup.py). Additionally, the logging configuration file 
(logging_config.ini) is also at this level.

In order to automatically compile and run the test suite, Travis-CI is 
used and configured accordingly (.travis.yml).

The project is structured as follows: 
```
sbpipe:
  | - docs/
  | - sbpipe/
        | - pl
        | - R
        | - report
        | - simul
        | - utils
  | - scripts/
  | - tests/
```
These folders will be discussed in the next sections. In SBpipe, Python 
is the project main language. Instead, R is essentially used for computing 
statistics (see section configuration file in the user manual) and for 
generating plots. This choice allows users to run these scripts independently 
of SBpipe if needed using an R environment like Rstudio. This can be 
convenient if further data analysis are needed or plots need to be annotated 
or edited.


### docs
The folder `docs/` contains the documentation for this project. The user 
and developer manuals in markdown format are contained in `docs/source`. 
In order to generate the complete documentation for SBpipe, the following 
packages must be installed: 

- python-sphinx
- pandoc
- texlive-fonts-recommended
- texlive-latex-extra

By default the documentation is generated in html and LaTeX/PDF. Instruction 
for generating or cleaning SBpipe documentation are provided below.

To generate the source code documentation:
```
$ cd $SBPIPE/docs
$ ./gen_doc.sh
```

To clean the documentation:
```
$ cd $SBPIPE/docs
$ ./cleanup_doc.sh
```
The complete source code documentation for this project is stored in 
`docs/build/html` (html format) and `docs/build/latex` (LaTeX/PDF format).
A shortcut to the documentation in html format is available at the page 
`docs/index.html`. 


### sbpipe
This folder contains the source code of the project SBpipe. At this 
level a file called `__main__.py` enables users to run SBpipe
programmatically as a Python module via the command:
```
$ python sbpipe
```
Alternatively `sbpipe` can programmatically be imported within a
Python environment as shown below:
```
$ cd $SBPIPE
$ python
# Python environment
>>> from sbpipe import main as sb
>>> sb.sbpipe(simulate="ir_model_det_simul.yaml")
```
The following subsections describe sbpipe subpackages.


#### pl
The subpackage `sbpipe.pl` contains the class `Pipeline` in the file 
`pipeline.py`. This class represents a generic pipeline which is extended 
by SBpipe pipelines. These are organised in the following subpackages:

- `create`: creates a new project
- `ps1`: scan a model parameter, generate plots and report;
- `ps2`: scan two model parameters, generate plots and report;
- `pe`: generate a parameter fit sequence, tables of statistics, plots 
and report;
- `sim`: generate deterministic or stochastic model simulations, plots 
and report.

All these pipelines can be invoked directly via the script 
`$SBPIPE/scripts/sbpipe.py`. Each SBpipe pipeline extends the class
`Pipeline` and therefore must implement the following methods: 
```
# executes a pipeline
def run(self, config_file)

# process the dictionary of the configuration file loaded by Pipeline.load()
def parse(self, config_dict)
```

- The method run() can invoke Pipeline.load() to load the YAML config_file as a dictionary.
Once the configuration is loaded and the parameters are imported, run() executes
the pipeline.
- The method parse() parses the dictionary and collects the values.


#### R
This folder contains a collection of R utility methods for plotting and 
generating statistics. These utilities are used by the pipelines during 
data analysis.


#### report
The subpackage `sbpipe.report` contains Python modules for generating 
LaTeX/PDF reports.


#### simul
The subpackage `sbpipe.simul` contains the class `Simul` in the file 
`simul.py`. This is a generic simulator interface used by the pipelines 
in SBpipe. This mechanism uncouples pipelines from specific simulators 
which can therefore be configured in each pipeline configuration file. 
As of 2016, the following simulators are available in SBpipe:

- `Copasi`, package `sbpipe.simul.copasi`, which implements all the methods 
of the class `Simul`;
- `Python`, package `sbpipe.simul.python`.

Pipelines can dynamically load a simulator via the class method
`Pipeline.get_simul_obj(simulator)`. This method instantiates an 
object of subtype `Simul` by refractoring the simulator name as parameter. 
A simulator class (e.g. `Copasi`) must have the same name of their package 
(e.g. `copasi`) but start with an upper case letter. A simulator class 
must be contained in a file with the same name of their package (e.g. 
`copasi`). Therefore, for each simulator package, exactly one simulator 
class can be instantiated. Simulators can be configured in the 
configuration file using the field `simulator`. 


#### utils
The subpackage `sbpipe.utils` contains a collection of Python utility 
modules which are used by sbpipe. Here are also contained the functions
for running commands in parallel.


### scripts
The folder `scripts` contains the scripts: `cleanup_sbpipe.py` and 
`sbpipe.py`. `sbpipe.py` is the main script and is used to run
the pipelines. `cleanup_sbpipe.py` is used for cleaning the package 
including the test results. 


### tests
The package `tests` contains the script `test_suite.py` which executes 
all sbpipe tests. It should be used for testing the correct installation 
of SBpipe dependencies as well as reference for configuring a project 
before running any pipeline. Projects inside the folder `$SBPIPE/tests/` 
have the SBpipe project structure:

- `Models`: (e.g. models, Copasi models, Python models, data sets directly used
by Copasi models);
- `Results`: (e.g. pipelines results, etc).

Examples of configuration files (*.yaml) using Copasi can be found in
$SBPIPE/tests/insulin_receptor/.

To run tests for Python models, the Python packages `numpy`, `scipy`, and `pandas` must be installed.
In principle, users may define their Python models using arbitrary packages.

As of 2016, the repository for SBpipe source code is `github.com`. This 
is configured to run Travis-CI every time a `git push` into the repository 
is performed. The exact details of execution of Travis-CI can be found in 
Travis-CI configuration file `$SBPIPE/.travis.yml`. Importantly, Travis-CI 
runs all SBpipe tests using `nosetests`.


## Miscellaneous of useful commands
### Git
**Startup**
```
# clone master
$ git clone https://github.com/pdp10/sbpipe.git
# get develop branch
$ git checkout -b develop origin/develop
# to get all the other branches
$ for b in `git branch -r | grep -v -- '->'`; do git branch 
--track ${b##origin/} $b; done
# to update all the branches with remote
$ git fetch --all
```

**Update**
```
# ONLY use --rebase for private branches. Never use it for shared 
# branches otherwise it breaks the history. --rebase moves your 
# commits ahead. For shared branches, you should use 
# `git fetch && git merge --no-ff`
$ git pull [--rebase] origin BRANCH 
```

**File system**
```
$ git rm [--cache] filename 
$ git add filename
```

**Information**
```
$ git status 
$ git log [--stat]
$ git branch       # list the branches
```

**Maintenance**
```
$ git fsck      # check errors
$ git gc        # clean up
```

**Rename a branch locally and remotely**
```
git branch -m old_branch new_branch         # Rename branch locally
git push origin :old_branch                 # Delete the old branch
git push --set-upstream origin new_branch   # Push the new branch, set 
local branch to track the new remote
```

**Reset**
```
git reset --hard HEAD    # to undo all the local uncommitted changes
```

**Syncing a fork (assuming upstreams are set)**
```
git fetch upstream
git checkout develop
git merge upstream/develop
```
