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
# Object: Plotting of time courses columns wrt time. 
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



# Retrieve the environment variable PROJ_LIB
PROJ_LIB <- Sys.getenv(c("PROJ_LIB"))
# Add a collection of R functions
source(paste(PROJ_LIB, "/R/plot_functions.R", sep=""))



main <- function(args) {
    # The model model_noext
    model_noext <- args[1]
    inputdir <- args[2]
    outputdir <- args[3]
    

    # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }

    file <- list.files( path=inputdir, pattern=model_noext )
    
    # This assumes team=kathrin (....TODO)
    timepoints <- c ( 1, 3, 5, 10, 15, 20, 30, 45, 60, 120 )    # to add 1440
    
    
    linewidth <- 8
    # Timecourses and single boxplots
    # for each item in the vector file
    for ( i in 1:length (file)) {
      # load file[i] in the table timecourses
      timecourses <- read.table ( paste ( inputdir, file[i], sep="" ), header=TRUE, na.strings="NA", dec=".", sep="\t" )
      column <- names ( timecourses )
      print(file[i])
      # for each name contained column 
      for ( j in 1:length ( column ) ) {
	# Avoid the plot of Time vs Time
	if ( column[j] == "Time" ||
	    substr( column[j], 1, 6 ) == "Values" ||
	    substr( column[j], 1, 12 ) == "Compartments" ||
	    substr( column[j], 1, 1 ) == "X") { }
	else {
	  # Time vs column[j] scatterplot
	  # size : height=295, width=300
	  print(column[j])
	  plot_single_timecourse(timecourses, outputdir, model_noext, column[j], timepoints, linewidth)
	}
      }
      # clean the tables
      rm ( timecourses )
    }
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())



