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
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-11-16 12:14:32 $


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
# Add a collection of R functions
source(file.path(SB_PIPE, 'sb_pipe','pipelines','single_param_scan','single_param_scan__plots_func.r'))



# R Script to plot model single parameter scan time courses.
#
# :args[1]: the model name without extension
# :args[2]: the model variable to scan
# :args[3]: true if the scanning only decreases the variable amount (inhibition only)
# :args[4]: the output directory
# :args[5]: the name of the folder containing the simulated data
# :args[6]: the name of the folder containing the simulated plots
# :args[7]: the label for the x axis (e.g. Time (min))
# :args[8]: the simulation number
# :args[9]: true if scanning levels are in percent
# :args[10]: the minimum level
# :args[11]: the maximum level
# :args[12]: the number of levels
# :args[13]: true if lines should be plotted homogeneously
main <- function(args) {
    model_noext <- args[1]
    variable <- args[2]
    inhibition_only <- args[3]
    outputdir <- args[4]
    sim_data_folder <- args[5]
    sim_plots_folder <- args[6]
    xaxis_label <- args[7]
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
	plot_single_param_scan_data_homogen(model_noext, variable, 
				    outputdir, sim_data_folder, 
				    sim_plots_folder, xaxis_label, 
				    simulations_number)
    } else {    
	plot_single_param_scan_data(model_noext, variable, inhibition_only, 
				    outputdir, sim_data_folder, 
				    sim_plots_folder, xaxis_label, 
				    simulations_number, percent_levels, min_level, 
				    max_level, levels_number)
    }
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
