#!/bin/bash


# read the model_noext
model_noext=$1

# read the specie
specie=$2

# read the results dir
results_dir=$3

# the directory containing the plots of the single perturbation scan
tc_parameter_scan_dir=${4}

# The prefix for the results filename
param_scan__single_perturb_prefix_results_filename=${5}

# The name of the legend
param_scan__single_perturb_legend=${6}


echo "python ${SB_PIPE}/bin/sb_param_scan__single_perturb/latex_report_par_scan.py"
python ${SB_PIPE}/bin/sb_param_scan__single_perturb/param_scan__single_perturb_report.py $model_noext $specie ${results_dir} ${tc_parameter_scan_dir} ${param_scan__single_perturb_prefix_results_filename} ${tc_parameter_scan_dir} ${param_scan__single_perturb_legend}

cd ${results_dir}
echo "pdflatex ${param_scan__single_perturb_prefix_results_filename}${model_noext}.tex ... "
pdflatex ${param_scan__single_perturb_prefix_results_filename}${model_noext}.tex  >/dev/null
pdflatex ${param_scan__single_perturb_prefix_results_filename}${model_noext}.tex  >/dev/null
rm -rf ${param_scan__single_perturb_prefix_results_filename}${model_noext}.out ${param_scan__single_perturb_prefix_results_filename}${model_noext}.log ${param_scan__single_perturb_prefix_results_filename}${model_noext}.idx ${param_scan__single_perturb_prefix_results_filename}${model_noext}.toc ${param_scan__single_perturb_prefix_results_filename}${model_noext}.aux
echo "DONE"
#echo "okular ${param_scan__single_perturb_prefix_results_filename}${model_noext}.pdf"
#okular ${param_scan__single_perturb_prefix_results_filename}${model_noext}.pdf &
#cd -
