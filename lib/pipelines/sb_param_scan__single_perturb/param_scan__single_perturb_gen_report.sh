#!/bin/bash
# -*- coding: utf-8 -*-
#
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
# Object: Autogeneration of latex code containing images
#
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $

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


echo "python ${SB_PIPE_LIB}/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_report.py"
python ${SB_PIPE_LIB}/pipelines/sb_param_scan__single_perturb/param_scan__single_perturb_report.py $model_noext $specie ${results_dir} ${tc_parameter_scan_dir} ${param_scan__single_perturb_prefix_results_filename} ${tc_parameter_scan_dir} ${param_scan__single_perturb_legend}

cd ${results_dir}
echo "pdflatex -halt-on-error ${param_scan__single_perturb_prefix_results_filename}${model_noext}.tex ... "
pdflatex -halt-on-error ${param_scan__single_perturb_prefix_results_filename}${model_noext}.tex # >/dev/null
pdflatex -halt-on-error ${param_scan__single_perturb_prefix_results_filename}${model_noext}.tex # >/dev/null
rm -rf ${param_scan__single_perturb_prefix_results_filename}${model_noext}.out ${param_scan__single_perturb_prefix_results_filename}${model_noext}.log ${param_scan__single_perturb_prefix_results_filename}${model_noext}.idx ${param_scan__single_perturb_prefix_results_filename}${model_noext}.toc ${param_scan__single_perturb_prefix_results_filename}${model_noext}.aux
echo "DONE"
#echo "okular ${param_scan__single_perturb_prefix_results_filename}${model_noext}.pdf"
#okular ${param_scan__single_perturb_prefix_results_filename}${model_noext}.pdf &
#cd -
