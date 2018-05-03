#!/bin/bash
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Piero Dalle Pezze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



# This script releases a new version of SBpipe or update the last github tag.
# This script also creates and uploads a new SBpipe package for anaconda cloud.
#
# Type `release.sh -h` for help.



# This can be `new` or `update`
action=${1}

# This is a string representing the new version (e.g. v4.0.0)
version=${2-null}


if [ "${action}" == "-n" -o "$action" == "--new" ] && [ "$version" != "null" ]
then
    printf "create a new tag\n"

    # We always action from the `master` branch
    printf "checkout master\n"
    git checkout master

    # add a tag
    git tag -a ${version} -m "sbpipe ${version}"
    # transfer the tag to the remote server
    # this goes in a separate 'branch'
    git push origin ${version}


elif [ "${action}" == "-u" -o "$action" == "--update" ] && [ "$version" != "null" ]
then
    printf "update the last tag with current commits\n"

    # We always action from the `master` branch
    printf "checkout master\n"
    git checkout master

    # Update the last tag to include the last commits
    git tag -f -a ${version}
    # push this updated tag
    git push -f --tags origin ${version}


elif [ "${action}" == "-h" -o "${action}" == "--help" ]
then
    printf "\nNAME\n"
    printf "\trelease.sh - A tool for releasing new/updated SBpipe versions"
    printf "\n\nSYNOPSIS\n"
    printf "\trelease.sh [-h] [-n version] [-u version]"
    printf "\n\nDESCRIPTION\n"
    printf "\tThis tool releases a new SBpipe version or update the current tag on github and anaconda cloud.\n"
    printf "\tThe option are as follows:\n"
    printf "\t-n, --new version\t create a new tag called version\n"
    printf "\t-u, --update version\t update the last tag with the current commits and renamed it to version\n"
    printf "\t-h, --help\t\t shows this help\n"
    printf "\n"
    exit 0

else
    echo "ERROR. See: release.sh --help for command syntax\n"
    exit 1
fi



printf "release a new SBpipe package for anaconda cloud\n"
# we upload this new package automatically
conda config --set anaconda_upload yes
# build and upload the package
conda-build conda_recipe/meta.yaml -c pdp10 -c conda-forge -c fbergmann -c defaults

## To test this package locally:
## install
# conda install sbpipe --use-local
## uninstall
# conda remove sbpipe



printf "release a new SBpipe package for pypi.org\n"
# Settings for ~/.pypirc file:
## ~/.pypirc
# [distutils]
# index-servers =
#     pypi
#
# [pypi]
# repository: https://upload.pypi.org/legacy/
# username: pdp10
#
#
# command
python setup.py clean build sdist upload --repository=https://upload.pypi.org/legacy/
