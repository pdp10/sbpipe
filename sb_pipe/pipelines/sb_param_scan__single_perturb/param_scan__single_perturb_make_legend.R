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
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2011-07-7 16:14:32 $

# Create a legend

# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
# Add a collection of R functions
source(paste(SB_PIPE, "/sb_pipe/utils/R/plot_functions.R", sep=""))


main <- function(args) {
    # The name of the legend
    path <- args[1]
    # The name of the legend
    name <- args[2]
    # The minimum value
    min <- args[3]
    # the maximum value
    max <- args[4]
    # a boolean. Y = KD_only (blue), N = KD (blue) + overexpression (red)
    inhibition_only <- args[5]
    # "true" or "false" as string
    perturbation_in_percent_levels <- args[6]
    # The number of lines to be drawn
    values <- args[7]
    make_legend(path, name, min, max, values, inhibition_only, perturbation_in_percent_levels)
    make_legend_sim_exp(path, name)
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())

