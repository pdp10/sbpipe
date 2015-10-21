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
# Object: Plotting of model parameters correlations
#
# Institute for Ageing and Health
# Newcastle University
# Newcastle upon Tyne
# NE4 5PL
# UK
# Tel: +44 (0)191 248 1106
# Fax: +44 (0)191 248 1101
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $



library(colorspace)
library(gplots)


# Retrieve the environment variable PROJ_LIB
PROJ_LIB <- Sys.getenv(c("PROJ_LIB"))
# Add a collection of R functions
source(paste(PROJ_LIB, "/R/plot_functions.R", sep=""))



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