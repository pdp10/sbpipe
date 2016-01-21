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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $

# This script processes the parted datasets of a double perturbation 
# experiment and generates the plots. 


# The project name
project=$1
# The model name 
model=$2
# The number of files to combine
nfiles=$3
# The dataset folder of the double perturbation (e.g. "perturb_AMPK_mTORC1_data")
dp_dataset_dir=$4
# The length of the simulation (e.g 21)
sim_length=$5



# Concatenates the parted files of a double perturbation experiment (${nfiles} subfiles => 1 merged file)
${SB_PIPE}/bin/param_scan__double_perturb_concat_files.sh ${project} ${model} ${nfiles} ${dp_dataset_dir}

# Extract the single timepoints of the double perturbation (1 merged file => ${sim_length} time-point files}
${SB_PIPE}/bin/param_scan__double_perturb_extract_timepoints.sh ${project} ${model} ${sim_length} ${dp_dataset_dir}

# Generate plots for each time points 
path="${SB_PIPE}/${project}/simulations/"
folderin="dp_dataset_dir"
matlab -desktop -r "try; path=\'${path}\'; folderin=\'${folderin}\'; run(\'${SB_PIPE}/bin/param_scan__double_perturb_plot_surfaces.m\'); catch; end; quit"


