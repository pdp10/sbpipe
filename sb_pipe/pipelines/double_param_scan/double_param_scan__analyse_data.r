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

    # Add controls here if any
    
    plot_double_param_scan_data(model_noext, scanned_par1, scanned_par2, 
				inputdir, outputdir)    
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
