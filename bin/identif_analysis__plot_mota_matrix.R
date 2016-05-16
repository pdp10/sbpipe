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
# Object: Plotting of model parameters correlations
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $



library(colorspace)
library(gplots)


# Retrieve the environment variable SB_PIPE_LIB
SB_PIPE_LIB <- Sys.getenv(c("SB_PIPE_LIB"))
# Add a collection of R functions
source(paste(SB_PIPE_LIB, "/R/plot_functions.R", sep=""))



main <- function(args) {
#    # the version of the model
#    version <- args[1]
#    # timepoints
#    inputdir <- paste("./", version, sep="")
#    # collect all *.csv files in the directory
#    files <- dir(path=inputdir, pattern="*.csv",full.names=TRUE, ignore.case = TRUE)  
#    columns <- 1
#    for(i in 1:length(files)) {
#      print(files[i])
#      # NOTE: the pipe-cut allows to select only the first line of the files[i] [ pipe("cut -f1,5,28 myFile.txt") ]
#      plot.param_correlations(files[i])      
#    }

    # Plot MOTA parameter correlation for 1 file
    file <- args[1]
    print(file)

    margin <- 24
    cex <- 1.2
    
    # NOTE: the pipe-cut allows to select only the first line of the file [ pipe("cut -f1,5,28 myFile.txt") ]
    plot.param_correlations(file,valmargin,valcex)      

}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())