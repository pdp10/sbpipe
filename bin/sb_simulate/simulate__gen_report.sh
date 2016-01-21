#!/bin/bash
# -*- coding: utf-8 -*-
#
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either model_noext 2 of the License, or (at
# your option) any later model_noext.
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
# Object: Autogeneration of latex code containing images
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $


# read the model_noext
model_noext=$1
# read the results_dir
results_dir=$2
# the directory containing the time courses results combined with experimental data
tc_mean_dir=$3
# The prefix name for the report
simulate__prefix_results_filename=$4



echo "python ${SB_PIPE}/bin/sb_simulate/latex_report.py"
python ${SB_PIPE}/bin/sb_simulate/simulate__report.py ${model_noext} ${results_dir} ${tc_mean_dir} ${simulate__prefix_results_filename}

cd ${results_dir}
echo "pdflatex -halt-on-error ${simulate__prefix_results_filename}${model_noext}.tex ... "
pdflatex -halt-on-error ${simulate__prefix_results_filename}${model_noext}.tex  #>/dev/null
pdflatex -halt-on-error ${simulate__prefix_results_filename}${model_noext}.tex  #>/dev/null
rm -rf ${simulate__prefix_results_filename}${model_noext}.out ${simulate__prefix_results_filename}${model_noext}.log ${simulate__prefix_results_filename}${model_noext}.idx ${simulate__prefix_results_filename}${model_noext}.toc ${simulate__prefix_results_filename}${model_noext}.aux
echo "DONE"
#echo "okular ${simulate__prefix_results_filename}${model_noext}.pdf"
#okular ${simulate__prefix_results_filename}${model_noext}.pdf &
#cd -
