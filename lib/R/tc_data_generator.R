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
# Object: Generator of sample time courses using experimental mean and standard deviation. 
# Input and output files are csv files (fields separated by comma, NaN for empty values).
# This script expects 4 inputs: file_in, file_out, sample number, lognormal (boolean).
# lognormal is a boolean, true if log normal distribution is used. If this is used 
# data must be geometric mean and sd.
#
# The output file can be used in Copasi for parameter fitting.
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
# SB_PIPE_LIB <- Sys.getenv(c("SB_PIPE_LIB"))
# Add a collection of R functions
#source(paste(SB_PIPE_LIB, "/R/plot_functions.R", sep=""))



main <- function(args) {
    data_file <- args[1] # a file containing readouts specified as time,mean,sd,mean,sd, ...
    sample_file <- args[2]
    samples.num <- as.numeric(args[3])
    lognormal <- args[4] # a boolean, true if log normal distribution is used. If this is used 
                         # data must be geometric mean and sd.
    resampling <- args[5] # a boolean, true if resampling is desired when a NA or negative value is computed.
    
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
    
    # parse the columns from the input files (time,mean,sd,mean,sd, ..)
    while(d <= column.number) {
      print(column.name[d])
      column.export <- c(column.export, column.name[d])
      # condense mean + sd into one column (a sample)
      s.i <- s.i + 1
      
      mat3d[,1,] <- time
      for(s.j in 1:samples.rows) { 

	if(lognormal == "true") {
 
	  # Use of geometric mean, sd and Log-Normal distribution.
	  tp.mean <- data[s.j, d]
	  tp.sd <- data[s.j, d+1]
	  sample <- rlnorm(samples.num, meanlog=tp.mean, sdlog=tp.sd)

	  if(resampling == "false") {
	    # DISCARD IF NA or O
	    for(s.k in 1:samples.num) {
	      logSample = log(sample[s.k])
	      ##logSample = sample[s.k]
	      if(!is.na(logSample) && logSample > 0) {
		mat3d[s.j, s.i, s.k] = logSample
	      }
	    }
	  } else {
	    # RE-SAMPLE IF NA or O
	    for(s.k in 1:samples.num) { 
	      while(!is.na(log(sample[s.k])) && log(sample[s.k]) <= 0) {
		sample[s.k] <- rlnorm(1, meanlog=tp.mean, sdlog=tp.sd)
	      }      
	      # copy the data
	      mat3d[s.j, s.i, s.k] = log(sample[s.k])
	    }
	  }
	  
	  
	} else {
	  # Use of arithmetic mean, sd and Normal distribution.
	  tp.mean <- data[s.j, d]
	  tp.sd <- data[s.j, d+1]
	  sample <- rnorm(samples.num, mean=tp.mean, sd=tp.sd)

	  if(resampling == "false") {
	    # DISCARD IF NA or O
	    for(s.k in 1:samples.num) {
	      if(!is.na(sample[s.k]) && sample[s.k] > 0) {
		mat3d[s.j, s.i, s.k] = sample[s.k]
	      }
	    }  
	  } else {
	    # RE-SAMPLE IF NA or O
	    for(s.k in 1:samples.num) { 
	      while(!is.na(sample[s.k]) && sample[s.k] <= 0) {
		sample[s.k] <- rnorm(1, tp.mean, tp.sd) 
	      }
	      # copy the data
	      mat3d[s.j, s.i, s.k] = sample[s.k]
	    }
	  }
	}

      }
      d <- d+2     
    }
    
    #print(mat3d)
    print(column.export)

    # delete a previous file if this exists
    if (file.exists(sample_file)) file.remove(sample_file)
    
    # save data on file
    for(k in 1:samples.num) {
      if(samples.rows == 1) {
        # take the transpose to print it as a row and not as a column.
	write.table(t(mat3d[, , k]), file = sample_file, append = TRUE, quote = FALSE, sep = ",",
            na = "", row.names = FALSE, col.names = c(column.export))
      } else {
	write.table(mat3d[, , k], file = sample_file, append = TRUE, quote = FALSE, sep = ",",
            na = "", row.names = FALSE, col.names = c(column.export))      
      }
# Copasi throws an Error if an empty line is added between repeats. 
# Weird as the documentation says to add it!            
#      write.table(array(NA, dim=c(1, samples.cols)), file = sample_file, append = TRUE, quote = FALSE, sep = ",",
#            na = "", row.names = FALSE, col.names = FALSE)            
    }
    
}


main(commandArgs(TRUE))
# Clean the environment
rm (list=ls())

