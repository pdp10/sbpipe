#!/bin/bash



model="mtor_model_0_8_6_0_FEBS_model"
local_dir=`dirname $0`


echo "MODEL: $model"
echo "Have you set PI3K_level from 0 to 100 in COPASI-ParameterScanTask? "
echo "(Remember to deselect 'UseInitialExpression' in Specie-PI3K_level) "
read pi3k
if [[ "$pi3k" == "Y" || "$pi3k" == "y" ]] ; then 
  echo "bash ${local_dir}/parscan__copasi_wplots_wreport.sh $model only_PI3K_level Y"
  bash ${local_dir}/parscan__copasi_wplots_wreport.sh $model only_PI3K_level Y
fi

echo "Have you set mTOR_level from 0 to 100 in COPASI-ParameterScanTask?"
echo "(Remember to deselect 'UseInitialExpression' in Specie-mTOR_level) "
read mtor
if [[ "$mtor" == "Y" || "$mtor" == "y" ]] ; then 
  echo "bash ${local_dir}/parscan__copasi_wplots_wreport.sh $model only_mTOR_level Y"
  bash ${local_dir}/parscan__copasi_wplots_wreport.sh $model only_mTOR_level Y
fi

echo "Have you set comb_PI3K_mTOR_level from 0 to 100 in COPASI-ParameterScanTask?"
echo "(Remember to select 'UseInitialExpression' and set the InitialExpression to comb_PI3K_mTOR_level in Specie-PI3K_level and Specie-mTOR_level) "
read comb
if [[ "$comb" == "Y" || "$comb" == "y" ]] ; then 
  echo "bash ${local_dir}/parscan__copasi_wplots_wreport.sh $model comb_PI3K_mTOR_level Y"
  bash ${local_dir}/parscan__copasi_wplots_wreport.sh $model comb_PI3K_mTOR_level Y
fi

# Prepare the legend
Rscript parscan__make_legend.R ${local_dir}/../results inhibitors_legend 0 100 Y

# Generate the comparison report
python ${local_dir}/compare_inibitors_proc.py

# Visualize the report
okular "${local_dir}/../results/hp_comparison/graphs_par_scan_${model}.pdf" &

