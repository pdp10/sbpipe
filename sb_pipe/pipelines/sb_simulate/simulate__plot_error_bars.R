# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: Plotting of the confidence intervals
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $



# To launch the script, type
# $ R
# > source("filename.R")
#
# OR type
# $ Rscritp filename.R



# Compute statistics and plot the mean with error bars.


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(paste(SB_PIPE, "/sb_pipe/utils/R/error_bars_func2.r", sep=""))



main <- function(args) {
    # The model model_noext
    model_noext <- args[1]
    inputdir <- args[2]
    outputdir <- args[3]
    outputfile <- args[4]
    simulate__xaxis_label <- args[5]
    

    # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }

    # collect all files in the directory
    files <- list.files( path=inputdir, pattern=model_noext )
    print(files)
    
    plot_error_bars_plus_statistics(inputdir, outputdir, model_noext, files, outputfile, simulate__xaxis_label)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
