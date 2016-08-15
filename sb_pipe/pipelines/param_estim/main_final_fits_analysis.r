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
# Object: Plotting of the confidence intervals
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-01 14:14:32 $


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(file.path(SB_PIPE, 'sb_pipe','pipelines','param_estim','param_estim_utils.r'))


main <- function(args) {
  
  model <- args[1]
  filename <- args[2]
  plots_dir <- args[3]
  best_fits_percent <- args[4]
  logspace <- args[5]
  
  if(logspace == 'True' || logspace == 'TRUE' || logspace == 'true') logspace = TRUE
  else logspace = FALSE

  final_fits_analysis(model, filename, plots_dir, best_fits_percent, logspace)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )

