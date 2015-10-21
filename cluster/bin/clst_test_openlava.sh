#!/bin/bash

# start openlava on the cluster of computers specified in clst_iah_list.txt
# by Piero Dalle Pezze - piero.dallepezze@ncl.ac.uk - (npdp2) - 2013


proc=40
time="20s"

echo; echo "Submit jobs to the normal queue"; echo;
for ((p=0; p<${proc}; p++))
do
  ssh iah-huygens "bsub -q normal sleep ${time}"
done

