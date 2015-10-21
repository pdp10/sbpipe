#!/bin/bash

# Piero Dalle Pezze

# This script executes CopasiSE ntimes. 
# The computation is on an openlava cluster


# the path of the model
PATH=$1
# the model pattern name (e.g. mtor_model_ )
MODEL=$2
# the number of models (e.g. 3 if: mtor_model_1.cps, mtor_model_2.cps, mtor_model_3.cps)
NUM=$3



USAGE="run_concur_copasi_cluster.sh [path] [model_pattern] [n_times]"


echo "$USAGE"
for (( i=1; i<=${NUM}; i+=1 ))
do
  # run copasi on openlava on the cluster
  echo "bsub CopasiSE ${PATH}/${MODEL}${i}.cps"
  bsub -q npdp2_queue CopasiSE "${PATH}/${MODEL}${i}.cps"  
done

