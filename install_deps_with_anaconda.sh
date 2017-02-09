#!/bin/bash

## clone sbpipe into working directory
# git clone https://github.com/pdp10/sbpipe.git  path/to/workdir
# cd path/to/workdir

# install dependencies into isolated environment using
# anaconda or miniconda
conda env create --name sbpipe --file environment.yaml

# activate environment
source activate sbpipe

