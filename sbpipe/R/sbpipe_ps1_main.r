# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-11-16 12:14:32 $


# retrieve SBpipe folder containing R scripts
args <- commandArgs(trailingOnly = FALSE)
SBPIPE_R <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))
source(file.path(SBPIPE_R, 'sbpipe_ps1.r'))





# R Script to plot model single parameter scan time courses.
#
# :args[1]: the model name without extension
# :args[2]: true if the scanning only decreases the variable amount (inhibition only)
# :args[3]: the output directory
# :args[4]: the name of the folder containing the simulated data
# :args[5]: the name of the folder containing the simulated plots
# :args[6]: the simulation number
# :args[7]: true if scanning levels are in percent
# :args[8]: the minimum level
# :args[9]: the maximum level
# :args[10]: the number of levels
# :args[11]: true if lines should be plotted homogeneously
# :args[12]: the label for the x axis (e.g. Time [min])
# :args[13]: the label for the y axis (e.g. Level [a.u.])
main <- function(args) {
    model_noext <- args[1]
    inhibition_only <- args[2]
    outputdir <- args[3]
    sim_data_folder <- args[4]
    sim_plots_folder <- args[5]
    run <- args[6]
    percent_levels <- args[7]
    min_level <- args[8]
    max_level <- args[9]
    levels_number <- args[10]
    homogeneous_lines <- args[11]
    xaxis_label <- args[12]
    yaxis_label <- args[13]

    
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
        plot_single_param_scan_data_homogen(model_noext,
                        outputdir, sim_data_folder,
                        sim_plots_folder, run,
                        xaxis_label, yaxis_label)
    } else {    
        plot_single_param_scan_data(model_noext, inhibition_only,
                        outputdir, sim_data_folder,
                        sim_plots_folder, run,
                        percent_levels, min_level,
                        max_level, levels_number,
                        xaxis_label, yaxis_label)
    }
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
