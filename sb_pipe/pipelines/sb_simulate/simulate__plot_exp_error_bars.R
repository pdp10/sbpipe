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
# Object: Plotting of the confidence intervals
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $



# Compute statistics and plot the mean with error bars.


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(paste(SB_PIPE, "/sb_pipe/utils/R/error_bars_func.R", sep=""))



main <- function(args) {
    data_dir <- args[1]
    # Not using: experimental dataset normalised by (y = log10(x) + 1)
    inputdir <- args[2]
    outputdir <- args[3]
    outputfile <- args[4]
    # For compatibility this is hold. No Version as we are printing the experimental data
    version <- ""

    
      # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }  
    
    # collect all files in the directory
    #files <- c("exp_as001_az.csv","exp_as001_bc.csv","exp_as001_bh.csv","exp_as001_bj.csv")
    files <- list.files(path=inputdir, pattern=".csv")
    
    print(files)
    timepoints <- c ( 0, 1, 3, 5, 10, 15, 20, 30, 45, 60, 120 )    # to add 1440
    #timepoints <- c ( 0, 1, 3, 5, 10, 15, 20, 30, 45, 60, 120, 1440 )    # to add 1440
    exp = TRUE
    plot_error_bars_plus_statistics(inputdir, outputdir, version, files, outputfile, timepoints, exp)

}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())



