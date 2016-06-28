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
# Object: Plotting of time courses columns wrt time. (ANNIKA's NEW EXPERIMENTS)
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2009-01-15 16:14:32 $
# $Id: plot_experiments_new.R,v 3.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $



# To launch the script, type
# $ R
# > source("/home/ariel/filename.R")
#
# OR type
# $ R CMD BATCH /home/ariel/filename.R


# To include libraries
#library ( lattice  )
# library( car ) # scatterplot


# Retrieve the environment variable SB_PIPE
SB_PIPE <- Sys.getenv(c("SB_PIPE"))
source(paste(SB_PIPE, "/sb_pipe/utils/R/plot_functions.R", sep=""))



main <- function(args) {
    data_dir <- args[1]
    inputdir <- args[2]
    outputdir <- args[3]

      # create the directory of output
    if (!file.exists(outputdir)){ dir.create(outputdir) }      
    
    #files_exp <- c( "exp_as001_az.csv", "exp_as001_bc.csv", "exp_as001_bh.csv" ,"exp_as001_bj.csv")
    files_exp <- list.files(path=inputdir, pattern=".csv")    
    
    timepoints <- c ( 0, 1, 3, 5, 10, 15, 20, 30, 45, 60, 120, 1440 )    # to add 1440
    # Multiple curves for each plots (experiments)
    exp1 <- read.table(paste(inputdir,files_exp[1],sep=""),header=TRUE,na.strings="NA",dec=".",sep="\t")
    exp2 <- read.table(paste(inputdir,files_exp[2],sep=""),header=TRUE,na.strings="NA",dec=".",sep="\t")
    exp3 <- read.table(paste(inputdir,files_exp[3],sep=""),header=TRUE,na.strings="NA",dec=".",sep="\t")
    #exp4 <- read.table ( paste ( inputdir, files_exp[4], sep="" ), header=TRUE, na.strings="NA", dec=".", sep="\t" )
    column <- names (exp1)
    exp <- list(exp1, exp2, exp3)
    linewidth = 8

    # for each name contained column
    for ( j in 1:length ( column ) ) {
      if ( column[j] == "Time" ) { }
      else {
	print(column[j])
	plot_experimental_timecourse(outputdir, files_exp, exp, column[j], timepoints, linewidth)
	# plot correlations
	for(k in 1:(length(exp)-1)) {
	  for(l in (k+1):length(exp)) {
	    plot.correlation(paste(outputdir, substr( files_exp[1], 1, 3 ), "_corr_", column[j], "_exp", k, "_vs_", column[j], "_exp", l, ".png", sep="" ), exp[[k]][[column[j]]], exp[[l]][[column[j]]], paste(column[j], "_exp", k, sep=""),paste(column[j], "_exp", l, sep=""),linewidth)
	  }
	}
      }
    }
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())

