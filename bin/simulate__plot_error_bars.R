# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either model_noext 2 of the License, or (at
# your option) any later model_noext.
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
# Object: Plotting of the confidence intervals
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



# To launch the script, type
# $ R
# > source("filename.R")
#
# OR type
# $ Rscritp filename.R



# Compute statistics and plot the mean with error bars.


# Retrieve the environment variable PROJ_LIB
PROJ_LIB <- Sys.getenv(c("PROJ_LIB"))
# Add a collection of R functions
source(paste(PROJ_LIB, "/R/error_bars_func.R", sep=""))



main <- function(args) {
    # The model model_noext
    model_noext <- args[1]
    inputdir <- args[2]
    outputdir <- args[3]
    outputfile <- args[4]
    team <- args[5]
    simulate__duration <- as.numeric(args[6])
    simulate__interval_size <- as.numeric(args[7])
    

    # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }

    # collect all files in the directory
    files <- list.files( path=inputdir, pattern=model_noext )
    print(files)

    exp = FALSE
    plot_error_bars_plus_statistics(inputdir, outputdir, model_noext, files, outputfile, team, simulate__duration, simulate__interval_size, exp)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
