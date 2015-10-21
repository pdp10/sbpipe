#!/bin/bash

#source "model.conf"
model=$1

nohup ./run_parallel_copasi.sh . ${model} 89 100 4 &