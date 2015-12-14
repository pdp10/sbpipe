#!/bin/bash

#source "model.conf"
model=$1

nohup ./run_parallel_copasi.sh . ${model} 68 100 8 &
