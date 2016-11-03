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
# $Date: 2016-07-7 16:14:32 $


library(gplots)

# Retrieve the environment variable SBPIPE
SBPIPE <- Sys.getenv(c("SBPIPE"))
# Add a collection of R functions
source(file.path(SBPIPE, 'sbpipe','R','plots.r'))




# R Script to plot model sensitivities analysis.
#
# :args[1]: the directory containing the sensitivity analysis report.
main <- function(args) {
    # the model_noext of the model
    sensitivities_dir <- args[1]
 
    # timepoints
    inputdir <- sensitivities_dir
    # collect all *.csv files in the directory
    files <- dir(path=inputdir, pattern="*.csv",full.names=TRUE, ignore.case = TRUE)
    columns <- 1
    for(i in 1:length(files)) {
      print(files[i])
      # NOTE: the pipe-cut allows to select only the first line of the files[i] [ pipe("cut -f1,5,28 myFile.txt") ]
      if(length(grep("kin-rates", files[i], value=TRUE)) == 0) {
        plot_sensitivities(files[i], kinetics=FALSE)
      } else {
        plot_sensitivities(files[i], kinetics=TRUE)
      }
    }
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())
