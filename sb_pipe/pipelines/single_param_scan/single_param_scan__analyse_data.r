# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Plotting of time courses columns wrt time. 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-11-16 12:14:32 $


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
# Add a collection of R functions
source(file.path(SB_PIPE, 'sb_pipe','pipelines','single_param_scan','single_param_scan__plots_func.r'))


main <- function(args) {
    model_noext <- args[1]
    species <- args[2]
    inhibition_only <- args[3]
    results_dir <- args[4]
    dataset_parameter_scan_dir <- args[5]
    tc_parameter_scan_dir <- args[6]
    simulate__xaxis_label <- args[7]
    simulations_number <- args[8]
    percent_levels <- args[9]    
    min_level <- args[10]
    max_level <- args[11]
    levels_number <- args[12]
    homogeneous_lines <- args[13]

    
    # Add controls here if any
    if(homogeneous_lines=="true" || homogeneous_lines=="True" || homogeneous_lines=="TRUE") {
      homogeneous_lines <- TRUE
    } else {
      homogeneous_lines <- FALSE      
    }
    
    if(inhibition_only=="true" || inhibition_only=="True" || inhibition_only=="TRUE") {
      inhibition_only <- TRUE
    } else {
      inhibition_only <- FALSE
    }
      
    if(percent_levels=="true" || percent_levels=="True" || percent_levels=="TRUE") {
      percent_levels <- TRUE
    } else {
      percent_levels <- FALSE      
    }
    
    
    if(homogeneous_lines) {
	plot_single_param_scan_data_homogen(model_noext, species, 
				    results_dir, dataset_parameter_scan_dir, 
				    tc_parameter_scan_dir, simulate__xaxis_label, 
				    simulations_number)
    } else {    
	plot_single_param_scan_data(model_noext, species, inhibition_only, 
				    results_dir, dataset_parameter_scan_dir, 
				    tc_parameter_scan_dir, simulate__xaxis_label, 
				    simulations_number, percent_levels, min_level, 
				    max_level, levels_number)
    }
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
