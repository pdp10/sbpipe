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
source(file.path(SB_PIPE, 'sb_pipe','pipelines','double_param_scan','double_param_scan__plots_func.r'))


main <- function(args) {
    model_noext <- args[1]
    scanned_par1 <- args[2]
    scanned_par2 <- args[3]
    inputdir <- args[4]
    outputdir <- args[5]
    
    plot_double_param_scan_data(model_noext, scanned_par1, scanned_par2, 
				inputdir, outputdir)    
    
    ## POSSIBLY REMOVE
    # Add controls here if any
#     if(homogeneous_lines=="true" || homogeneous_lines=="True" || homogeneous_lines=="TRUE") {
#       homogeneous_lines <- TRUE
#     } else {
#       homogeneous_lines <- FALSE      
#     }
#     
#     if(inhibition_only=="true" || inhibition_only=="True" || inhibition_only=="TRUE") {
#       inhibition_only <- TRUE
#     } else {
#       inhibition_only <- FALSE
#     }
#       
#     if(percent_levels=="true" || percent_levels=="True" || percent_levels=="TRUE") {
#       percent_levels <- TRUE
#     } else {
#       percent_levels <- FALSE      
#     }
    
    #matlab -desktop -r "try; SB_PIPE=getenv('SB_PIPE'); dp_dir='"${dp_dir}"'; dp_datasets_dir='"${dp_datasets_dir}"'; perturbed_species='"${param_scan__double_perturb_copasi_species}"'; param_scan__double_perturb_suffix_plots_folder='"${param_scan__double_perturb_suffix_plots_folder}"'; param_scan__double_perturb_intervals_first_species=${param_scan__double_perturb_intervals_first_species}; param_scan__double_perturb_type_first_species='"${param_scan__double_perturb_type_first_species}"'; param_scan__double_perturb_intervals_second_species=${param_scan__double_perturb_intervals_second_species}; param_scan__double_perturb_type_second_species='"${param_scan__double_perturb_type_second_species}"'; param_scan__double_perturb_plots_3D='"${param_scan__double_perturb_plots_3D}"'; param_scan__double_perturb_plots_2D_pub='"${param_scan__double_perturb_plots_2D_pub}"'; run([SB_PIPE,'/bin/sb_param_scan__double_perturb/param_scan__double_perturb_plot_surfaces.m']); catch; end; quit; "

}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
