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
# You should hade received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
# Object: Time course data generator
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-03-15 09:45:32 $






# To launch the script, type
# $ R
# > source("/home/ariel/filename.R")
#
# OR type
# $ R CMD BATCH /home/ariel/filename.R


# To include libraries
#library ( lattice  )
# library( car ) # scatterplot


# Retrieve the environment variable SB_PIPE_LIB
SB_PIPE_LIB <- Sys.getenv(c("SB_PIPE_LIB"))
# Add a collection of R functions
#source(paste(SB_PIPE_LIB, "/R/plot_functions.R", sep=""))



main <- function(args) {
    data_file <- args[1] # a file containing readouts specified as time, mean, sd, mean, sd, ...
    sample_file <- args[2]
    samples.num <- as.numeric(args[3])
    
#    data_file <- "data_file.csv"
#    sample_file <- "samples_file.csv"
#    samples.num <- 10
    
    data <- read.table(data_file,header=TRUE,na.strings="NaN",dec=".",sep=",")

    column.name <- names(data)
    column.number <- length(column.name)
    column.export <- c("time")
    
    samples.rows <- length(data[,1])
    samples.cols <- ((column.number-1)/2)+1
    
    data.length <- samples.rows * samples.cols * samples.num
    
    mat3d <- array(NA, dim=c(samples.rows, samples.cols, samples.num))
    #print(mat3d)
    
    time <- data[,1]
    d <- 2
    s.i <- 1
    
    # parse the columns from the input files (time, mean, sd, mean, sd, ..)
    while(d <= column.number) {
      print(column.name[d])
      column.export <- c(column.export, column.name[d])
      # condense mean + sd into one column (a sample)
      s.i <- s.i + 1
      
      mat3d[,1,] <- time
      for(s.j in 1:samples.rows) { 
	tp.mean <- data[s.j, d]
	tp.sd <- data[s.j, d+1]
	sample <- rnorm(samples.num, tp.mean, tp.sd) 
	
	# discard negative values as they don't make sense in this context
	for(s.k in 1:samples.num) { 
	  while(!is.na(sample[s.k]) && sample[s.k] <= 0) {
	    sample[s.k] <- rnorm(1, tp.mean, tp.sd) 
	  }
	}
	
	# copy the data
	for(s.k in 1:samples.num) {
	  mat3d[s.j, s.i, s.k] = sample[s.k]
	}
      }
      d <- d+2     
    }
    
    # print(mat3d)


    # delete a previous file if this exists
    if (file.exists(sample_file)) file.remove(sample_file)
    
    # save data on file
    for(k in 1:samples.num) {
      write.table(mat3d[, , k], file = sample_file, append = TRUE, quote = FALSE, sep = "\t",
            na = "", row.names = FALSE, col.names = c(column.export))
    }
    
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())

