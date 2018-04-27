Development model
-----------------

This project follows the Feature-Branching model. Briefly, there are two
main branches: ``master`` and ``develop``. The former contains the
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

The script ``release.sh`` at the root of the package allows to release a
new version of SBpipe or update the last github tag. This script also
creates and uploads a new SBpipe package for Anaconda Cloud and pypi.org .

The following two sections describe how to release a new version for
SBpipe, manually.

How to release a new tag
^^^^^^^^^^^^^^^^^^^^^^^^

When the ``develop`` branch includes all the desired feature for a
release, it is time to checkout this branch in a new one called
``release-x.x.x``. It is at this stage that a version is established.

::

    # record the release add a tag:
    git tag -a v1.3 -m "SBpipe v1.3"

    # transfer the tag to the remote server:
    git push origin v1.3   # Note: this goes to a separate 'branch'

    # see all the releases:
    git show

How to release a new SBpipe conda package (Anaconda Cloud)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a short guide for building SBpipe as a conda package. Miniconda
must be installed. In order to proceed, the package ``conda-build`` must
be installed:

::

    conda install conda-build

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
