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
# $Date: 2016-07-01 14:14:32 $


# Retrieve the environment variable SBPIPE
SBPIPE <- Sys.getenv(c("SBPIPE"))
source(file.path(SBPIPE, 'sbpipe','R','sbpipe_pe.r'))



# R Script to run model parameter estimation analysis and plot results. This script analyses
# only the best fits using a percent threshold.
#
# :args[1]: the model name without extension
# :args[2]: the dataset containing the parameter estimation data.
# :args[3]: the directory to save the generated plots
# :args[4]: the percent of best fits to analyse.
# :args[5]: true if parameters should be plotted in logspace.
# :args[6]: true if axis labels should be plotted in scientific notation.
main <- function(args) {
  
  model <- args[1]
  dataset <- args[2]
  plots_dir <- args[3]
  best_fits_percent <- args[4]
  logspace <- args[5]
  scientific_notation <- args[6]
  
  if(logspace == 'True' || logspace == 'TRUE' || logspace == 'true') { 
    logspace = TRUE
  } else { 
    logspace = FALSE
  }
  
  if(scientific_notation == 'True' || scientific_notation == 'TRUE' || scientific_notation == 'true') {
    scientific_notation = TRUE
  } else {
    scientific_notation = FALSE
  }  
  
  final_fits_analysis(model, dataset, plots_dir, best_fits_percent, logspace, scientific_notation)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )

