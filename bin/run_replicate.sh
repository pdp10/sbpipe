#!/bin/bash
 
path=$1
name=$2
ext=$3
replicates=$4

# Creates replicates
for (( i=1; i<=$replicates; i+=1 ))
do
  echo "cp ${path}/${name}.${ext} ${path}/${name}${i}.${ext}"
  cp ${path}/${name}.${ext} ${path}/${name}${i}.${ext}
done
