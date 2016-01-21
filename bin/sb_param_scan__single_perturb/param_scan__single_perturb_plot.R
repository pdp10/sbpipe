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
# Object: Plotting of time courses columns wrt time. 
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-11-16 12:14:32 $
# $Id: param_scan__sim_parameter_scan.R,v 3.0 2010-11-16 19:45:32 Piero Dalle Pezze Exp $


# Retrieve the environment variable SB_PIPE_LIB
SB_PIPE_LIB <- Sys.getenv(c("SB_PIPE_LIB"))
# Add a collection of R functions
source(paste(SB_PIPE_LIB, "/R/single_perturb_plots_func.R", sep=""))





main <- function(args) {
    model_noext <- args[1]
    species <- args[2]
    inhibition_only <- args[3]
    results_dir <- args[4]
    dataset_parameter_scan_dir <- args[5]
    tc_parameter_scan_dir <- args[6]
    simulate__start <- as.numeric(args[7])
    simulate__end <- as.numeric(args[8])
    simulate__interval_size <- as.numeric(args[9])
    simulate__xaxis_label <- args[10]
    param_scan__single_perturb_simulations_number <- args[11]
    perturbation_in_percent_levels <- args[12]

    # Add controls here if any
    
    plot_single_perturbation_data(model_noext, species, inhibition_only, results_dir, dataset_parameter_scan_dir, tc_parameter_scan_dir, simulate__start, simulate__end, simulate__interval_size, simulate__xaxis_label, param_scan__single_perturb_simulations_number, perturbation_in_percent_levels)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
