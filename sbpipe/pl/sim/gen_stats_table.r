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



# Retrieve the environment variable SBPIPE
SBPIPE <- Sys.getenv(c("SBPIPE"))
source(file.path(SBPIPE, 'sbpipe','pl','sim','plot_tc.r'))


# R Script to collect statistics.
#
# :args[1]: the model name without extension
# :args[2]: the input directory
# :args[3]: the output directory
# :args[4]: the output file name
# :args[5]: the label for the x axis (e.g. Time [min])
# :args[6]: the label for the y axis (e.g. Level [a.u.])
main <- function(args) {
    # The model model_noext
    model_noext <- args[1]
    inputdir <- args[2]
    outputdir <- args[3]
    outputfile <- args[4]
    xaxis_label <- args[5]
    yaxis_label <- args[6]
    
    gen_stats_table(inputdir, outputdir, model_noext, outputfile, xaxis_label, yaxis_label)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
