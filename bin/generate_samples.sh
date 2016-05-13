#!/bin/bash

samples=100

Rscript ${SB_PIPE_LIB}/R/tc_data_generator.R generate_samples_dataset.csv generate_samples_dataset_output.csv ${samples} true

