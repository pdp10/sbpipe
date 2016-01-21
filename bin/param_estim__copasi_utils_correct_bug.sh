#!/bin/bash
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#    
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
# Object: compute the ratio of contribution between two pathway of activation
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-05-06 10:14:32 $

# Read the project name
project=$1
# read the model
model=$2
# the time point to collect the result
timepoint=$2
#timepoint=30


="${model%.*}"

local_dir=`dirname $0`
models_dir="${local_dir}/../${project}/Models/"
results_dir="${local_dir}/../${project}/simulations/${}/"




cd ${models_dir}/


# remove existing *_short model_noext.csv
rm -rf ${model_noext}_short.csv

cp ${model_noext}.csv ${model_noext}_short.csv
# Replace some string in the report model_noext
sed -i "s/mTOR model\[Time\]/Time/g" ${model_noext}_short.csv
sed -i "s/\[ParticleNumber\]//g" ${model_noext}_short.csv



# Delete every 2nd line starting from the 1st line (all odd lines). It corrects a bug in copasi..
sed '1~2 d' -i ${model_noext}_short.csv
# Delete all blank lines.
# sed -i "/^$/d" ${model_noext}_short.csv



# select the lines starting with the specified time point (^pattern . pattern$ is for string ending with pattern)
# w -> Select only those lines containing matches that form whole words.
grep -w ^${timepoint} ${model_noext}_short.csv > ${model_noext}_tmp.csv
# sed -n "/${timepoint}\t/p" ${model_noext}_short.csv > ${model_noext}_tmp.csv

# remove duplicate, consecutive lines
awk 'a !~ $0; {a=$0}' ${model_noext}_tmp.csv > ${model_noext}_tmp2.csv
# remove duplicate, non consecutive lines
#awk ' !x[$0]++' ${model_noext}_tmp.csv > ${model_noext}_tmp2.csv



# create blocks of 11 lines, separated by blank line
#sed 'n;n;n;n;n;n;n;n;n;n;G;' -i ${model_noext}_tmp2.csv



# Write the header line
head -1 ${model_noext}_short.csv > ${model_noext}_sel_tp_$timepoint.csv
# Write the blocks of the specified time point
cat ${model_noext}_tmp2.csv >> ${model_noext}_sel_tp_$timepoint.csv

# if [[ $model_noext = *PI3K_KD* ]]
# then
#   for i in {1..10}
#   do
#     # complete the last kd (PI3K_like is 0%, unknown is 100%). So there is no knockdown effect and the lines are equal and deleted.
#     # here, lines are restored for completeness 
#     tail -1 ${model_noext}_tmp2.csv >> ${model_noext}_sel_tp_$timepoint.csv
#   done
# fi



# remove temporary model_noexts
rm ${model_noext}_tmp.csv ${model_noext}_tmp2.csv




Rscript add_ratio_pi3k_unknown_column.R ${model_noext}_sel_tp_${timepoint}.csv ${model_noext}_sel_tp_${timepoint}_summary.csv

# create blocks of 11 lines, separated by blank line
#sed 'n;n;n;n;n;n;n;n;n;n;G;' -i ${model_noext}_sel_tp_${timepoint}_summary.csv
sed '12~11G' -i ${model_noext}_sel_tp_${timepoint}_summary.csv

cp ${model_noext}.csv ${results_dir}/
cp ${model_noext}_short.csv ${results_dir}/
mv ${model_noext}_sel* ${results_dir}/



cd -


