Development model
-----------------

This project follows the Feature-Branching model. Briefly, there are two
main GitHub branches: ``master`` and ``develop``. The former contains the
history of stable releases, the latter contains the history of
development. The ``master`` branch contains checkout points for
production hotfixes or merge points for release-x.x.x branches. The
``develop`` branch is used for feature-bugfix integration and checkout
point in development. Nobody should directly develop in here.

Conventions
~~~~~~~~~~~

To manage the project in a more consistent way, here is a list of
conventions to follow:

-  Each new feature is developed in a separate branch forked from
   *develop*. This new branch is called *featureNUMBER*, where *NUMBER*
   is the number of the GitHub Issue discussing that feature. The first
   line of each commit message for this branch should contain the string
   *Issue #NUMBER* at the beginning. Doing so, the commit is
   automatically recorded by the Issue Tracking System for that specific
   Issue. Note that the sharp (#) symbol is required.
-  The same for each new bugfix, but in this case the branch name is
   called bugfixNUMBER.
-  The same for each new hotfix, but in this case the branch name is
   called hotfixNUMBER and is forked from *master*.

Work flow
~~~~~~~~~

The procedure for checking out a new feature from the ``develop`` branch
is:

::

    git checkout -b feature10 develop

This creates the ``feature10`` branch off ``develop``. This feature10 is
discussed in *Issue #10* in GitHub. When you are ready to commit your
work, run:

::

    git commit -am "Issue #10, summary of the changes. Detailed
    description of the changes, if any."
    git push origin feature10       # sometimes and at the end.

As of June 2016, the branches ``master`` and ``develop`` are protected
and a status check using Travis-CI must be performed before merging or
pushing into these branches. This automatically forces a merge without
fast-forward. In order to merge **any** new feature, bugfix or simple
edits into ``master`` or ``develop``, a developer **must** checkout a
new branch and, once committed and pushed, **merge** it to ``master`` or
``develop`` using a ``pull request``. To merge ``feature10`` to
``develop``, the pull request output will look like this in GitHub Pull
Requests:

::

    base:develop  compare:feature10   Able to merge. These branches can be
    automatically merged.

A small discussion about feature10 should also be included to allow
other users to understand the feature.

Finally delete the branch:

::

    git branch -d feature10      # delete the branch feature10 (locally)

New releases
~~~~~~~~~~~~

The script ``release.sh`` at the root of the package is used to release a
new version of SBpipe on:

- github
- pypi
- anaconda cloud (channel: pdp10)

Conda releases
~~~~~~~~~~~~~~

This is a short guide for building a conda package for SBpipe. Miniconda3
and the conda package ``conda-build`` must be installed:

::

    conda install conda-build

SBpipe is stored in two Anaconda Cloud channels:

- ``pdp10``
- ``bioconda``


SBpipe on pdp10 channel (Anaconda Cloud)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This channel is used for storing the latest release of SBpipe and sbpiper.
It is also used by Travis-CI for continuous integration tests.

::

    # DON'T FORGET TO SET THIS so that your built package is not uploaded automatically
    conda config --set anaconda_upload no

The recipe for SBpipe is already prepared (file: ``meta.yaml``). To
create the conda package for SBpipe:

::

    cd path/to/sbpipe
    conda-build conda_recipe/meta.yaml -c pdp10 -c conda-forge -c fbergmann -c defaults

To test this package locally:

::

    # install
    conda install sbpipe --use-local

    # uninstall
    conda remove sbpipe

To upload the package to Anaconda Cloud repository:

::

    anaconda upload ~/miniconda/conda-bld/noarch/sbpipe-x.x.x-py_y.tar.bz2

To install the package from Anaconda Cloud:

::

    conda install sbpipe -c pdp10 -c conda-forge -c fbergmann -c defaults

How to release SBpipe to bioconda (Anaconda Cloud)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This conda repository is used for storing the stable releases of SBpipe and sbpiper.
More documentation can be found here:

- https://bioconda.github.io/
- https://bioconda.github.io/contribute-a-recipe.html
- https://bioconda.github.io/guidelines.html#guidelines

The first step is to setup a repository forked from bioconda-recipes:

::

    # fork the GitHub repository: https://github.com/bioconda/bioconda-recipes.git

    # clone your forked bioconda-recipes repository
    git clone https://github.com/YOUR_REPOSITORY/bioconda-recipes.git

    # move to the repository
    cd bioconda-recipes

    # create and checkout new branch `sbpipe`
    git checkout -b sbpipe

    # set a new remote upstream repository that will be synced with the fork.
    git remote add upstream https://github.com/bioconda/bioconda-recipes.git

    # synchronise the remote upstream repository with your local forked repository.
    git fetch upstream


Create the recipes for SBpipe and sbpiper:

::

    # assuming your current location is bioconda-recipes/, move to recipes
    cd recipes

    # use conda skeleton to create a recipe for sbpipe.
    # This will create a folder called sbpipe.
    conda skeleton pypi sbpipe

    # use conda skeleton to create a recipe for sbpiper.
    # This will create a folder called r-sbpiper
    conda skeleton cran sbpiper

    ################
    ### At this stage, follow the instructions provided in the above three links. ###
    ################

Finally, the recipes should be committed and pushed. A pull request including these
edits should be created in the repository `bioconda/bioconda-recipes`

::

    git add -u
    git commit -m 'added recipes'
    git push origin sbpipe

