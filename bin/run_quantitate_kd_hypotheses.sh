#!/bin/bash
# This file is part of SB pipe.
#
# SB pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SB pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SB pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $


folders=("../results/mtor_model_0_8_5_0_tsc_dep_model/dataset_parameter_scan/"
	 "../results/mtor_model_0_8_5_0_pi3k_dep_model/dataset_parameter_scan/"
	 "../results/mtor_model_0_8_5_0_pi3k_indep_model/dataset_parameter_scan/")

files=("tsc_dep" "pi3k_dep" "pi3k_indep")
timepoints=(60 100 30)

rm -rf quantitation_of_*.csv



for index in ${!folders[*]}
do
  echo "create ${files[$index]} output file and correspondent header line"
  touch quantitation_of_${files[$index]}.csv

  echo "Append the extrated data:"
  echo -e "\tTSC KD quantitation (time point: ${timepoints[0]} min)"
  echo -e "\nTSC Knockdown (time point: ${timepoints[0]} min)\n" >> quantitation_of_${files[$index]}.csv
  echo -e "Time\tAkt-T308\tAkt-S473\tmTOR-S2481" >> quantitation_of_${files[$index]}.csv
  model="mtor_model_0_8_5_0_"${files[$index]}"_model_scan_1_TSC_clx_"
  suffixes=("10" "8" "5" "2" "0")
  line=$((${timepoints[0]}+2))
  for suffix in ${suffixes[*]}
  do
    awk -v ln=$line 'FNR==ln {print $1"\t"$3"\t"$4"\t"$24}' ${folders[$index]}${model}$suffix.csv >> quantitation_of_${files[$index]}.csv
  done

  echo -e "\tmTORC1 KD quantitation (time point: ${timepoints[1]} min)"
  echo "" >> quantitation_of_${files[$index]}.csv
  echo -e "\nmTORC1 Knockdown (time point: ${timepoints[1]} min)\n" >> quantitation_of_${files[$index]}.csv
  echo -e "Time\tAkt-T308\tAkt-S473\tmTOR-S2481" >> quantitation_of_${files[$index]}.csv
  model="mtor_model_0_8_5_0_"${files[$index]}"_model_scan_1_mTORC1_"
  suffixes=("4" "3" "2" "1" "0")
  line=$((${timepoints[1]}+2))
  for suffix in ${suffixes[*]}
  do
    awk -v ln=$line 'FNR==ln {print $1"\t"$3"\t"$4"\t"$24}' ${folders[$index]}${model}$suffix.csv >> quantitation_of_${files[$index]}.csv
  done

  echo -e "\tPI3K inhib quantitation (time point: ${timepoints[2]} min)"
  echo -e "\nPI3K Inhibition (time point: ${timepoints[2]} min)\n" >> quantitation_of_${files[$index]}.csv
  echo -e "Time\tAkt-T308\tAkt-S473\tmTOR-S2481" >> quantitation_of_${files[$index]}.csv
  model="mtor_model_0_8_5_0_"${files[$index]}"_model_scan_1_IRS1_PI3K_"
  suffixes=("2.965" "2.22375" "1.4825" "0.74125" "0")
  line=$((${timepoints[2]}+2))
  for suffix in ${suffixes[*]}
  do
    awk -v ln=$line 'FNR==ln {print $1"\t"$3"\t"$4"\t"$24}' ${folders[$index]}${model}$suffix.csv >> quantitation_of_${files[$index]}.csv
  done

done



