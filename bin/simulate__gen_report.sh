#!/bin/bash


# read the model_noext
model_noext=$1
# read the results_dir
results_dir=$2
# the directory containing the time courses results combined with experimental data
tc_mean_dir=$3
# The prefix name for the report
simulate__prefix_results_filename=$4



echo "python ${SB_PIPE}/bin/latex_report.py"
python ${SB_PIPE}/bin/simulate__report.py ${model_noext} ${results_dir} ${tc_mean_dir} ${simulate__prefix_results_filename}

cd ${results_dir}
echo "pdflatex ${simulate__prefix_results_filename}${model_noext}.tex ... "
pdflatex ${simulate__prefix_results_filename}${model_noext}.tex  #>/dev/null
pdflatex ${simulate__prefix_results_filename}${model_noext}.tex  #>/dev/null
rm -rf ${simulate__prefix_results_filename}${model_noext}.out ${simulate__prefix_results_filename}${model_noext}.log ${simulate__prefix_results_filename}${model_noext}.idx ${simulate__prefix_results_filename}${model_noext}.toc ${simulate__prefix_results_filename}${model_noext}.aux
echo "DONE"
#echo "okular ${simulate__prefix_results_filename}${model_noext}.pdf"
#okular ${simulate__prefix_results_filename}${model_noext}.pdf &
#cd -
